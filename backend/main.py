from fastapi import FastAPI
from pydantic import BaseModel
from sistema_principal import SistemaCompletoRevista
from orquestador import base_datos

# Inicializar FastAPI y el sistema de agentes
app = FastAPI(title="BCN Metropolitan Bots API")

# Instanciar el sistema con la base de datos
sistema = SistemaCompletoRevista(base_datos)

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

# Ejemplo de prueba local
if __name__ == "__main__":
    mensaje = "Quiero anunciar mi negocio en la revista"
    respuesta = sistema.procesar_mensaje(mensaje)
    print("\nRespuesta final:", respuesta)
