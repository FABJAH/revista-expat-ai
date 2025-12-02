# backend/api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
    pregunta: str
    language: str = "es"


orq = Orchestrator()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/consulta")
def consulta(body: Consulta):
    result = orq.process_query(body.pregunta, language=body.language)
    return result
