# 🦉 LUNA - Bot de Publicidad Dinámico
## Resumen de Implementación Completada

---

## 📦 Archivos Creados

### Backend (Python)

#### 1. **bots/bot_advertising_sales.py** ⭐
Bot inteligente de ventas con:
- ✅ 4 planes configurables (Básico, Premium, Featured, Anual)
- ✅ Respuestas dinámicas a preguntas de clientes
- ✅ Sistema de saludos por hora (mañana, tarde, noche)
- ✅ Captura de leads (inquiries)
- ✅ Testimonios de clientes exitosos
- ✅ Soporte bilingüe (ES/EN)
- ✅ Clase `AdvertisingSalesBot` con métodos principales

**Métodos principales:**
```python
get_greeting(language, time_of_day)
get_plans_comparison(language)
get_plan_details(plan_id, language)
respond_to_question(question, language)
get_testimonials(language)
create_inquiry(name, email, business_name, phone, language)
responder_consulta_ventas(pregunta, language)  # Endpoint principal
```

---

#### 2. **routes/advertising_api.py** 🚀
API REST con Flask Blueprint:
- `POST /api/bot/advertising` - Chat principal
- `GET /api/bot/advertising/plans` - Obtener todos los planes
- `GET /api/bot/advertising/plans/{plan_id}` - Detalle de plan
- `POST /api/bot/advertising/inquiry` - Capturar leads
- `GET /api/bot/advertising/greeting` - Saludos dinámicos
- `GET /api/bot/advertising/testimonials` - Testimonios
- `GET /api/bot/advertising/health` - Health check

**Integración en Flask:**
```python
from routes.advertising_api import register_advertising_api
app = Flask(__name__)
register_advertising_api(app)
```

---

#### 3. **config/luna_config.py** ⚙️
Configuración centralizada:
- Configuración de mascota (nombre, emoji, color)
- 4 planes completos (ES/EN) con beneficios
- Mensajes dinámicos por contexto
- FAQ en ambos idiomas
- Categorías disponibles
- Testimonios precargados
- Métricas de la plataforma
- Funciones de utilidad para acceder a datos

**Uso:**
```python
from config.luna_config import get_all_plans, get_categories
plans = get_all_plans("es")
categories = get_categories("en")
```

---

### Frontend (JavaScript + CSS)

#### 4. **widget/luna-advertising.js** 💬
Widget dinámico interactivo:
- ✅ Clase `LunaAdvertisingWidget`
- ✅ Interfaz de chat con HTML5
- ✅ Mensajes proactivos automáticos
- ✅ Animaciones suaves
- ✅ Comparativa visual de planes
- ✅ Galería de testimonios
- ✅ Quick reply buttons
- ✅ Typing indicators
- ✅ API calls a backend
- ✅ Tracking de conversaciones
- ✅ Bilingual support

**Uso:**
```javascript
const widget = new LunaAdvertisingWidget({
    language: 'es',
    position: 'bottom-right',
    autoOpen: true,
    autoOpenDelay: 3000
});
```

---

#### 5. **widget/luna-advertising.css** 🎨
Estilos completos y animaciones:
- Tema moderno con gradientes
- CSS variables para fácil personalización
- Animaciones suaves:
  - `gentle-bounce` - Movimiento del búho
  - `happy-bounce` - Al pasar mouse
  - `message-appear` - Entrada de mensajes
  - `typing-bounce` - Indicador de escritura
  - `button-bounce` - Notificación de nuevo mensaje
  - `badge-pulse` - Badge de notificación
- Dark mode automático
- Responsive (mobile-first)
- Scroll suave en conversaciones

---

#### 6. **widget/luna-demo.html** 📄
Página de demostración interactiva:
- Descripción visual de Luna
- Features listadas
- Estadísticas (5000+ usuarios, 92% engagement)
- Cómo funciona paso a paso
- Instrucciones de integración
- Toggle de idioma (ES/EN)
- Botones para probar funcionalidades
- Info de soporte

**Abre en navegador:** `widget/luna-demo.html`

---

### Documentación

