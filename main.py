# main.py - Servidor Backend con FastAPI
import json
import os
import threading
import time
from collections import defaultdict
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
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
orchestrator = None
orchestrator_lock = threading.Lock()

MAX_ANALYTICS_DATA_CHARS = 8000
MAX_SESSION_ID_LEN = 128
STRICT_JSON_POST_PATHS = {"/api/query", "/api/analytics"}
METRICS_WINDOW_SIZE = 200
ALERT_ERROR_RATE_PCT = 20.0
ALERT_P95_LATENCY_MS = 1500.0

metrics_lock = threading.Lock()
request_counts = defaultdict(int)
error_counts = defaultdict(int)
latency_samples = defaultdict(lambda: deque(maxlen=METRICS_WINDOW_SIZE))
query_agent_counts = defaultdict(int)


def sync_rss_feeds():
    """Tarea para sincronizar feeds RSS cada 6 horas"""
    try:
        rss_mgr = get_rss_manager()
        new_count = rss_mgr.sync_feeds()
        logger.info(f"RSS Sync completado: {new_count} artículos nuevos")
    except Exception as e:
        logger.error(f"Error sincronizando RSS: {e}")


def has_json_content_type(request: Request) -> bool:
    """Valida Content-Type JSON (acepta parámetros como charset)."""
    content_type = request.headers.get("content-type", "")
    return content_type.split(";")[0].strip().lower() == "application/json"


def get_orchestrator() -> Orchestrator:
    """Inicializa el orquestador una sola vez de forma thread-safe."""
    global orchestrator
    if orchestrator is not None:
        return orchestrator

    with orchestrator_lock:
        if orchestrator is None:
            orchestrator = Orchestrator()
            logger.info("Orquestador inicializado correctamente.")
    return orchestrator


def get_metrics_snapshot() -> dict:
    """Genera una fotografía consistente de las métricas en memoria."""
    with metrics_lock:
        endpoints = set(request_counts.keys())
        endpoints.update(error_counts.keys())
        endpoints.update(latency_samples.keys())

        by_endpoint = {}
        for endpoint in sorted(endpoints):
            samples = list(latency_samples.get(endpoint, []))
            avg_latency = (
                round(sum(samples) / len(samples), 2) if samples else 0.0
            )
            p95_latency = 0.0
            if samples:
                ordered = sorted(samples)
                idx = int(0.95 * (len(ordered) - 1))
                p95_latency = round(ordered[idx], 2)

            total_requests = request_counts.get(endpoint, 0)
            total_errors = error_counts.get(endpoint, 0)
            error_rate = (
                round((total_errors / total_requests) * 100, 2)
                if total_requests else 0.0
            )

            by_endpoint[endpoint] = {
                "requests": total_requests,
                "errors": total_errors,
                "error_rate_pct": error_rate,
                "latency_avg_ms": avg_latency,
                "latency_p95_ms": p95_latency,
                "samples": len(samples),
            }

        top_query_agents = dict(
            sorted(
                query_agent_counts.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )

        return {
            "window_size": METRICS_WINDOW_SIZE,
            "endpoints": by_endpoint,
            "tracked_endpoints": len(by_endpoint),
            "query_agents": top_query_agents,
        }


def build_metric_alerts(metrics: dict) -> list[dict]:
    """Genera alertas simples basadas en umbrales de error y latencia."""
    alerts = []
    for endpoint, values in metrics.get("endpoints", {}).items():
        if values.get("requests", 0) < 5:
            continue

        if values.get("error_rate_pct", 0.0) >= ALERT_ERROR_RATE_PCT:
            alerts.append({
                "type": "error_rate",
                "severity": "high",
                "endpoint": endpoint,
                "value": values.get("error_rate_pct", 0.0),
                "threshold": ALERT_ERROR_RATE_PCT,
                "message": (
                    f"Error rate alto en {endpoint}: "
                    f"{values.get('error_rate_pct', 0.0)}%"
                ),
            })

        if values.get("latency_p95_ms", 0.0) >= ALERT_P95_LATENCY_MS:
            alerts.append({
                "type": "latency_p95",
                "severity": "medium",
                "endpoint": endpoint,
                "value": values.get("latency_p95_ms", 0.0),
                "threshold": ALERT_P95_LATENCY_MS,
                "message": (
                    f"Latencia p95 alta en {endpoint}: "
                    f"{values.get('latency_p95_ms', 0.0)} ms"
                ),
            })

    return alerts


def build_prometheus_metrics(metrics: dict) -> str:
    """Convierte métricas internas al formato de texto Prometheus."""
    lines = [
        "# HELP revista_api_requests_total Total requests by endpoint",
        "# TYPE revista_api_requests_total counter",
    ]

    for endpoint, values in metrics.get("endpoints", {}).items():
        safe_endpoint = endpoint.replace('"', "\\\"")
        lines.append(
            f'revista_api_requests_total{{endpoint="{safe_endpoint}"}} '
            f'{values.get("requests", 0)}'
        )

    lines.extend([
        "# HELP revista_api_errors_total Total error responses by endpoint",
        "# TYPE revista_api_errors_total counter",
    ])
    for endpoint, values in metrics.get("endpoints", {}).items():
        safe_endpoint = endpoint.replace('"', "\\\"")
        lines.append(
            f'revista_api_errors_total{{endpoint="{safe_endpoint}"}} '
            f'{values.get("errors", 0)}'
        )

    lines.extend([
        "# HELP revista_api_latency_avg_ms Average API latency in ms",
        "# TYPE revista_api_latency_avg_ms gauge",
    ])
    for endpoint, values in metrics.get("endpoints", {}).items():
        safe_endpoint = endpoint.replace('"', "\\\"")
        lines.append(
            f'revista_api_latency_avg_ms{{endpoint="{safe_endpoint}"}} '
            f'{values.get("latency_avg_ms", 0.0)}'
        )

    lines.extend([
        "# HELP revista_query_agent_total Query count by resolved agent",
        "# TYPE revista_query_agent_total counter",
    ])
    for agent, count in metrics.get("query_agents", {}).items():
        safe_agent = str(agent).replace('"', "\\\"")
        lines.append(
            f'revista_query_agent_total{{agent="{safe_agent}"}} {count}'
        )

    return "\n".join(lines) + "\n"


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


@app.middleware("http")
async def enforce_json_post_content_type(request: Request, call_next):
    """Aplica Content-Type JSON a rutas POST críticas antes del parseo."""
    if (
        request.method == "POST"
        and request.url.path in STRICT_JSON_POST_PATHS
        and not has_json_content_type(request)
    ):
        return JSONResponse(
            status_code=415,
            content={"error": "Content-Type debe ser application/json"}
        )
    return await call_next(request)


@app.middleware("http")
async def collect_api_metrics(request: Request, call_next):
    """Recolecta métricas de latencia/errores para endpoints API."""
    path = request.url.path
    start = time.perf_counter()
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception:
        # Re-raise para mantener comportamiento actual de error handling.
        raise
    finally:
        if path.startswith("/api/") and not path.startswith("/api/metrics"):
            elapsed_ms = (time.perf_counter() - start) * 1000
            with metrics_lock:
                request_counts[path] += 1
                if status_code >= 400:
                    error_counts[path] += 1
                latency_samples[path].append(elapsed_ms)

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

# --- Endpoints de la API ---


@app.get("/api/health")
def health_check():
    """Verifica que el servidor está funcionando"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "Revista Expats AI API"
    }


@app.get("/api/metrics")
def get_metrics():
    """Expone métricas simples de latencia/errores por endpoint API."""
    metrics = get_metrics_snapshot()
    return {
        "status": "ok",
        "generated_at": datetime.utcnow().isoformat(),
        "metrics": metrics,
        "alerts": build_metric_alerts(metrics),
    }


@app.get("/api/metrics/prometheus")
def get_prometheus_metrics():
    """Expone métricas en formato Prometheus text exposition."""
    metrics = get_metrics_snapshot()
    return PlainTextResponse(
        content=build_prometheus_metrics(metrics),
        media_type="text/plain; version=0.0.4",
    )


@app.get("/dashboard")
def get_dashboard():
    """Sirve el dashboard HTML para visualizar métricas en tiempo real."""
    dashboard_path = Path(__file__).parent / "dashboard.html"
    if not dashboard_path.exists():
        return JSONResponse(
            status_code=404,
            content={"error": "Dashboard no encontrado"}
        )

    with open(dashboard_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    return PlainTextResponse(content=html_content, media_type="text/html")


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
        logger.error(f"Error en /api/sync-rss: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "Ocurrió un error interno en el servidor."}
        )


@app.post("/api/query")
@limiter.limit("20/minute")
async def handle_query(request: Request,
                       query: QueryRequest):
    """Endpoint principal para consultas al asistente"""
    try:
        # Validar input
        question = query.get_question().strip()
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
        if query.language not in ["es", "en"]:
            query.language = "es"

        # Validar paginación
        if query.limit is None or query.limit <= 0:
            query.limit = 5
        if query.limit > 20:
            query.limit = 20
        if query.offset < 0:
            query.offset = 0
        if query.offset > 1000:
            query.offset = 1000

        logger.info(
            f"Query: '{question}' lang={query.language} "
            f"limit={query.limit} offset={query.offset}"
        )

        response_data = get_orchestrator().process_query(
            question,
            query.language,
            limit=query.limit,
            offset=query.offset,
        )

        logger.info(
            f"Response: agent={response_data.get('agente')} "
            f"total={response_data.get('total_results')}"
        )

        with metrics_lock:
            agent_name = response_data.get("agente") or "unknown"
            query_agent_counts[str(agent_name)] += 1

        return response_data

    except ValueError as e:
        logger.warning(f"Validación fallida en /api/query: {e}")
        return JSONResponse(
            status_code=400,
            content={"error": "Solicitud inválida"}
        )
    except TimeoutError as e:
        logger.error(f"Timeout en /api/query: {e}", exc_info=True)
        return JSONResponse(
            status_code=504,
            content={"error": "Tiempo de espera agotado"}
        )
    except RuntimeError as e:
        logger.error(f"Error operativo en /api/query: {e}", exc_info=True)
        return JSONResponse(
            status_code=503,
            content={"error": "Servicio temporalmente no disponible"}
        )
    except Exception as e:
        logger.error(f"ERROR en /api/query: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Ocurrió un error interno en el servidor."
            }
        )


# --- Analytics con buffer ---
analytics_buffer = []
analytics_lock = threading.Lock()
BUFFER_SIZE = 50


def flush_analytics_buffer():
    """Escribe eventos de analytics acumulados"""
    global analytics_buffer
    with analytics_lock:
        if not analytics_buffer:
            return
        events_to_flush = analytics_buffer
        analytics_buffer = []

    try:
        analytics_dir = Path("data/analytics")
        analytics_dir.mkdir(parents=True, exist_ok=True)
        analytics_file = analytics_dir / "events.jsonl"

        with open(analytics_file, "a", encoding="utf-8") as f:
            for event_data in events_to_flush:
                f.write(json.dumps(event_data, ensure_ascii=False) + "\n")

        logger.info(f"Analytics: {len(events_to_flush)} eventos guardados")
    except Exception as e:
        logger.warning(f"Error escribiendo analytics: {e}")


@app.post("/api/analytics")
def track_analytics(request_obj: Request, event: AnalyticsEvent):
    """Trackea eventos de analytics"""
    try:
        if not has_json_content_type(request_obj):
            return JSONResponse(
                status_code=415,
                content={"error": "Content-Type debe ser application/json"}
            )

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

        if event.session_id and len(event.session_id) > MAX_SESSION_ID_LEN:
            return JSONResponse(
                status_code=400,
                content={"error": "session_id excede el tamaño permitido"}
            )

        data_payload = event.data or {}
        data_payload_str = json.dumps(data_payload, ensure_ascii=False)
        if len(data_payload_str) > MAX_ANALYTICS_DATA_CHARS:
            return JSONResponse(
                status_code=413,
                content={"error": "Payload de analytics demasiado grande"}
            )

        event_data = {
            "timestamp": event.timestamp or datetime.utcnow(
            ).isoformat(),
            "event": event.event,
            "data": data_payload,
            "session_id": event.session_id
        }

        should_flush = False
        with analytics_lock:
            analytics_buffer.append(event_data)
            if len(analytics_buffer) >= BUFFER_SIZE:
                should_flush = True

        if should_flush:
            flush_analytics_buffer()

        return {"status": "tracked", "event": event.event}

    except Exception as e:
        logger.error(f"Error tracking analytics: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Error interno del servidor"
            }
        )


# --- Servir archivos estáticos ---
app.mount("/widget", StaticFiles(directory="widget"), name="widget")
app.mount("/", StaticFiles(directory="frontend", html=True),
          name="static")


# --- Iniciar servidor ---
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")

    logger.info(f"Iniciando servidor en {host}:{port}")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
