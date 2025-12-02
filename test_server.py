from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

@app.route('/test', methods=['GET'])
def test_connection():
    return jsonify({"message": "¡Conexión exitosa con el servidor de prueba!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
