"""
Backend API para Luna Advertising Sales Bot
Endpoints para servir las respuestas del bot a través del widget
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Optional
import logging
from datetime import datetime
from pathlib import Path

# Importar el bot de ventas
from bots.bot_advertising_sales import AdvertisingSalesBot

logger = logging.getLogger(__name__)

# Planes base para respuestas rápidas del bot de ventas
ADVERTISING_PLANS = {
    "es": {
        "directorio": {
            "nombre": "Directorio",
            "precio": "34€/mes",
            "descripcion": "Listado en el directorio y visibilidad ante 12k+ usuarios/mes",
            "incluye": [
                "Perfil completo con foto y descripción",
                "Analytics de visitas",
                "Soporte por email"
            ]
        },
        "basica": {
            "nombre": "Campaña Básica",
            "precio": "159€/mes",
            "descripcion": "Estrategia inicial de marketing",
            "incluye": ["Plan de medios", "Optimización básica", "Reportes mensuales"]
        },
        "profesional": {
            "nombre": "Campaña Profesional",
            "precio": "199€/mes",
            "descripcion": "La más popular, balance entre alcance y costo",
            "incluye": ["Plan estratégico", "Creatividades", "Gestión y seguimiento"]
        },
        "premium": {
            "nombre": "Campaña Premium",
            "precio": "299€/mes",
            "descripcion": "Máximo impacto con acompañamiento dedicado",
            "incluye": ["Estrategia full-funnel", "Optimización avanzada", "Soporte dedicado"]
        }
    },
    "en": {
        "directorio": {
            "nombre": "Directory",
            "precio": "34€/month",
            "descripcion": "Listed in the directory and visible to 12k+ users/month",
            "incluye": [
                "Full profile with photo and description",
                "Visit analytics",
                "Email support"
            ]
        },
        "basica": {
            "nombre": "Basic Campaign",
            "precio": "159€/month",
            "descripcion": "Initial marketing strategy",
            "incluye": ["Media plan", "Basic optimization", "Monthly reports"]
        },
        "profesional": {
            "nombre": "Professional Campaign",
            "precio": "199€/month",
            "descripcion": "Most popular, balanced reach and cost",
            "incluye": ["Strategic plan", "Creatives", "Management and follow-up"]
        },
        "premium": {
            "nombre": "Premium Campaign",
            "precio": "299€/month",
            "descripcion": "Maximum impact with dedicated support",
            "incluye": ["Full-funnel strategy", "Advanced optimization", "Dedicated support"]
        }
    }
}

# Crear blueprint
advertising_api = Blueprint('advertising_api', __name__, url_prefix='/api/bot')

# ============================================================================
# ENDPOINTS
# ============================================================================

@advertising_api.route('/advertising', methods=['POST'])
def handle_advertising_query():
    """
    Endpoint principal para el widget Luna.

    POST /api/bot/advertising
    {
        "message": str,
        "language": "es" | "en",
        "conversation_id": str (opcional),
        "user_id": str (opcional)
    }

    Returns:
    {
        "type": str,
        "message": str,
        "quick_replies": [...],
        "plans": [...],
        "testimonials": [...]
    }
    """

    try:
        data = request.json

        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing 'message' field"
            }), 400

        message = data.get('message', '').strip()
        language = data.get('language', 'es').lower()
        conversation_id = data.get('conversation_id')
        user_id = data.get('user_id')

        # Validar idioma
        if language not in ['es', 'en']:
            language = 'es'

        if not message:
            return jsonify({
                "error": "Empty message"
            }), 400

        # Obtener respuesta del bot de manera segura
        bot = AdvertisingSalesBot(language)
        bot_reply = bot.get_response(message)

        response = {
            "type": "text",
            "message": bot_reply,
            "quick_replies": [
                {"title": "Ver planes", "payload": "planes"},
                {"title": "Casos de exito", "payload": "testimonials"},
                {"title": "Contactar", "payload": "contact"}
            ],
            "plans": [],
            "testimonials": [],
            "conversation_id": conversation_id,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Log
        log_conversation(
            message=message,
            language=language,
            response_type=response.get('type'),
            conversation_id=conversation_id,
            user_id=user_id
        )

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error en advertising endpoint: {e}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@advertising_api.route('/advertising/plans', methods=['GET'])
def get_plans():
    """
    GET /api/bot/advertising/plans?language=es

    Retorna todos los planes disponibles.
    """

    try:
        language = request.args.get('language', 'es').lower()

        if language not in ['es', 'en']:
            language = 'es'

        plans_data = ADVERTISING_PLANS.get(language, ADVERTISING_PLANS['es'])

        # Convertir a lista
        plans_list = []
        for plan_id, plan_info in plans_data.items():
            plan = plan_info.copy()
            plan['id'] = plan_id
            plans_list.append(plan)

        return jsonify({
            "language": language,
            "plans": plans_list,
            "count": len(plans_list)
        }), 200

    except Exception as e:
        logger.error(f"Error obteniendo planes: {e}")
        return jsonify({"error": str(e)}), 500


@advertising_api.route('/advertising/plans/<plan_id>', methods=['GET'])
def get_plan_detail(plan_id):
    """
    GET /api/bot/advertising/plans/{plan_id}?language=es

    Retorna detalles de un plan específico.
    """

    try:
        language = request.args.get('language', 'es').lower()

        if language not in ['es', 'en']:
            language = 'es'

        plans_data = ADVERTISING_PLANS.get(language, ADVERTISING_PLANS['es'])

        if plan_id not in plans_data:
            return jsonify({"error": "Plan not found"}), 404

        plan = plans_data[plan_id].copy()
        plan['id'] = plan_id
        plan['language'] = language

        return jsonify(plan), 200

    except Exception as e:
        logger.error(f"Error obteniendo detalle de plan: {e}")
        return jsonify({"error": str(e)}), 500


@advertising_api.route('/advertising/inquiry', methods=['POST'])
def create_inquiry():
    """
    POST /api/bot/advertising/inquiry
    {
        "name": str,
        "email": str,
        "business_name": str,
        "phone": str,
        "language": "es" | "en",
        "plan_interested": str (opcional),
        "message": str (opcional)
    }

    Captura información de un cliente interesado.
    """

    try:
        data = request.json or {}

        required_fields = ['name', 'email', 'business_name', 'phone']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400

        language = data.get('language', 'es').lower()
        plan_interested = data.get('plan_interested', 'general')
        message = data.get('message', '')

        bot = AdvertisingSalesBot(language)
        contact = f"{data['name']} | {data['email']} | {data['phone']} | {data['business_name']}"
        inquiry = bot.create_inquiry(contact=contact, plan_type=plan_interested, message=message)

        return jsonify({"success": True, "data": inquiry}), 201

    except Exception as e:
        logger.error(f"Error creando inquiry: {e}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@advertising_api.route('/advertising/greeting', methods=['GET'])
def get_greeting():
    """
    GET /api/bot/advertising/greeting?language=es&time=morning

    Retorna un saludo dinámico.
    """

    try:
        language = request.args.get('language', 'es').lower()
        time_of_day = request.args.get('time', 'morning').lower()

        if language not in ['es', 'en']:
            language = 'es'

        if time_of_day not in ['morning', 'afternoon', 'evening']:
            time_of_day = 'morning'

        bot = AdvertisingSalesBot(language)
        response = bot.get_greeting()

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error obteniendo saludo: {e}")
        return jsonify({"error": str(e)}), 500


@advertising_api.route('/advertising/testimonials', methods=['GET'])
def get_testimonials():
    """
    GET /api/bot/advertising/testimonials?language=es

    Retorna testimonios de clientes.
    """

    try:
        language = request.args.get('language', 'es').lower()

        if language not in ['es', 'en']:
            language = 'es'

        bot = AdvertisingSalesBot(language)
        response = bot.get_testimonials()

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error obteniendo testimonios: {e}")
        return jsonify({"error": str(e)}), 500


@advertising_api.route('/advertising/health', methods=['GET'])
def health_check():
    """
    GET /api/bot/advertising/health

    Health check endpoint.
    """
    return jsonify({
        "status": "healthy",
        "bot": "advertising_sales",
        "timestamp": datetime.utcnow().isoformat()
    }), 200


# ============================================================================
# UTILITIES
# ============================================================================

def log_conversation(message: str, language: str, response_type: str,
                    conversation_id: Optional[str] = None,
                    user_id: Optional[str] = None):
    """
    Registra conversaciones en archivo de log.

    TODO: Integrar con analytics/database
    """

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "message": message,
        "language": language,
        "response_type": response_type,
        "conversation_id": conversation_id,
        "user_id": user_id
    }

    try:
        logs_dir = Path(__file__).parent.parent / 'data' / 'logs'
        logs_dir.mkdir(parents=True, exist_ok=True)

        log_file = logs_dir / 'advertising_conversations.jsonl'

        with open(log_file, 'a', encoding='utf-8') as f:
            import json
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    except Exception as e:
        logger.error(f"Error logging conversation: {e}")


# ============================================================================
# REGISTRO DEL BLUEPRINT
# ============================================================================

def register_advertising_api(app):
    """
    Registrar el blueprint en la aplicación Flask.

    Uso en main.py o app.py:

        from routes.advertising_api import register_advertising_api

        app = Flask(__name__)
        register_advertising_api(app)
    """
    app.register_blueprint(advertising_api)
    logger.info("Advertising API blueprint registrado")
