# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from bots.orchestrator import Orchestrator

app = FastAPI(title="BCN Metropolitan Bots API")

# CORS para que tu frontend pueda llamar a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajusta a tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciar el orquestador con datos
orchestrator = Orchestrator()

class Consulta(BaseModel):
    pregunta: str
    language: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "message": "BCN Metropolitan Bots API funcionando"}

@app.post("/consulta")
def consulta(body: Consulta):
    result = orchestrator.process_query(body.pregunta)
    # Agregar el idioma solicitado si quieres afectar el texto; por ahora devolvemos tal cual
    return result
