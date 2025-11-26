from orquestador import AgenteOrquestador
from agente_ventas import AgenteVentasPublicitarias
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SistemaCompletoRevista:
    def __init__(self):
        self.orquestador = AgenteOrquestador()
        self.agente_ventas = AgenteVentasPublicitarias()
        logger.info("Sistema Completo de Revista Inicializado")

    def procesar_mensaje(self, mensaje: str) -> dict:
        print(f"\n📨 Usuario dice: {mensaje}")

        # Analizar mensaje
        contexto = self.orquestador.analizar_usuario(mensaje)

        # Ruteo según tipo de usuario
        if contexto.tipo_usuario.value == "anunciante":
            resultado = self.agente_ventas.procesar_consulta(mensaje, contexto)
        else:
            resultado = self.orquestador.route_mensaje(mensaje)

        print(f"\n🤖 Respuesta del agente: {resultado['agente']}")
        print(f"{resultado['respuesta']}")
        return resultado
