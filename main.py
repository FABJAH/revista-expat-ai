# main.py - Servidor Backend con FastAPI
import json
import os
import threading
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from apscheduler.schedulers.background import BackgroundScheduler

from bots.orchestrator import Orchestrator
from bots.rss_manager import get_rss_manager
from bots.logger import logger


# --- Configurar scheduler en background ---
scheduler = BackgroundScheduler()


def sync_rss_feeds():
    """Tarea para sincronizar feeds RSS cada 6 horas"""
    try:
        rss_mgr = get_rss_manager()
        new_count = rss_mgr.sync_feeds()
        logger.info(f"RSS Sync completado: {new_count} artículos nuevos")
    except Exception as e:
        logger.error(f"Error sincronizando RSS: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager para startup y shutdown"""
    # Startup
    logger.info("Iniciando servidor...")
    rss_mgr = get_rss_manager()

    # Sync inicial en background para no bloquear startup
    def initial_sync():
        try:
            logger.info("Sincronizando RSS feeds en background...")
            rss_mgr.sync_feeds()
            logger.info("Sincronización inicial RSS completada")
        except Exception as e:
            logger.error(f"Error en sync inicial RSS: {e}")

    threading.Thread(target=initial_sync, daemon=True).start()

    scheduler.add_job(sync_rss_feeds, 'interval', hours=6)
    scheduler.start()
    logger.info("Scheduler iniciado: feeds sincronizarán cada 6 horas")

    yield

    # Shutdown
    scheduler.shutdown()
    flush_analytics_buffer()
    logger.info("Servidor detenido correctamente")


# --- Modelos de datos para validación ---


class QueryRequest(BaseModel):
    """Modelo para consultas al asistente"""
    pregunta: str | None = None
    question: str | None = None
    language: str = "es"
    session_id: str | None = None
    limit: int | None = 5
    offset: int = 0

    def get_question(self) -> str:
        """Retorna la pregunta, priorizando 'pregunta'"""
        return self.pregunta or self.question or ""


class AnalyticsEvent(BaseModel):
    """Modelo para eventos de analytics"""
    event: str
    data: dict = {}
    session_id: str | None = None
    timestamp: str | None = None


# --- Inicialización de FastAPI ---
app = FastAPI(
    title="Revista Expats AI API",
    description=(
        "API para el asistente virtual de la revista "
        "para expatriados en Barcelona."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Middleware: GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Middleware: Rate Limiting
limiter = Limiter(key_func=get_remote_address,
                  default_limits=["100/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware: CORS
production_mode = os.getenv("PRODUCTION", "false").lower() == "true"

if production_mode:
    # Producción: solo dominios específicos
    allowed_origins = [
        "https://www.barcelona-metropolitan.com",
        "https://barcelona-metropolitan.com",
    ]
else:
    # Desarrollo: permitir localhost
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Inicializar orquestador
try:
    orchestrator = Orchestrator()
    logger.info("Orquestador inicializado correctamente.")
except Exception as e:
    error_msg = (
        f"ERROR FATAL: No se pudo inicializar el Orquestador. "
        f"Causa: {e}"
    )
    logger.critical(error_msg)
    raise SystemExit(
        "El servidor no puede arrancar sin el Orquestador."
    )


# --- Endpoints de la API ---


@app.get("/api/health")
def health_check():
    """Verifica que el servidor está funcionando"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Revista Expats AI API"
    }


@app.get("/api/categories")
def get_categories():
    """Retorna las categorías disponibles"""
    return {
        "categories": [
            {"id": "accommodation", "name": "Alojamiento", "icon": "🏠"},
            {"id": "legal", "name": "Legal", "icon": "⚖️"},
            {"id": "healthcare", "name": "Salud", "icon": "🏥"},
            {"id": "education", "name": "Educación", "icon": "🎓"},
            {"id": "restaurants", "name": "Restaurantes",
             "icon": "🍽️"},
            {"id": "social", "name": "Social", "icon": "👥"},
            {"id": "work", "name": "Trabajo", "icon": "💼"},
            {"id": "service", "name": "Servicios", "icon": "🔧"},
            {"id": "comercial", "name": "Comercial", "icon": "🛍️"}
        ]
    }


@app.get("/api/sync-rss")
def manual_sync_rss():
    """Sincroniza feeds RSS manualmente"""
    try:
        rss_mgr = get_rss_manager()
        new_count = rss_mgr.sync_feeds()
        return {
            "status": "success",
            "message": f"RSS sincronizado: {new_count} artículos",
            "new_articles": new_count,
            "total_articles": len(rss_mgr.articles)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/query")
# @limiter.limit("20/minute")  # Temporarily disabled due to async issues
async def handle_query(request_obj: Request,
                       request: QueryRequest):
    """Endpoint principal para consultas al asistente"""
    try:
        # Validar input
        question = request.get_question()
        if not question:
            return JSONResponse(
                status_code=400,
                content={"error": "Pregunta vacía o no proporcionada"}
            )

        # Validar que no sea demasiado largo
        if len(question) > 1000:
            return JSONResponse(
                status_code=400,
                content={"error": "Pregunta demasiado larga (máx 1000)"}
            )

        # Validar idioma
        if request.language not in ["es", "en"]:
            request.language = "es"

        # Validar paginación
        if request.limit and request.limit < 0:
            request.limit = 5
        if request.offset < 0:
            request.offset = 0

        logger.info(
            f"Query: '{question}' lang={request.language} "
            f"limit={request.limit} offset={request.offset}"
        )

        response_data = orchestrator.process_query(
            question,
            request.language,
            limit=request.limit,
            offset=request.offset,
        )

        logger.info(
            f"Response: agent={response_data.get('agente')} "
            f"total={response_data.get('total_results')}"
        )
        return response_data

    except Exception as e:
        logger.error(f"ERROR en /api/query: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Ocurrió un error interno en el servidor.",
                "details": str(e)
            }
        )


# --- Analytics con buffer ---
analytics_buffer = []
BUFFER_SIZE = 50


def flush_analytics_buffer():
    """Escribe eventos de analytics acumulados"""
    global analytics_buffer
    if not analytics_buffer:
        return

    try:
        analytics_dir = Path("data/analytics")
        analytics_dir.mkdir(parents=True, exist_ok=True)
        analytics_file = analytics_dir / "events.jsonl"

        with open(analytics_file, "a", encoding="utf-8") as f:
            for event_data in analytics_buffer:
                f.write(json.dumps(event_data, ensure_ascii=False) + "\n")

        logger.info(f"Analytics: {len(analytics_buffer)} eventos guardados")
        analytics_buffer = []
    except Exception as e:
        logger.warning(f"Error escribiendo analytics: {e}")


@app.post("/api/analytics")
def track_analytics(event: AnalyticsEvent):
    """Trackea eventos de analytics"""
    try:
        # Validar input
        if not event.event:
            return JSONResponse(
                status_code=400,
                content={"error": "Campo 'event' es obligatorio"}
            )

        # Validar nombre del evento
        allowed_events = [
            "click", "view", "recommend", "error",
            "session_start", "session_end"
        ]
        if event.event not in allowed_events:
            logger.warning(
                f"Evento desconocido: {event.event}"
            )

        event_data = {
            "timestamp": event.timestamp or datetime.utcnow(
            ).isoformat(),
            "event": event.event,
            "data": event.data or {},
            "session_id": event.session_id
        }

        analytics_buffer.append(event_data)

        if len(analytics_buffer) >= BUFFER_SIZE:
            flush_analytics_buffer()

        return {"status": "tracked", "event": event.event}

    except Exception as e:
        logger.warning(f"Error tracking analytics: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


# --- Servir archivos estáticos ---
app.mount("/widget", StaticFiles(directory="widget"), name="widget")
app.mount("/", StaticFiles(directory="frontend", html=True),
          name="static")
