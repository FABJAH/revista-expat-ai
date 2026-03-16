# 🚀 Despliegue - Revista Expats AI

## 🎯 Objetivo
Permitir que cualquier persona acceda a la aplicación 24/7 sin necesidad de que el servidor local esté siempre corriendo.

## ✅ Cambios Recientes
- **AGREGADO:** Dependencias de ML completas (PyTorch, sentence-transformers) para clasificación semántica avanzada
- **RESTAURADO:** Clasificación inteligente con embeddings para máxima precisión
- **REQUIERE:** Servidor con recursos suficientes para ML

## 📋 Opciones de Despliegue

### 1. 🌐 Ngrok (Para testing rápido - Gratis con límites)
**Ventajas:**
- ✅ Fácil de usar para pruebas
- ✅ Sin registro complicado
- ✅ URL temporal para compartir

**Limitaciones:**
- ❌ URL temporal (cambia cada reinicio)
- ❌ Límite de 8 horas/día
- ❌ No apto para producción

**Pasos:**
```bash
# Instalar
snap install ngrok

# Configurar (obtén token gratis en ngrok.com)
ngrok config add-authtoken TU_TOKEN

# Ejecutar
./expose_with_ngrok.sh
```

### 2. 🖥️ VPS/Cloud Server (Para producción completa)
**Opciones recomendadas:**
- **DigitalOcean** ($6/mes) - Fácil para principiantes
- **Linode** ($5/mes) - Buen rendimiento
- **AWS Lightsail** ($3.50/mes) - Escalable
- **Google Cloud Run** (pago por uso) - Serverless

**Requisitos del servidor:**
- Ubuntu 20.04+ o similar
- 2GB RAM mínimo (4GB recomendado para ML)
- Python 3.11+
- Conexión SSH

**Pasos de despliegue:**
```bash
# 1. Conectar al servidor
ssh user@tu-servidor

# 2. Instalar dependencias del sistema
sudo apt update
sudo apt install python3 python3-pip git

# 3. Clonar el proyecto
git clone https://github.com/FABJAH/revista-expat-ai.git
cd revista-expat-ai

# 4. Instalar dependencias Python
pip install -r requirements.txt

# 5. Configurar variables de entorno
cp .env.example .env
nano .env  # Editar configuración

# 6. Ejecutar la aplicación
./start_server.sh
```

### 3. ☁️ Servicios Cloud (Alternativas avanzadas)
- **Render** - Similar a Railway, con plan gratuito
- **Heroku** - Plataforma tradicional
- **Vercel** - Para aplicaciones frontend
- **Fly.io** - Buen rendimiento para apps con ML

## 🔧 Configuración del Servidor

### Variables de Entorno (.env)
```bash
# Producción
PRODUCTION=true
PORT=8000

# CORS
ALLOWED_ORIGINS=["*"]

# Luna Bot
LUNA_DEFAULT_LANGUAGE=es
LUNA_WIDGET_POSITION=bottom-right
LUNA_AUTO_OPEN=true
LUNA_AUTO_OPEN_DELAY=3000

# Logging
LOG_LEVEL=INFO
```

### Puertos y Firewall
- **Puerto 8000**: Aplicación principal
- **Puerto 80/443**: Nginx reverse proxy (recomendado)
- Configurar firewall para permitir solo puertos necesarios

## 📊 Comparación de Opciones

| Servicio | Costo | 24/7 | Recursos ML | Complejidad |
|----------|-------|------|-------------|-------------|
| Ngrok | Gratis | ❌ No | ❌ Limitado | Baja |
| VPS Básico | $3-6/mes | ✅ Sí | ✅ Completo | Media |
| Cloud Run | Pago por uso | ✅ Sí | ✅ Completo | Alta |
| Render | Gratis/pequeño | ✅ Sí | ⚠️ Limitado | Baja |

## 🚀 Scripts de Despliegue

### Para Testing Rápido:
```bash
./expose_with_ngrok.sh
```

### Para Producción:
```bash
./start_server.sh
```

### Verificación:
```bash
./check_deployment.sh
```

## 🔍 Troubleshooting

### Problemas Comunes:
1. **Memoria insuficiente**: Aumentar RAM del servidor (mínimo 2GB)
2. **Dependencias ML**: Asegurar instalación completa de PyTorch
3. **Puertos bloqueados**: Configurar firewall correctamente
4. **Variables de entorno**: Verificar archivo .env

### Logs y Debugging:
```bash
# Ver logs de la aplicación
tail -f logs/revista_expats_ai.log

# Ver procesos
ps aux | grep python

# Verificar puertos
netstat -tlnp | grep :8000
```

## 📞 Soporte

Para problemas específicos:
1. Revisar logs de la aplicación
2. Verificar configuración del servidor
3. Comprobar conectividad de red
4. Validar dependencias instaladas
**Para pruebas rápidas y feedback**
```bash
# Instalar
snap install ngrok

# Configurar (obtén token gratis en ngrok.com)
ngrok config add-authtoken TU_TOKEN

# Usar script automático
./expose_with_ngrok.sh
```

**Ventajas:**
- ✅ URL HTTPS instantánea
- ✅ Fácil de compartir
- ✅ No necesitas servidor externo

**Desventajas:**
- ❌ URL cambia cada vez
- ❌ Límite de 8 horas/día gratis

### 2. 🎨 Render (Alternativa gratuita)
**Para producción permanente**

**Ventajas:**
- ✅ Siempre disponible (24/7)
- ✅ URL permanente
- ✅ Escalado automático
- ✅ Despliegue desde GitHub
- ✅ Fácil de mantener

**Desventajas:**
- ❌ Límite de uso gratis

**Para desplegar:**
1. Ve a [render.com](https://render.com)
2. Conecta tu GitHub
3. Crea "Web Service" desde tu repo
4. Render hace todo automáticamente

### 3. 🖥️ Servidor Local 24/7 (Para acceso local)
**Si tienes IP fija o dominio**
```bash
# Instalar servicio systemd
sudo ./install_service.sh

# Configurar port forwarding en tu router
# Puerto 8000 -> tu PC
```

**Ventajas:**
- ✅ Control total
- ✅ Sin costos
- ✅ Datos locales

**Desventajas:**
- ❌ Necesitas IP pública
- ❌ PC debe estar encendida

## 🛠️ Scripts Disponibles

- `start_server.sh` - Inicia servidor local
- `expose_with_ngrok.sh` - Expone con ngrok
- `install_service.sh` - Instala servicio systemd

## 📊 Comparación

| Opción | Costo | Disponibilidad | Complejidad | Recomendado para |
|--------|-------|----------------|-------------|------------------|
| Ngrok | Gratis/limitado | 8h/día | Baja | Pruebas rápidas |
| Render | Gratis/pequeño | 24/7 | Baja | Producción pequeña |
| VPS | $3-6/mes | 24/7 | Media | Producción completa |
| Local 24/7 | $0 | PC encendida | Media | Acceso local |

## 🎯 Recomendación

**Para pruebas rápidas:** Ngrok
**Para producción pequeña:** Render
**Para producción completa:** VPS (DigitalOcean/Linode)

¿Quieres que configure alguna de estas opciones?
