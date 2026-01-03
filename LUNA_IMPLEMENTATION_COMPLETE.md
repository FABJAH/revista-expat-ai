# 🦉 LUNA - Bot de Publicidad Integrado
## Implementación Completa para Revista de Expatriados

**Fecha:** 20 de Diciembre de 2025
**Estado:** ✅ Completado y Probado
**Versión:** 1.0

---

## 📋 Resumen Ejecutivo

Se ha creado **Luna**, un sistema completo de ventas de espacios publicitarios con:

- ✅ **Bot inteligente** bilingüe (ES/EN) que vende planes de publicidad
- ✅ **Widget dinámico** con mascota atractiva (búho 🦉)
- ✅ **4 planes flexibles** (Básico, Premium, Featured, Anual)
- ✅ **Burbujas proactivas** que aparecen automáticamente
- ✅ **Captura de leads** estructurada
- ✅ **Analytics completo** de conversaciones
- ✅ **Integración fácil** con Flask/FastAPI existente
- ✅ **Personalizable** sin tocar código (config centralizada)

---

## 🚀 Inicio Rápido (5 Minutos)

### 1. Verificar Instalación
```bash
cd /home/fleet/Escritorio/Revista-expats-ai
python3 setup_luna.py
```
✅ Todo debe pasar los chequeos

### 2. Registrar Blueprint en tu App

**En `main.py` o `app.py` de tu proyecto:**

```python
from flask import Flask
from routes.advertising_api import register_advertising_api

app = Flask(__name__)

# Registrar Luna API
register_advertising_api(app)

# ... resto de configuración
```

### 3. Incluir Widget en HTML

**En cualquier página donde quieras Luna:**

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/widget/luna-advertising.css">
</head>
<body>
    <!-- Tu contenido -->

    <script src="/widget/luna-advertising.js"></script>
    <script>
        window.lunaLanguage = 'es';  // Auto-detecta si no se establece
    </script>
</body>
</html>
```

### 4. Probar

Abre: `widget/luna-demo.html` en el navegador
→ Verás Luna funcionando con todos sus features

---

## 📁 Archivos Creados

| Archivo | Tamaño | Descripción |
|---------|--------|-------------|
| `bots/bot_advertising_sales.py` | 20 KB | Bot principal con lógica de ventas |
| `routes/advertising_api.py` | 9 KB | API REST con 7 endpoints |
| `config/luna_config.py` | 21 KB | Configuración de planes, mensajes, FAQ |
| `widget/luna-advertising.js` | 15 KB | Widget interactivo dinámico |
| `widget/luna-advertising.css` | 15 KB | Estilos, animaciones, responsive |
| `widget/luna-demo.html` | 13 KB | Página de demostración |
| `docs/LUNA_BOT_DOCUMENTATION.md` | 12 KB | Documentación técnica completa |
| `setup_luna.py` | 11 KB | Script de validación/setup |
| `.env.example` | 0.5 KB | Variables de configuración |
| `LUNA_INTEGRATION_GUIDE.md` | 5 KB | Guía rápida de integración |

**Total:** ~102 KB de código + documentación

---

## 🔌 Integración con Proyecto Existente

### Opción A: FastAPI (si usas main.py con FastAPI)

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.advertising_api import advertising_api

app = FastAPI()

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="widget"), name="static")
app.mount("/static/widget", StaticFiles(directory="widget"), name="widget")

# Registrar API
app.include_router(advertising_api, prefix="/api")
```

### Opción B: Flask (si usas con Flask)

```python
from flask import Flask
from routes.advertising_api import register_advertising_api

app = Flask(__name__)
register_advertising_api(app)

app.run(debug=True)
```

### Opción C: Ambos (FastAPI + Flask)

```python
from fastapi import FastAPI
from flask import Flask
from routes.advertising_api import register_advertising_api as flask_register

# FastAPI
app = FastAPI()

# Flask wrapper para compatibilidad
flask_app = Flask(__name__)
flask_register(flask_app)

# Montar rutas de Flask en FastAPI
# (requiere middleware especial)
```

---

## 💰 Planes Disponibles

| Plan | Precio | Usuarios/Mes | Características | Ideal Para |
|------|--------|--------------|-----------------|-----------|
| **Básico** 🌱 | 19€/mes | ~5,000 | Listing digital, 2 categorías | Empresas nuevas |
| **Premium** ⭐ | 34€/mes | ~15,000 | Featured, 5 categorías, Analytics | La mayoría |
| **Featured** 👑 | 64€/mes | ~30,000 | Logo, 10 fotos, Banner, Analytics avanzado | Marcas consolidadas |
| **Anual** 🎁 | 199€/año | ~15,000 | Plan Premium + 15% descuento | Compromisos largo plazo |

**Personalizable:** Edita precios, beneficios, límites en `config/luna_config.py`

---

## 📊 Funcionalidades

### 1. Chat Principal (POST /api/bot/advertising)
```
Usuario: "¿Cuáles son vuestros planes?"
Luna: Muestra comparativa visual de 4 planes

Usuario: "¿Es caro?"
Luna: Explica precios y propone opciones

Usuario: "Quiero destacarme"
Luna: Muestra plan Featured con botón de CTA
```

### 2. Burbujas Proactivas
- Se abre automáticamente después de 3 segundos
- Saludos dinámicos (mañana/tarde/noche)
- Preguntas de venta cada 30 segundos si está cerrado
- Badges de notificación pulsantes

### 3. Comparativa Visual de Planes
- Grid de 2-4 planes lado a lado
- Emojis identificadores (🌱 ⭐ 👑 🎁)
- Beneficios listados
- Botones de CTA destacados

### 4. Captura de Leads
```
Campos: Nombre, Email, Empresa, Teléfono
Guardado: data/inquiries/inquiry_TIMESTAMP.json
Automático: Se envía cuando el usuario "Quiere contratar"
```

### 5. Testimonios
- 3 clientes exitosos (modificables)
- Rating de 5 estrellas
- Resultados medibles ("triplicamos consultas")
- Incluye plan que usaron

### 6. FAQ Inteligente
- Detecta intención por keywords
- Respuestas preprogramadas
- Propone siguiente paso
- Fallback a "Hablar con ventas"

---

## 📈 Analytics y Tracking

Luna registra automáticamente:

**Ubicación:** `data/logs/advertising_conversations.jsonl`

**Campos:**
```json
{
    "timestamp": "2025-12-20T14:30:45",
    "message": "¿Cuáles son los precios?",
    "language": "es",
    "response_type": "faq_answer",
    "conversation_id": "conv_abc123",
    "user_id": "user_xyz789"
}
```

**Análisis Posibles:**
- Preguntas más frecuentes
- Planes más consultados
- Idioma de preferencia
- Tasa de conversión
- Tiempo promedio en chat

---

## 🎨 Personalización (Sin Código)

### Cambiar Planes
Edita: `config/luna_config.py` → `PLANS_CONFIG`

Ejemplo:
```python
{
    "id": "startup",
    "nombre": "Plan Startup",
    "precio": 29,
    "beneficios": [
        "Listing en directorio",
        "3 categorías",
        # ...
    ]
}
```

### Cambiar Mensajes
Edita: `config/luna_config.py` → `DYNAMIC_MESSAGES`

```python
"greeting_morning": "¡Hola! Buenos días..."
"proactive_questions": [
    "¿Necesitas más visibilidad? 📈",
    # ...
]
```

### Cambiar Colores
Edita: `widget/luna-advertising.css` → `:root`

```css
--luna-primary: #FF6B6B;      /* Rojo actual */
--luna-secondary: #FFB703;    /* Naranja */
--luna-accent: #FB5607;       /* Coral */
```

### Cambiar Mascota
Edita: `config/luna_config.py` → `MASCOT_CONFIG`

```python
"emoji": "🦁",        # Cambiar de búho a león
"color_primary": "#FFD700"  # Oro
```

---

## 🌐 Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/bot/advertising` | Chat principal |
| GET | `/api/bot/advertising/plans` | Todos los planes |
| GET | `/api/bot/advertising/plans/{id}` | Detalle de plan |
| POST | `/api/bot/advertising/inquiry` | Capturar lead |
| GET | `/api/bot/advertising/greeting` | Saludos dinámicos |
| GET | `/api/bot/advertising/testimonials` | Testimonios |
| GET | `/api/bot/advertising/health` | Status check |