#### 7. **docs/LUNA_BOT_DOCUMENTATION.md** 📚
Documentación completa:
- Descripción general
- Instalación paso a paso
- 4 planes con beneficios
- 7 endpoints API documentados
- Flujos de conversación
- Guía de personalización
- Manejo de leads
- Bilingüismo
- Troubleshooting
- Ejemplos de código
- Roadmap futuro

---

## 🎯 Características Principales

### 1. Bot Dinámico
```
✅ Abre automáticamente con saludo personalizado
✅ Burbujas de diálogo cada 30 segundos (si cerrado)
✅ Mensajes diferentes por hora del día
✅ Responde preguntas en tiempo real
```

### 2. Mascota Atractiva
```
✅ Emoji búho 🦉 (tender, curioso)
✅ Animaciones suaves
✅ Bounce al pasar mouse
✅ Personalizable (color, emoji, nombre)
```

### 3. Planes Flexibles
```
Básico:    19€/mes  - Inicio
Premium:   34€/mes  - Popular ⭐
Featured:  64€/mes  - Premium
Anual:     199€/año - Best value
```

### 4. Bilingüe
```
✅ Español (es) - Default
✅ Inglés (en)  - Auto-detect navegador
✅ Fácil cambio en tiempo real
```

### 5. Captura de Leads
```
✅ Formulario ligero en chat
✅ Campos: nombre, email, teléfono, empresa
✅ Guardado en: data/inquiries/
✅ JSON estructurado
```

### 6. Analytics
```
✅ Logs automáticos en: data/logs/advertising_conversations.jsonl
✅ Tracking: mensaje, respuesta, idioma, conversación_id
✅ Fácil análisis posteriör
```

---

## 🚀 Instalación Rápida

### 1. Registrar Blueprint en Flask
```python
# app.py
from routes.advertising_api import register_advertising_api

app = Flask(__name__)
register_advertising_api(app)
```

### 2. Incluir en HTML
```html
<link rel="stylesheet" href="/widget/luna-advertising.css">
<script src="/widget/luna-advertising.js"></script>
```

### 3. ¡Listo!
El widget aparecerá automáticamente en la esquina inferior derecha.

---

## 📊 Estructura de Datos

### Plan
```json
{
    "id": "premium",
    "nombre": "Plan Premium",
    "precio": 34,
    "periodo": "mes",
    "beneficios": ["...", "..."],
    "limite_categorias": 5,
    "featured": true,
    "analytics": true
}
```

### Inquiry (Lead)
```json
{
    "timestamp": "2025-01-20T12:34:56",
    "name": "Juan García",
    "email": "juan@example.com",
    "business_name": "Abogados García",
    "phone": "+34 912 345 678",
    "language": "es",
    "status": "new"
}
```

### Log de Conversación
```json
{
    "timestamp": "2025-01-20T12:34:56",
    "message": "¿Cuáles son los precios?",
    "language": "es",
    "response_type": "faq_answer",
    "conversation_id": "conv_123..."
}
```

---

## 🎨 Personalización

### Cambiar Planes
`config/luna_config.py` → `PLANS_CONFIG`

### Cambiar Mascota
`config/luna_config.py` → `MASCOT_CONFIG`
O directamente en `widget/luna-advertising.js`

### Cambiar Colores
`widget/luna-advertising.css` → `:root` variables

### Cambiar Mensajes
`config/luna_config.py` → `DYNAMIC_MESSAGES`
O editar en `bot_advertising_sales.py`

---

## 🔌 Integración con Sistemas Existentes

### Con base de datos
```python
# En advertising_api.py, método create_inquiry():
# Reemplazar guardado JSON con INSERT a DB
```

### Con email/SMS
```python
# Después de crear inquiry:
send_email(inquiry['email'], "Confirmación")
send_sms(inquiry['phone'], "Nos contactaremos")
```

### Con CRM
```python
# En create_inquiry():
crm.create_lead(
    name=inquiry['name'],
    email=inquiry['email'],
    source='luna_bot'
)
```

