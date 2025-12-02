from flask import Flask, request, jsonify
from flask_cors import CORS
from bots.orchestrator import Orchestrator

# Inicializa la aplicación Flask
app = Flask(__name__)
# Habilita CORS para permitir que el frontend (desde cualquier origen) se comunique con esta API.
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Crea una única instancia del Orchestrator para que la base de datos
# se cargue solo una vez al iniciar el servidor.
try:
    orchestrator = Orchestrator()
    print("✅ Orquestador inicializado correctamente.")
except Exception as e:
    print("===================================================")
    print(f"❌ ERROR FATAL: No se pudo inicializar el Orquestador.")
    print(f"Causa: {e}")
    raise SystemExit("El servidor no puede arrancar sin el Orquestador. Revisa el error de arriba.")

@app.route('/api/query', methods=['POST'])
def handle_query():
    if not orchestrator:
        return jsonify({"error": "El servidor no está configurado correctamente."}), 500

    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "La pregunta no puede estar vacía."}), 400

    # Procesa la pregunta usando el orquestador y devuelve la respuesta
    response = orchestrator.process_query(question)
    return jsonify(response)

if __name__ == '__main__':
    # Ejecuta la aplicación en modo de depuración para facilitar el desarrollo
    app.run(debug=True, port=5000)
