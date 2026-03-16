#!/bin/bash
# Script para instalar el servicio systemd
# Uso: sudo ./install_service.sh

echo "🔧 Instalando servicio Revista Expats AI..."

# Copiar archivo de servicio
sudo cp revista-expats.service /etc/systemd/system/

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar el servicio
sudo systemctl enable revista-expats

# Iniciar el servicio
sudo systemctl start revista-expats

# Verificar estado
echo "📊 Estado del servicio:"
sudo systemctl status revista-expats --no-pager

echo ""
echo "✅ Servicio instalado!"
echo "📱 Tu aplicación estará disponible en: http://tu-ip-local:8000"
echo "🌐 Para acceso remoto, configura port forwarding en tu router"
echo ""
echo "Comandos útiles:"
echo "  Ver logs: sudo journalctl -u revista-expats -f"
echo "  Reiniciar: sudo systemctl restart revista-expats"
echo "  Detener: sudo systemctl stop revista-expats"
