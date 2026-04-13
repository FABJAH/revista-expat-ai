"""
API Blueprint para el Bot de Inmigración
Proporciona endpoints REST para consultas sobre visados, NIE y documentación
"""

from flask import Blueprint, request, jsonify
from bots.bot_immigration import ImmigrationBot

immigration_api = Blueprint('immigration_api', __name__)


@immigration_api.route('/api/immigration', methods=['POST'])
def handle_immigration_query():
    """
    Endpoint para consultas de inmigración

    Body JSON:
    {
        "message": "¿Qué necesito para vivir en España desde USA?",
        "language": "es"  // opcional: "es" o "en", default "es"
    }

    Response JSON:
    {
        "message": "...",
        "legal_ads": [{"nombre": "...", "contacto": "...", ...}],
        "type": "immigration"
    }
    """
    try:
        if not request.is_json:
            return jsonify({
                "error": "Content-Type debe ser application/json"
            }), 415

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No se proporcionó ningún dato en el cuerpo de la petición"
            }), 400

        message = data.get('message', '').strip()
        language = data.get('language', 'es').lower()

        if not message:
            return jsonify({
                "error": "El campo 'message' es obligatorio y no puede estar vacío"
            }), 400

        if len(message) > 1000:
            return jsonify({
                "error": "El campo 'message' supera el máximo de 1000 caracteres"
            }), 400

        if language not in ['es', 'en']:
            language = 'es'

        # Crear instancia del bot de inmigración
        bot = ImmigrationBot(language=language)

        # Obtener respuesta
        response_text = bot.get_response(message)

        # Preparar respuesta con información adicional
        response = {
            "message": response_text,
            "legal_ads": bot.legal_ads,  # Lista de anunciantes legales de la revista
            "type": "immigration",
            "language": language
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"❌ Error en immigration_api: {e}")
        return jsonify({
            "error": "Error interno del servidor"
        }), 500


@immigration_api.route('/api/immigration/health', methods=['GET'])
def health_check():
    """Health check para verificar que el endpoint está funcionando"""
    try:
        bot = ImmigrationBot('es')
        return jsonify({
            "status": "ok",
            "bot": "ImmigrationBot",
            "legal_ads_loaded": len(bot.legal_ads),
            "countries_supported": len(bot.get_visa_info.__code__.co_consts)  # aproximado
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500
