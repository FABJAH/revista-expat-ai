# main.py - Nuestro nuevo backend con FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Configuración de CORS (igual que en Flask, pero con sintaxis de FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen
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
    # Procesa la pregunta usando el orquestador y devuelve la respuesta
    response = orchestrator.process_query(request.question, request.language)
    return response
