#!/bin/bash
# Script para iniciar el servidor y abrir el test del bot de inmigración

echo "🌍 Iniciando servidor de Revista Expats AI..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py no encontrado"
    echo "Ejecuta este script desde el directorio del proyecto"
    exit 1
fi

# Iniciar servidor
echo "📡 Iniciando Flask en puerto 8000..."
python3 app.py &
SERVER_PID=$!

# Esperar a que el servidor arranque
sleep 3

# Verificar que el servidor está corriendo
if curl -s http://127.0.0.1:8000/api/immigration/health > /dev/null 2>&1; then
    echo "✅ Servidor iniciado correctamente"
    echo ""
    echo "📋 Endpoints disponibles:"
    echo "  - http://127.0.0.1:8000/ (landing page principal)"
    echo "  - http://127.0.0.1:8000/api/immigration (bot de inmigración)"
    echo "  - http://127.0.0.1:8000/api/bot/advertising (Luna - bot publicidad)"
    echo "  - http://127.0.0.1:8000/api/query (orquestador general)"
    echo ""
    echo "🧪 Páginas de prueba:"
    echo "  - test_immigration.html (prueba bot inmigración)"
    echo "  - landing.html (página principal con dos caminos)"
    echo ""
    echo "Abre test_immigration.html en tu navegador para probar"
    echo ""
    echo "Para detener el servidor: kill $SERVER_PID"
    echo "O presiona Ctrl+C"
    echo ""

    # Abrir navegador si está disponible
    if command -v xdg-open > /dev/null 2>&1; then
        echo "🌐 Abriendo test en navegador..."
        xdg-open "$(pwd)/test_immigration.html" 2>/dev/null &
    fi

    # Mantener el script vivo
    wait $SERVER_PID
else
    echo "❌ Error: No se pudo iniciar el servidor"
    echo "Revisa los logs para más detalles"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi
