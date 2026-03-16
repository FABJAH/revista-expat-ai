#!/bin/bash
# Script de verificación antes del despliegue
# Uso: ./check_deployment.sh

echo "🔍 Verificando Revista Expats AI para despliegue..."

# Verificar entorno virtual
echo "📦 Verificando entorno virtual..."
if [ ! -d ".venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecuta: python3 -m venv .venv"
    exit 1
fi

# Activar entorno virtual
source .venv/bin/activate

# Verificar dependencias
echo "📚 Verificando dependencias..."
python3 -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependencias faltantes. Ejecuta: pip install -r requirements.txt"
    exit 1
fi

# Verificar archivos críticos
echo "📁 Verificando archivos..."
files=("main.py" "frontend/index.html" "frontend/script.js" "frontend/styles.css")
for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Archivo faltante: $file"
        exit 1
    fi
done

# Verificar que el servidor puede iniciar
echo "🚀 Probando inicio del servidor..."
timeout 10s python3 -m uvicorn main:app --host 127.0.0.1 --port 8001 > server_test.log 2>&1 &
SERVER_PID=$!

sleep 3

# Verificar que responde
if curl -s http://127.0.0.1:8001/api/health > /dev/null; then
    echo "✅ Servidor responde correctamente"
else
    echo "❌ Servidor no responde"
    cat server_test.log
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Detener servidor de prueba
kill $SERVER_PID 2>/dev/null
rm -f server_test.log

echo ""
echo "🎉 ¡Todo listo para el despliegue!"
echo ""
echo "Opciones disponibles:"
echo "  🌐 Ngrok: ./expose_with_ngrok.sh"
echo "  🚂 Railway: Sube a GitHub y conecta"
echo "  🖥️ Local 24/7: sudo ./install_service.sh"
echo ""
echo "Lee DEPLOYMENT.md para más detalles"
