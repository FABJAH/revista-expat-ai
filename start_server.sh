#!/bin/bash
# Script para iniciar Revista Expats AI
# Uso: ./start_server.sh

echo "🚀 Iniciando Revista Expats AI..."

# Cambiar al directorio del proyecto
cd "$(dirname "$0")"

# Activar entorno virtual
source .venv/bin/activate

# Verificar que las dependencias estén instaladas
echo "📦 Verificando dependencias..."
python -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependencias faltantes. Ejecuta: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Dependencias OK"

# Iniciar servidor
echo "🌐 Iniciando servidor en http://127.0.0.1:8000"
echo "📱 Abre tu navegador y ve a: http://127.0.0.1:8000"
echo "🛑 Presiona Ctrl+C para detener el servidor"
echo ""

uvicorn main:app --reload --port 8000
