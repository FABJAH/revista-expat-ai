from fastapi import FastAPI
from pydantic import BaseModel
from sistema_principal import SistemaCompletoRevista

# Inicializar FastAPI y el sistema de agentes
app = FastAPI(title="BCN Metropolitan Bots API")
sistema = SistemaCompletoRevista()

# Modelo de entrada para la consulta
class Consulta(BaseModel):
    pregunta: str

# Endpoint principal para recibir preguntas
@app.post("/consulta")
async def consulta_usuario(body: Consulta):
    resultado = sistema.procesar_mensaje(body.pregunta)
    return resultado

# Endpoint de prueba para verificar que el servidor está activo
@app.get("/health")
async def health():
    return {"status": "ok", "message": "BCN Metropolitan Bots API funcionando"}
