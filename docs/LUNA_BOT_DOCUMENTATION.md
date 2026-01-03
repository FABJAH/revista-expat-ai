# 🦉 Luna - Bot de Publicidad Dinámico

## Descripción General

**Luna** es un bot inteligente de ventas de espacios publicitarios para la **Revista de Expatriados**. Funciona como mascota virtual que:

- ✨ Se abre automáticamente con burbujas de diálogo dinámicas
- 🎯 Vende planes de publicidad de forma atractiva
- 🌐 Soporte bilingüe (Español e Inglés)
- 📊 Captura leads y datos de contacto
- 💬 Responde preguntas frecuentes sobre beneficios
- 🎁 Muestra testimonios de clientes exitosos

---

## Estructura del Sistema

```
widget/
├── luna-advertising.js      # Widget dinámico (navegador)
├── luna-advertising.css     # Estilos y animaciones
└── luna-demo.html          # Página de demostración

bots/
├── bot_advertising_sales.py # Bot de ventas (backend)
└── [otros bots...]

routes/
└── advertising_api.py       # API endpoints (Flask)

data/
├── plans.json              # Planes de precios (si se desea persistencia)
└── inquiries/              # Carpeta de leads capturados
```

---

## 🚀 Instalación y Uso

### 1. Backend - Registrar API en Flask

En tu archivo `app.py` o `main.py`:

```python
from flask import Flask
from routes.advertising_api import register_advertising_api

app = Flask(__name__)

# Registrar el blueprint del bot publicitario
register_advertising_api(app)

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. Frontend - Incluir Widget en HTML

En cualquier página HTML donde quieras el bot:

```html
<!DOCTYPE html>
<html>
<head>
    <!-- Incluir CSS del widget -->
    <link rel="stylesheet" href="/widget/luna-advertising.css">
</head>
<body>
    <!-- Tu contenido aquí -->

    <!-- Incluir JS del widget al final del body -->
    <script src="/widget/luna-advertising.js"></script>

    <!-- Opcional: Configurar idioma inicial -->
    <script>
        window.lunaLanguage = 'es'; // 'es' o 'en'
    </script>
</body>
</html>
```

### 3. Probar en Demo

Abre `widget/luna-demo.html` en tu navegador para ver Luna en acción.

---

## 📋 Planes y Precios

Luna ofrece 4 planes configurables:

### Plan Básico - 19€/mes
- ✅ Listing en directorio digital
- ✅ Perfil con foto y descripción
- ✅ 2 categorías principales
- ✅ Visible para ~5,000 usuarios/mes

### Plan Premium - 34€/mes (⭐ Popular)
- ✅ Todo del Plan Básico
- ✅ Featured (destacado en búsquedas)
- ✅ Hasta 5 categorías
- ✅ Visible para ~15,000 usuarios/mes
- ✅ Soporte prioritario
- ✅ Analytics básico

### Plan Featured - 64€/mes
- ✅ Todo del Plan Premium
- ✅ Logo personalizado
- ✅ Hasta 10 fotos/videos
- ✅ Banner rotativo en homepage
- ✅ Visible para ~30,000 usuarios/mes
- ✅ Analytics avanzado
- ✅ Prioridad en customer success

### Plan Anual - 199€/año
- ✅ Plan Premium todo el año
- ✅ 15% ahorro vs. mensual
- ✅ Visibilidad garantizada
- ✅ Featured en eventos especiales
- ✅ Newsletter exclusiva 2x/mes

---

## 🔧 Endpoints API

### 1. Chat Principal

```
POST /api/bot/advertising

Request:
{
    "message": "¿Cuál es el precio?",
    "language": "es",
    "conversation_id": "conv_123...",
    "user_id": "user_456..."
}

Response:
{
    "type": "faq_answer",
    "message": "Nuestros precios varían desde 19€...",
    "quick_replies": [...],
    "conversation_id": "conv_123...",
    "timestamp": "2025-01-20T..."
}
```

### 2. Obtener Planes

```
GET /api/bot/advertising/plans?language=es

Response:
{
    "language": "es",
    "count": 4,
    "plans": [
        {
            "id": "basico",
            "nombre": "Plan Básico",
            "precio": "19€/mes",
            ...
        },
        ...
    ]
}
```

### 3. Detalle de Plan

```
GET /api/bot/advertising/plans/premium?language=es

