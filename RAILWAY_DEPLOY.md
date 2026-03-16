# 🚀 Despliegue en Railway - Guía Rápida

## ✅ Requisitos Previos

1. **Cuenta en Railway**: Regístrate en [railway.app](https://railway.app)
2. **Cuenta en GitHub**: Tu código debe estar en GitHub
3. **Proyecto actualizado**: Ya hiciste push de los últimos cambios

## 🚀 Pasos para Desplegar

### 1. Conectar Railway con GitHub
1. Ve a [railway.app](https://railway.app) y haz login
2. Haz clic en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza a Railway para acceder a tus repositorios
5. Busca y selecciona tu repositorio: `revista-expat-ai`

### 2. Configuración Automática
Railway detectará automáticamente:
- ✅ Python 3.11 (por `runtime.txt` y `.python-version`)
- ✅ FastAPI application
- ✅ Puerto correcto (`$PORT`)
- ✅ Comando de inicio correcto

### 3. Variables de Entorno (Opcional)
Si necesitas configurar variables específicas:
1. Ve a tu proyecto en Railway
2. Haz clic en "Variables"
3. Agrega las variables del archivo `.env.example`

### 4. ¡Listo!
Railway comenzará a construir y desplegar automáticamente. En unos minutos tendrás:
- 🌐 **URL pública** (ej: `https://revista-expats.up.railway.app`)
- 📊 **Logs en tiempo real**
- 🔄 **Despliegues automáticos** cuando hagas push a GitHub

## 🧪 Probar el Despliegue

Una vez desplegado, prueba:
```bash
curl https://tu-url-de-railway.up.railway.app/api/health
```

Deberías ver: `{"status":"healthy","version":"1.0.0","service":"Revista Expats AI API"}`

## 💡 Consejos

- **Primer despliegue**: Puede tomar 10-15 minutos por las dependencias de ML
- **Actualizaciones**: Solo haz `git push` y Railway se actualiza automáticamente
- **Logs**: Ve a la pestaña "Logs" en Railway para debugging
- **Base de datos**: Railway incluye PostgreSQL gratis si lo necesitas

## 🔧 Solución de Problemas

Si hay errores:
1. Revisa los logs en Railway
2. Verifica que `requirements.txt` tenga versiones compatibles
3. Asegúrate de que `main.py` sea el punto de entrada correcto

¿Necesitas ayuda con algún paso específico?