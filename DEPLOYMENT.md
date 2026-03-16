# 🚀 Despliegue - Revista Expats AI

## 🎯 Objetivo
Permitir que cualquier persona acceda a la aplicación 24/7 sin necesidad de que el servidor local esté siempre corriendo.

## ✅ Cambios Recientes
- **REMOVIDO:** Dependencias de ML (PyTorch, sentence-transformers) para compatibilidad con Railway
- **SIMPLIFICADO:** Clasificación de intenciones usando solo palabras clave
- **OPTIMIZADO:** Para despliegue en plataformas gratuitas

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

### 2. 🚂 Railway (RECOMENDADO - Gratis para proyectos pequeños)
**Para producción permanente - ¡Ya está configurado!**

**Estado:** ✅ **LISTO PARA DESPLEGAR**

**Ventajas:**
- ✅ Siempre disponible (24/7)
- ✅ URL permanente
- ✅ Escalado automático
- ✅ Despliegue desde GitHub
- ✅ Base de datos incluida
- ✅ Fácil de mantener

**Desventajas:**
- ❌ Límite de uso gratis (512MB RAM, 1GB disco)

**Para desplegar ahora:**
1. Ve a [railway.app](https://railway.app)
2. Conecta tu GitHub
3. Selecciona el repo `revista-expat-ai`
4. Railway hace todo automáticamente

**Guía detallada:** Ver [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)

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
