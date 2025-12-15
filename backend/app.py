# backend/api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from bots.orchestrator import Orchestrator

app = FastAPI(title="Revista Expats AI API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Consulta(BaseModel):
    pregunta: str = None
    question: str = None
    language: str = "es"


orq = Orchestrator()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/consulta")
def consulta(body: Consulta):
    pregunta = body.pregunta or body.question
    result = orq.process_query(pregunta, language=body.language)
    return result


@app.post("/api/query")
def api_query(body: Consulta):
    """Endpoint compatible con el frontend"""
    pregunta = body.pregunta or body.question
    result = orq.process_query(pregunta, language=body.language)
    return result


# Servir archivos estáticos del frontend (DEBE IR AL FINAL)
frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