Response:
{
    "type": "plan_details",
    "plan_id": "premium",
    "nombre": "Plan Premium",
    "precio": "34€/mes",
    ...
}
```

### 4. Capturar Lead

```
POST /api/bot/advertising/inquiry

Request:
{
    "name": "Juan García",
    "email": "juan@example.com",
    "business_name": "Abogados García",
    "phone": "+34 912 345 678",
    "language": "es",
    "plan_interested": "premium"
}

Response:
{
    "success": true,
    "message": "¡Gracias! Nos pondremos en contacto en 24 horas.",
    "inquiry_id": "inquiry_2025-01-20T..."
}
```

### 5. Testimonios

```
GET /api/bot/advertising/testimonials?language=es

Response:
{
    "type": "testimonials",
    "title": "Lo que dicen nuestros clientes",
    "testimonials": [
        {
            "nombre": "Juan López",
            "negocio": "Abogado - Especialista en NIE",
            "plan": "Plan Premium",
            "testimonial": "En 3 meses triplicamos nuestras consultas.",
            "emoji": "⭐⭐⭐⭐⭐"
        },
        ...
    ]
}
```

### 6. Saludo Dinámico

```
GET /api/bot/advertising/greeting?language=es&time=morning

Response:
{
    "type": "greeting",
    "message": "¡Hola! 👋 ¿Es tu primer día en Barcelona?...",
    "mascot": {
        "emoji": "🦉",
        "name": "Luna"
    },
    "quick_replies": [...]
}
```

### 7. Health Check

```
GET /api/bot/advertising/health

Response:
{
    "status": "healthy",
    "bot": "advertising_sales",
    "timestamp": "2025-01-20T..."
}
```

---

## 💬 Flujo de Conversación

Luna detects intención del usuario y responde automáticamente:

### 1. Preguntas sobre Planes
Usuario: "¿Cuáles son vuestros planes?"
Luna: Muestra comparativa visual de 4 planes lado a lado

### 2. Preguntas sobre Precios
Usuario: "¿Cuánto cuesta?"
Luna: Explica pricing y opciones de pago

### 3. Preguntas sobre Beneficios
Usuario: "¿Qué incluye cada plan?"
Luna: Detalla beneficios de cada propuesta

### 4. Preguntas Técnicas
Usuario: "¿Puedo cambiar de plan?"
Luna: Respuesta FAQ + botón "Hablar con ventas"

### 5. Intent Comercial
Usuario: "Quiero anunciar"
Luna: Muestra planes y propone siguiente paso

---

## 🎨 Personalización

### Cambiar Planes

Edita `bots/bot_advertising_sales.py`:

```python
ADVERTISING_PLANS = {
    "es": {
        "mi_plan_custom": {
            "nombre": "Mi Plan Custom",
            "precio": "XXX€/mes",
            "beneficios": [
                "✅ Beneficio 1",
                "✅ Beneficio 2",
            ]
        }
    }
}
```

### Cambiar Mensajes Proactivos

Edita en `bot_advertising_sales.py`:

```python
PROACTIVE_MESSAGES = {
    "es": {
        "greeting_morning": "Tu mensaje personalizado...",
        "greeting_afternoon": "...",
        "greeting_evening": "...",
    }
}
```

### Cambiar Mascota

Edita `luna-advertising.js`:

```javascript
const MASCOT = {
    name_es: "Luna",
    emoji: "🦉",  // Cambiar emoji aquí
    color: "#FF6B6B"  // Color del botón
}
```

### Cambiar Estilos

Edita `luna-advertising.css` - Variables CSS al inicio:

```css
:root {
  --luna-primary: #FF6B6B;        /* Color principal */
  --luna-secondary: #FFB703;      /* Color secundario */
  --luna-radius: 16px;             /* Radio de bordes */
  --luna-shadow: rgba(0, 0, 0, 0.1); /* Sombras */
}
```

---

## 📊 Seguimiento de Leads

Los leads capturados se guardan en:

```
data/inquiries/
└── inquiry_2025-01-20T12-34-56.123456.json
```

Cada archivo contiene:

```json
{
    "timestamp": "2025-01-20T12:34:56.123456",
    "name": "Juan García",
    "email": "juan@example.com",
    "business_name": "Abogados García",
    "phone": "+34 912 345 678",
    "language": "es",
    "status": "new"
}
```

### Procesar Leads

```python
from pathlib import Path
import json