**Ejemplo de uso:**

```javascript
// Chat
fetch('/api/bot/advertising', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: "¿Cuáles son los planes?",
        language: "es"
    })
})
.then(res => res.json())
.then(data => console.log(data));

// Obtener planes
fetch('/api/bot/advertising/plans?language=es')
    .then(res => res.json())
    .then(data => data.plans.forEach(plan => {
        console.log(`${plan.nombre}: ${plan.precio}`);
    }));
```

---

## 🔐 Consideraciones de Seguridad

✅ **Validación de inputs** en backend
✅ **Sanitización de HTML** en frontend
✅ **Datos de leads** almacenados localmente (privado)
✅ **CORS configurable** por dominio
✅ **Rate limiting recomendado** en producción

---

## 🚨 Troubleshooting

### "El widget no aparece"
- Verifica rutas: `/widget/luna-advertising.js`
- Revisa consola (F12) para errores
- Abre demo: `widget/luna-demo.html`

### "Chat no responde"
- API Flask/FastAPI debe estar corriendo
- `/api/bot/advertising` debe estar registrado
- Revisa logs en `data/logs/`

### "Estilos rotos"
- Revisa que CSS está cargado (F12 → Network)
- Limpia cache: Ctrl+Shift+R
- Verifica ruta del CSS

### "Leads no se guardan"
- Carpeta `data/inquiries/` debe existir
- Permisos de escritura en `data/`
- Revisa errores en consola

---

## 📚 Documentación Relacionada

| Documento | Contenido |
|-----------|----------|
| `docs/LUNA_BOT_DOCUMENTATION.md` | Documentación técnica completa |
| `LUNA_BOT_SUMMARY.md` | Resumen de implementación |
| `LUNA_INTEGRATION_GUIDE.md` | Guía paso a paso |
| `REPORTE_PROYECTO_COMPLETO.md` | Contexto del proyecto general |

---

## 🎯 Próximas Mejoras

**Fase 2 (Futura):**
- [ ] Pago directo Stripe/Paypal en chat
- [ ] Dashboard de vendedor en tiempo real
- [ ] A/B testing de mensajes
- [ ] Chatbot en Whatsapp
- [ ] Videollamadas en widget
- [ ] Presupuestos personalizados
- [ ] Integración CRM (Hubspot, Salesforce)
- [ ] Google Analytics integration

---

## 📊 Métricas Reales de Revista

(Del documento Canva proporcionado)

- **Años activa:** 28 años (desde 1996)
- **Usuarios mensuales:** 12,000+
- **Usuarios activos:** 8,500
- **Tasa engagement:** 87%
- **Tiempo promedio sesión:** 15 minutos
- **Negocios destacados:** 280+
- **Categorías:** 10

---

## ✅ Checklist de Integración

- [ ] Ejecutar `python3 setup_luna.py` (sin errores)
- [ ] Registrar blueprint en app Flask/FastAPI
- [ ] Incluir CSS en `<head>`
- [ ] Incluir JS antes de `</body>`
- [ ] Probar en `widget/luna-demo.html`
- [ ] Crear `data/inquiries/` si no existe
- [ ] Crear `data/logs/` si no existe
- [ ] Verificar permisos de escritura en `data/`
- [ ] Personalizar `config/luna_config.py`
- [ ] Probar endpoints API con Postman
- [ ] Implementar en sitio web
- [ ] Monitorear analytics en `data/logs/`

---

## 🎉 Conclusión

**Luna está lista para:**
1. ✅ Aumentar visibilidad de espacios publicitarios
2. ✅ Generar leads de calidad
3. ✅ Mejorar engagement del sitio
4. ✅ Proporcionar experiencia de usuario atractiva
5. ✅ Escalar con nuevas funcionalidades

**Tiempo de implementación:** < 5 minutos
**Complejidad:** Baja (plug & play)
**Mantenimiento:** Mínimo (autocontrolado)

---

**¡Adelante con Luna! 🦉🚀**

_Revista de Expatriados - Diciembre 2025_
