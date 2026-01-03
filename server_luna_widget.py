#!/usr/bin/env python3
"""
Servidor simple para probar el widget de Luna en landing.html
Incluye endpoints para el bot de publicidad
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import sys
import os
sys.path.insert(0, '/home/fleet/Escritorio/Revista-expats-ai')

from bots.bot_advertising_sales import AdvertisingSalesBot
from config.luna_config import get_all_plans, get_directorio_plans, get_campana_plans

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Permitir requests desde cualquier origen

# Instancias de bots
bots = {
    'es': AdvertisingSalesBot('es'),
    'en': AdvertisingSalesBot('en')
}

@app.route('/api/bot/advertising', methods=['POST'])
def handle_advertising_query():
    """Endpoint principal para consultas al bot de publicidad."""
    try:
        data = request.get_json()
        pregunta = data.get('pregunta', '')
        language = data.get('language', 'es').lower()

        if language not in ['es', 'en']:
            language = 'es'

        # Obtener bot correspondiente
        bot = bots.get(language)

        # Obtener respuesta
        respuesta = bot.get_response(pregunta)

        return jsonify({
            'success': True,
            'respuesta': respuesta,
            'language': language,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bot/advertising/greeting', methods=['GET'])
def get_greeting():
    """Obtener saludo inicial."""
    language = request.args.get('language', 'es')
    bot = bots.get(language, bots['es'])

    return jsonify({
        'success': True,
        'greeting': bot.get_greeting(),
        'language': language
    })

@app.route('/api/bot/advertising/plans', methods=['GET'])
def get_plans():
    """Obtener planes disponibles."""
    language = request.args.get('language', 'es')
    plan_type = request.args.get('type', 'all')  # 'all', 'directorio', 'campana'

    if plan_type == 'directorio':
        planes = {'directorio': get_directorio_plans(language)}
    elif plan_type == 'campana':
        planes = {'campanas': get_campana_plans(language)}
    else:
        planes = get_all_plans(language)

    return jsonify({
        'success': True,
        'planes': planes,
        'language': language
    })

@app.route('/api/bot/advertising/comparison', methods=['GET'])
def get_comparison():
    """Obtener comparación de planes."""
    language = request.args.get('language', 'es')
    bot = bots.get(language, bots['es'])

    return jsonify({
        'success': True,
        'comparison': bot.get_plans_comparison(),
        'language': language
    })

@app.route('/api/bot/advertising/testimonials', methods=['GET'])
def get_testimonials():
    """Obtener testimonios."""
    language = request.args.get('language', 'es')
    bot = bots.get(language, bots['es'])

    return jsonify({
        'success': True,
        'testimonials': bot.get_testimonials(),
        'language': language
    })

@app.route('/api/bot/advertising/inquiry', methods=['POST'])
def create_inquiry():
    """Crear consulta/lead."""
    try:
        data = request.get_json()
        language = data.get('language', 'es')
        contact = data.get('contact', '')
        plan_type = data.get('plan_type', '')
        message = data.get('message', '')

        bot = bots.get(language, bots['es'])
        inquiry = bot.create_inquiry(contact, plan_type, message)

        # Aquí podrías guardar en base de datos
        # Por ahora solo devolvemos confirmación

        return jsonify({
            'success': True,
            'inquiry': inquiry,
            'message': 'Consulta recibida. Te contactaremos pronto.' if language == 'es' else 'Inquiry received. We will contact you soon.'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/bot/advertising/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'Luna Advertising Bot',
        'version': '2.0',
        'bots_available': list(bots.keys())
    })

@app.route('/')
def index():
    """Página de inicio simple."""
    return """
    <html>
    <head>
        <title>Luna Bot API - Running</title>
        <style>
            body { font-family: system-ui; padding: 40px; max-width: 800px; margin: 0 auto; }
            h1 { color: #FF6B6B; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 4px; }
            code { background: #333; color: #fff; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🦉 Luna Bot API v2.0</h1>
        <p>Servidor Flask corriendo. Endpoints disponibles:</p>

        <div class="endpoint">
            <strong>POST</strong> <code>/api/bot/advertising</code><br>
            Body: {"pregunta": "...", "language": "es"}
        </div>

        <div class="endpoint">
            <strong>GET</strong> <code>/api/bot/advertising/greeting</code><br>
            Params: ?language=es
        </div>

        <div class="endpoint">
            <strong>GET</strong> <code>/api/bot/advertising/plans</code><br>
            Params: ?language=es&type=all
        </div>

        <div class="endpoint">
            <strong>GET</strong> <code>/api/bot/advertising/comparison</code><br>
            Params: ?language=es
        </div>

        <div class="endpoint">
            <strong>GET</strong> <code>/api/bot/advertising/testimonials</code><br>
            Params: ?language=es
        </div>

        <div class="endpoint">
            <strong>POST</strong> <code>/api/bot/advertising/inquiry</code><br>
            Body: {"contact": "...", "plan_type": "...", "message": "...", "language": "es"}
        </div>

        <div class="endpoint">
            <strong>GET</strong> <code>/api/bot/advertising/health</code><br>
            Health check
        </div>

        <hr>
        <p><strong>🎯 Para probar el widget:</strong></p>
        <ul>
            <li><a href="/landing.html" target="_blank">Abrir Landing Page con Luna Bot</a></li>
            <li><a href="/widget/luna-demo.html" target="_blank">Demo completo del widget</a></li>
        </ul>
    </body>
    </html>
    """

@app.route('/landing.html')
def serve_landing():
    """Servir landing page."""
    return send_file('landing.html')


if __name__ == '__main__':
    # Puerto por defecto 8000 (se puede cambiar con PORT si ya está en uso)
    port = int(os.environ.get('PORT', '8000'))

    print(f"""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                    🦉 LUNA BOT API - SERVIDOR FLASK                     ║
    ║                     Puerto: {port} (cámbialo con PORT)                     ║
    ╚══════════════════════════════════════════════════════════════════════════╝

    Endpoints disponibles:
    • POST /api/bot/advertising
    • GET  /api/bot/advertising/greeting
    • GET  /api/bot/advertising/plans
    • GET  /api/bot/advertising/comparison
    • GET  /api/bot/advertising/testimonials
    • POST /api/bot/advertising/inquiry
    • GET  /api/bot/advertising/health

    Para probar el widget:
    1. Abre http://127.0.0.1:{port}/landing.html
    2. El widget de Luna aparecerá en la esquina
    3. Interactúa con el bot

    Presiona Ctrl+C para detener el servidor
    """)

    app.run(host='0.0.0.0', port=port, debug=True)
