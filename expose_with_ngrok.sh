#!/bin/bash
# Script para exponer la aplicación con ngrok
# Uso: ./expose_with_ngrok.sh

echo "🌐 Exponiendo Revista Expats AI con ngrok..."

# Verificar si ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok no está instalado."
    echo "Instala con: snap install ngrok"
    echo "O descarga de: https://ngrok.com/download"
    exit 1
fi

# Verificar si hay token configurado
if ! ngrok config list | grep -q "authtoken"; then
    echo "⚠️  ngrok no está configurado."
    echo "1. Regístrate en: https://ngrok.com"
    echo "2. Obtén tu token gratis"
    echo "3. Configura: ngrok config add-authtoken TU_TOKEN"
    exit 1
fi

echo "✅ ngrok configurado"

# Verificar que el servidor esté corriendo
if ! curl -s http://127.0.0.1:8000/api/health > /dev/null; then
    echo "❌ El servidor no está corriendo."
    echo "Ejecuta primero: ./start_server.sh"
    exit 1
fi

echo "✅ Servidor corriendo"

# Iniciar ngrok
echo "🚀 Iniciando ngrok..."
echo "Tu aplicación estará disponible en la URL que ngrok te muestre"
echo "Comparte esa URL con las personas que quieran probar"
echo ""
echo "Presiona Ctrl+C para detener"
echo ""

ngrok http 8000