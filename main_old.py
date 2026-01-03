# main.py - Nuestro nuevo backend con FastAPI
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from bots.orchestrator import Orchestrator
from bots.rss_manager import get_rss_manager
from bots.logger import logger

# --- Configurar scheduler en background ---
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def sync_rss_feeds():
    """Tarea para sincronizar feeds RSS cada 6 horas"""
    try:
        rss_mgr = get_rss_manager()
        new_count = rss_mgr.sync_feeds()
        logger.info(f"RSS Sync completado: {new_count} artículos nuevos")
    except Exception as e:
        logger.error(f"Error sincronizando RSS: {e}")


# Lifecycle de FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: sincronizar feeds al iniciar y programar tarea de background
    logger.info("Iniciando servidor...")
    rss_mgr = get_rss_manager()

    # OPTIMIZACIÓN: Sync inicial en background para no bloquear startup
    import threading

    def initial_sync():
        try:
            logger.info("Sincronizando RSS feeds en background...")
            rss_mgr.sync_feeds()
            logger.info("Sincronización inicial RSS completada")
        except Exception as e:
            logger.error(f"Error en sync inicial RSS: {e}")

    # Lanzar sync en thread separado
    threading.Thread(target=initial_sync, daemon=True).start()

    scheduler.add_job(sync_rss_feeds, 'interval', hours=6)
    scheduler.start()
    logger.info("Scheduler iniciado: feeds sincronizarán cada 6 horas")

    yield

    # Shutdown: detener scheduler
    scheduler.shutdown()

    # OPTIMIZACIÓN: Flush del buffer de analytics antes de cerrar
    flush_analytics_buffer()

    logger.info("Servidor detenido correctamente")

# --- Modelos de datos para la validación ---


class QueryRequest(BaseModel):
    pregunta: str = None  # Para compatibilidad con frontend español
    question: str = None  # Para compatibilidad con frontend inglés
    language: str = "es"  # Valor por defecto 'es'
    session_id: str = None  # ID de sesión para tracking
    # Número de resultados por página (0 o None = todos)
    limit: int | None = 5
    # Desplazamiento para paginación
    offset: int = 0

    def get_question(self):
        """Retorna la pregunta, priorizando 'pregunta' sobre 'question'"""
        return self.pregunta or self.question or ""


class AnalyticsEvent(BaseModel):
    event: str
    data: dict = {}
    session_id: str = None
    timestamp: str = None


# --- Inicialización ---
app = FastAPI(
    title="Revista Expats AI API",
    description=(
        "API para el asistente virtual de la revista "
        "para expatriados en Barcelona."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# OPTIMIZACIÓN: GZip para comprimir respuestas JSON grandes
app.add_middleware(GZipMiddleware, minimum_size=1000)

# OPTIMIZACIÓN: Rate Limiting para evitar abuso
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configuración de CORS (OPTIMIZADO: Restringido en producción)
production_mode = os.getenv("PRODUCTION", "false").lower() == "true"

if production_mode:
    # Producción: Solo dominios específicos
    allowed_origins = [
        "https://www.barcelona-metropolitan.com",
        "https://barcelona-metropolitan.com",
    ]
else:
    # Desarrollo: Permitir localhost
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

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
    """Health check endpoint para verificar que el servidor está funcionando"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Revista Expats AI API"
    }


@app.get("/api/categories")
def get_categories():
    """Retorna las categorías disponibles de los bots"""
    return {
        "categories": [
            {"id": "accommodation", "name": "Alojamiento", "icon": "🏠"},
            {"id": "legal", "name": "Legal", "icon": "⚖️"},
            {"id": "healthcare", "name": "Salud", "icon": "🏥"},
            {"id": "education", "name": "Educación", "icon": "🎓"},
            {"id": "restaurants", "name": "Restaurantes", "icon": "🍽️"},
            {"id": "social", "name": "Social", "icon": "👥"},
            {"id": "work", "name": "Trabajo", "icon": "💼"},
            {"id": "service", "name": "Servicios", "icon": "🔧"},
            {"id": "comercial", "name": "Comercial", "icon": "🛍️"}
        ]
    }
@app.get("/api/sync-rss")
def manual_sync_rss():
    """Endpoint para sincronizar feeds RSS manualmente"""
    try:
        rss_mgr = get_rss_manager()
        new_count = rss_mgr.sync_feeds()
        return {
            "status": "success",
            "message": f"RSS sincronizado: {new_count} artículos nuevos",
            "new_articles": new_count,
            "total_articles": len(rss_mgr.articles)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/query")
@limiter.limit("20/minute")
async def handle_query(request_obj: Request, request: QueryRequest):
    """Endpoint principal para consultas al asistente (OPTIMIZADO: rate limited)"""
    try:
        # Obtener la pregunta desde el request (compatible con pregunta/question)
        question = request.get_question()
        if not question:
            return JSONResponse(
                status_code=400,
                content={"error": "Pregunta vacía o no proporcionada"}
            )

        logger.info(
            f"Query: '{question}' lang={request.language} "
            f"limit={request.limit} offset={request.offset}"
        )

        # Procesa la pregunta usando el orquestador y devuelve la respuesta
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
        # Si algo sale mal en el orquestador, capturamos el error
        logger.error(f"ERROR en /api/query: {e}")
        import traceback
        traceback.print_exc()
        # Devolvemos una respuesta de error en formato JSON
        return JSONResponse(
            status_code=500,
            content={
                "error": "Ocurrió un error interno en el servidor.",
                "details": str(e)
            }
        )

# OPTIMIZACIÓN: Buffer de analytics para reducir I/O de disco
analytics_buffer = []
BUFFER_SIZE = 50


def flush_analytics_buffer():
    """Escribe eventos de analytics acumulados en disco"""
    global analytics_buffer
    if not analytics_buffer:
        return

    try:
        from pathlib import Path
        import json
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
    """Tracking de eventos de analytics (OPTIMIZADO: con buffer)"""
    try:
        from datetime import datetime

        event_data = {
            "timestamp": event.timestamp or datetime.utcnow().isoformat(),
            "event": event.event,
            "data": event.data,
            "session_id": event.session_id
        }

        # OPTIMIZACIÓN: Agregar a buffer en lugar de escribir inmediatamente
        analytics_buffer.append(event_data)

        # Flush si el buffer está lleno
        if len(analytics_buffer) >= BUFFER_SIZE:
            flush_analytics_buffer()

        return {"status": "tracked", "event": event.event}

    except Exception as e:
        logger.warning(f"Error tracking analytics: {e}")
        # No fallar el request por errores de analytics
        return {"status": "error", "message": str(e)}

# --- Servir archivos estáticos del Frontend y Widget ---
# IMPORTANTE: Esto debe ir al final, después de definir todas las rutas de la API.

# Servir el widget
app.mount("/widget", StaticFiles(directory="widget"), name="widget")

# Servir el frontend principal
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
