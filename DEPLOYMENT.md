# 🚀 Despliegue - Revista Expats AI

## 🎯 Objetivo
Permitir que cualquier persona acceda a la aplicación 24/7 sin necesidad de que el servidor local esté siempre corriendo.

## 📋 Opciones de Despliegue

### 1. 🌐 Ngrok (Más simple - Gratis con límites)
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

### 2. 🚂 Railway (Recomendado - Gratis para proyectos pequeños)
**Para despliegue permanente**
```bash
# 1. Sube tu código a GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Ve a railway.app y conecta tu repo
# 3. Railway detecta automáticamente Python/FastAPI
```

**Ventajas:**
- ✅ Siempre disponible
- ✅ URL permanente
- ✅ Escalado automático
- ✅ Base de datos incluida

### 3. 🎨 Render (Alternativa gratuita)
**Similar a Railway**
```bash
# 1. Sube a GitHub
# 2. Ve a render.com
# 3. Crea "Web Service" desde tu repo
```

### 4. 🖥️ Servidor Local 24/7 (Para acceso local)
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
| Railway | Gratis/pequeño | 24/7 | Baja | Producción pequeña |
| Render | Gratis/pequeño | 24/7 | Baja | Producción pequeña |
| Local 24/7 | $0 | PC encendida | Media | Acceso local |

## 🎯 Recomendación

**Para tu caso (feedback y pruebas):** Railway o Render
**Para desarrollo continuo:** Railway con GitHub integration

¿Quieres que configure alguna de estas opciones?