inquiries_dir = Path("data/inquiries")
for inquiry_file in inquiries_dir.glob("*.json"):
    with open(inquiry_file) as f:
        inquiry = json.load(f)
        print(f"Nuevo lead: {inquiry['business_name']}")
        # Enviar email, guardar en CRM, etc.
```

---

## 🌐 Soporte Bilingüe

Luna responde en **Español e Inglés** automáticamente.

### Cambiar Idioma Dinámicamente

```javascript
// En el navegador
window.lunaLanguage = 'en';  // Cambia a inglés
window.lunaWidget.openChat();
```

### API con Idioma

```
POST /api/bot/advertising
{
    "message": "What are your plans?",
    "language": "en"  // o "es"
}
```

---

## 🔐 Consideraciones de Seguridad

- ✅ Validación de inputs en backend
- ✅ Sanitización de HTML en frontend
- ✅ Rate limiting recomendado para API
- ✅ CORS configurado para dominio
- ✅ Datos de inquiries almacenados localmente (privado)

---

## 📈 Métricas y Analytics

Luna registra automáticamente:

- Mensajes enviados/recibidos
- Tipo de respuestas
- Plans visualizados
- Leads capturados
- Idioma utilizado
- Hora de interacción

Se guardan en: `data/logs/advertising_conversations.jsonl`

### Ejemplo de Log

```json
{
    "timestamp": "2025-01-20T12:34:56",
    "message": "¿Cuáles son los precios?",
    "language": "es",
    "response_type": "faq_answer",
    "conversation_id": "conv_123...",
    "user_id": "user_456..."
}
```

---

## 🐛 Troubleshooting

### "El widget no aparece"
- Verifica que `luna-advertising.js` está cargado
- Revisa la consola del navegador (F12)
- Asegúrate que la ruta es `/widget/luna-advertising.js`

### "El chat no responde"
- Verifica que la API Flask está corriendo
- Revisa que el endpoint `/api/bot/advertising` existe
- Revisa errores en consola del navegador

### "Respuestas vacías"
- Verifica que el idioma es correcto (`es` o `en`)
- Revisa que `bot_advertising_sales.py` se importa correctamente
- Comprueba logs en `data/logs/advertising_conversations.jsonl`

### "Estilos rotos"
- Asegúrate que `luna-advertising.css` está cargado
- Verifica la ruta correcta del archivo
- Revisa que no hay conflictos CSS globales

---

## 📝 Ejemplos de Uso

### Ejemplo 1: Chat Básico

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/widget/luna-advertising.css">
</head>
<body>
    <h1>Bienvenido a nuestra revista</h1>
    <p>Busca servicios y negocios aquí...</p>

    <script src="/widget/luna-advertising.js"></script>
</body>
</html>
```

### Ejemplo 2: Configuración Avanzada

```html
<script>
document.addEventListener('DOMContentLoaded', () => {
    window.lunaWidget = new LunaAdvertisingWidget({
        language: 'es',
        position: 'bottom-right',
        autoOpen: true,
        autoOpenDelay: 3000
    });

    // Abrir chat manualmente
    document.getElementById('btn-contact').addEventListener('click', () => {
        window.lunaWidget.openChat();
    });
});
</script>
```

### Ejemplo 3: Obtener Planes Vía API

```javascript
fetch('/api/bot/advertising/plans?language=es')
    .then(res => res.json())
    .then(data => {
        console.log('Planes:', data.plans);
        data.plans.forEach(plan => {
            console.log(`${plan.nombre}: ${plan.precio}`);
        });
    });
```

---

## 🎯 Próximas Mejoras Planeadas

- [ ] Integración con Stripe para pagos directos
- [ ] Dashboard de ventas en tiempo real
- [ ] A/B testing de mensajes
- [ ] Integración con CRM (Hubspot, Salesforce)
- [ ] Chatbot en Whatsapp
- [ ] Video testimonios interactivos
- [ ] Formulario de presupuesto personalizado
- [ ] Integraciones con Google Analytics

---

## 📧 Soporte

Para preguntas o reportar issues:

- 📧 Email: support@revistaexpatriados.es
- 💬 Chat directo: Abre Luna en cualquier página
- 📱 WhatsApp: +34 XXX XXX XXX

---

## 📄 Licencia

Sistema propietario de Revista de Expatriados © 2025

---

**Happy selling! 🎉**

Recuerda: Luna no solo vende, ¡también conecta!
