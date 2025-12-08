# main.py - Nuestro nuevo backend con FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from bots.orchestrator import Orchestrator

# --- Modelo de datos para la validación ---
# Esto asegura que la pregunta siempre será un string.
class QueryRequest(BaseModel):
    question: str
    language: str = "en" # Valor por defecto 'en' si no se recibe

# --- Inicialización ---
app = FastAPI(
    title="Revista Expats AI API",
    description="API para el asistente virtual de la revista para expatriados en Barcelona.",
    version="1.0.0"
)

# Ahora que el frontend y el backend se sirven desde el mismo origen (puerto 8000),
# la configuración de CORS para orígenes externos como el 5500 ya no es necesaria para el desarrollo local.
# La mantenemos por si en el futuro despliegas el frontend y backend en dominios diferentes.
origins = [
    # Ejemplo: "https://www.tufrontend.com"
]

# Configuración de CORS (igual que en Flask, pero con sintaxis de FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Usamos nuestra lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (POST, GET, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

try:
    orchestrator = Orchestrator()
    print("✅ Orquestador inicializado correctamente.")
except Exception as e:
    print(f"❌ ERROR FATAL: No se pudo inicializar el Orquestador. Causa: {e}")
    raise SystemExit("El servidor no puede arrancar sin el Orquestador.")

# --- Endpoint de la API ---
@app.post("/api/query")
def handle_query(request: QueryRequest):
    try:
        print(f"➡️  Petición recibida: '{request.question}' en idioma '{request.language}'")
        # Procesa la pregunta usando el orquestador y devuelve la respuesta
        response_data = orchestrator.process_query(request.question, request.language)
        print(f"⬅️  Respuesta enviada: {response_data}")
        return response_data
    except Exception as e:
        # Si algo sale mal en el orquestador, capturamos el error
        print(f"❌ ERROR en /api/query: {e}")
        # Devolvemos una respuesta de error en formato JSON
        # Esto es crucial para que el frontend no se quede "colgado" esperando
        return JSONResponse(status_code=500, content={"error": "Ocurrió un error interno en el servidor.", "details": str(e)})

# --- Servir archivos estáticos del Frontend ---
# IMPORTANTE: Esto debe ir al final, después de definir todas las rutas de la API.
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
