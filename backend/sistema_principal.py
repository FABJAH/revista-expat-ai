import logging
from bots.orquestador import Orchestrator

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SistemaCompletoRevista:
    def __init__(self, base_datos):
        # Instanciamos el nuevo orquestador
        self.orquestador = Orchestrator()
        logger.info("✅ Sistema Completo de Revista Inicializado con Nuevo Orchestrator")

    def procesar_mensaje(self, mensaje: str) -> dict:
        print(f"\n📨 Usuario dice: {mensaje}")

        # Usar el nuevo orquestador que ya clasifica y responde
        resultado = self.orquestador.process_query(mensaje)

        # Mostrar respuesta en consola
        print(f"\n🤖 Respuesta del agente: {resultado.get('agente')}")
        print(f"📊 Confianza: {resultado.get('confidence')}")
        print(f"{resultado.get('respuesta')}")
        return resultado