### Con analytics
```javascript
// En luna-advertising.js:
window.gtag('event', 'luna_message_sent', {
    message_type: type,
    language: language
});
```

---

## 📈 Métricas Disponibles

```
- Usuarios únicos por conversación
- Mensajes promedio por sesión
- Tasa de conversión plan (clicks → leads)
- Idioma más usado
- Hora pico de visitas
- Plan más consultado
- Tasa de abandono
- Tiempo promedio en chat
```

**Acceder:** `data/logs/advertising_conversations.jsonl`

---

## 🆘 Troubleshooting

| Problema | Solución |
|----------|----------|
| Widget no aparece | Verificar rutas de archivos JS/CSS |
| Chat no responde | Revisar API Flask está corriendo |
| Respuestas vacías | Verificar idioma (es/en) |
| Estilos rotos | Limpiar cache, F5 hard refresh |
| Leads no se guardan | Verificar permisos carpeta `data/` |
| Doble widget | Incluir JS una sola vez |

---

## 🎉 Próximas Mejoras

- [ ] Integración Stripe/Paypal
- [ ] Dashboard de ventas tiempo real
- [ ] A/B testing de mensajes
- [ ] Integración Whatsapp
- [ ] Videollamadas en chat
- [ ] Presupuestos personalizados
- [ ] Integraciones CRM (Hubspot, Salesforce)
- [ ] Google Analytics tracking

---

## 📁 Estructura Final del Proyecto

```
/home/fleet/Escritorio/Revista-expats-ai/
│
├── bots/
│   ├── bot_advertising_sales.py      ⭐ Bot principal
│   └── [otros bots...]
│
├── routes/
│   ├── advertising_api.py             ⭐ API endpoints
│   └── [otras rutas...]
│
├── config/
│   ├── luna_config.py                 ⭐ Configuración
│   └── [otros configs...]
│
├── widget/
│   ├── luna-advertising.js            ⭐ Widget JS
│   ├── luna-advertising.css           ⭐ Estilos
│   ├── luna-demo.html                 ⭐ Demo
│   └── [otros widgets...]
│
├── data/
│   ├── inquiries/                     📂 Leads capturados
│   ├── logs/
│   │   └── advertising_conversations.jsonl  📂 Analytics
│   └── [otros datos...]
│
├── docs/
│   ├── LUNA_BOT_DOCUMENTATION.md      ⭐ Documentación
│   └── [otros docs...]
│
└── [otros archivos...]
```

---

## 💡 Tips para Máximo Impacto

1. **Personalizar mensaje de bienvenida**
   - Cambiar `PROACTIVE_MESSAGES` según tu público

2. **Destacar plan popular**
   - Marcar `"popular": true` en config de plan

3. **Usar emojis estratégicamente**
   - 🌱 para plan básico
   - ⭐ para plan popular
   - 👑 para plan premium

4. **A/B test de horarios**
   - Cambiar `auto_open_delay` (2000 vs 5000 ms)
   - Medir engagement

5. **Testimonios frescos**
   - Actualizar regularmente `TESTIMONIALS`

6. **Análisis de conversaciones**
   - Revisar `data/logs/` semanalmente
   - Ajustar FAQ basado en preguntas comunes

---

## 🎯 Próximos Pasos Recomendados

1. ✅ Instalar bot (ya completado)
2. ⏭️ Probar en `widget/luna-demo.html`
3. ⏭️ Registrar API en `app.py`
4. ⏭️ Personalizar planes según tu oferta
5. ⏭️ Ajustar mensajes para tu público
6. ⏭️ Implementar en sitio web
7. ⏭️ Monitorear analytics
8. ⏭️ Iterar basado en datos

---

## 📞 Soporte

- 📖 Documentación: `docs/LUNA_BOT_DOCUMENTATION.md`
- 💬 Demo interactiva: `widget/luna-demo.html`
- ⚙️ Configuración: `config/luna_config.py`
- 🐛 Issues: Revisar logs en `data/logs/`

---

**🦉 ¡Luna está lista para vender! ¡Éxito! 🎉**

_Creado con ❤️ para Revista de Expatriados_
