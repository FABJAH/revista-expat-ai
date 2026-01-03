#!/bin/bash
# Script para instalar la nueva dependencia slowapi

echo "🔧 Instalando dependencias de optimización..."
pip install slowapi==0.1.9

echo ""
echo "✅ Instalación completada"
echo ""
echo "📋 Para ejecutar el servidor optimizado:"
echo ""
echo "   Desarrollo:"
echo "   uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "   Producción:"
echo "   export PRODUCTION=true"
echo "   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"
echo ""
echo "🧪 Para validar optimizaciones:"
echo "   python3 test_performance.py"
echo ""
