# main.py - Nuestro nuevo backend con FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from bots.orchestrator import Orchestrator

# --- Modelos de datos para la validación ---
class QueryRequest(BaseModel):
    pregunta: str = None  # Para compatibilidad con frontend español
    question: str = None  # Para compatibilidad con frontend inglés
    language: str = "es"  # Valor por defecto 'es'
    session_id: str = None  # ID de sesión para tracking

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
    description="API para el asistente virtual de la revista para expatriados en Barcelona.",
    version="1.0.0"
)

# Configuración de CORS para integración profesional
origins = [
    "https://www.barcelona-metropolitan.com",
    "https://barcelona-metropolitan.com",
    "http://localhost:5500",  # Para desarrollo local
    "http://localhost:3000",  # Para desarrollo local
    "http://127.0.0.1:5500",
    "http://127.0.0.1:3000",
]

# Configuración de CORS (igual que en Flask, pero con sintaxis de FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes en desarrollo, restringir en producción
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Métodos específicos necesarios
    allow_headers=["*"],  # Permite todas las cabeceras
)

try:
    orchestrator = Orchestrator()
    print("✅ Orquestador inicializado correctamente.")
except Exception as e:
    print(f"❌ ERROR FATAL: No se pudo inicializar el Orquestador. Causa: {e}")
    raise SystemExit("El servidor no puede arrancar sin el Orquestador.")

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

@app.post("/api/query")
def handle_query(request: QueryRequest):
    """Endpoint principal para consultas al asistente"""
    try:
        # Obtener la pregunta desde el request (compatible con pregunta/question)
        question = request.get_question()
        if not question:
            return JSONResponse(
                status_code=400,
                content={"error": "Pregunta vacía o no proporcionada"}
            )

        print(f"➡️  Petición recibida: '{question}' en idioma '{request.language}'")

        # Procesa la pregunta usando el orquestador y devuelve la respuesta
        response_data = orchestrator.process_query(question, request.language)

        print(f"⬅️  Respuesta enviada: {response_data.get('categoria', 'N/A')}")
        return response_data

    except Exception as e:
        # Si algo sale mal en el orquestador, capturamos el error
        print(f"❌ ERROR en /api/query: {e}")
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

@app.post("/api/analytics")
def track_analytics(event: AnalyticsEvent):
    """Endpoint para tracking de eventos de analytics"""
    try:
        import json
        from datetime import datetime
        from pathlib import Path

        # Crear directorio de analytics si no existe
        analytics_dir = Path("data/analytics")
        analytics_dir.mkdir(parents=True, exist_ok=True)

        # Guardar evento en archivo JSONL
        analytics_file = analytics_dir / "events.jsonl"

        event_data = {
            "timestamp": event.timestamp or datetime.utcnow().isoformat(),
            "event": event.event,
            "data": event.data,
            "session_id": event.session_id
        }

        with open(analytics_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event_data, ensure_ascii=False) + "\n")

        return {"status": "tracked", "event": event.event}

    except Exception as e:
        print(f"⚠️ Error tracking analytics: {e}")
        # No fallar el request por errores de analytics
        return {"status": "error", "message": str(e)}

# --- Servir archivos estáticos del Frontend y Widget ---
# IMPORTANTE: Esto debe ir al final, después de definir todas las rutas de la API.

# Servir el widget
app.mount("/widget", StaticFiles(directory="widget"), name="widget")

# Servir el frontend principal
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
