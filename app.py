from flask import Flask, request, jsonify
from backend.orquestador import procesar_pregunta  # usa tu función existente

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Barcelona Metropolitan Bots OK"

@app.route("/consulta", methods=["POST"])
def consulta():
    data = request.get_json()
    pregunta = data.get("pregunta", "").strip()
    if not pregunta:
        return jsonify({"error": "Falta 'pregunta'"}), 400

    categoria, resultados = procesar_pregunta(pregunta)
    return jsonify({
        "categoria": categoria,
        "resultados": resultados
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
