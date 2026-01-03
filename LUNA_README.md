# 🦉 LUNA - Bot de Publicidad

## ¿Qué es Luna?

Luna es un **bot inteligente de ventas** que ayuda a la Revista de Expatriados a:
- ✅ Vender espacios publicitarios automáticamente
- ✅ Responder preguntas sobre planes y precios
- ✅ Capturar leads de empresas interesadas
- ✅ Proporcionar una experiencia conversacional atractiva

---

## 🚀 Instalación Rápida

### 1️⃣ Verificar Setup (2 minutos)
```bash
python3 setup_luna.py
```
Deberías ver: ✅ **¡Todos los chequeos pasaron!**

### 2️⃣ Registrar en tu App (1 minuto)
```python
# En main.py o app.py
from routes.advertising_api import register_advertising_api

app = Flask(__name__)
register_advertising_api(app)
```

### 3️⃣ Incluir en HTML (1 minuto)
```html
<link rel="stylesheet" href="/widget/luna-advertising.css">
<script src="/widget/luna-advertising.js"></script>
```

### 4️⃣ Probar (0 minutos)
Abre: `widget/luna-demo.html`
¡Verás Luna en funcionamiento! 🎉

---

## 📁 Estructura

```
widget/
├── luna-advertising.js      ← Widget interactivo
├── luna-advertising.css     ← Estilos y animaciones
└── luna-demo.html          ← Demostración

bots/
└── bot_advertising_sales.py ← Lógica de ventas

routes/
└── advertising_api.py       ← API REST (7 endpoints)

config/
└── luna_config.py          ← Configuración editable

data/
├── inquiries/              ← Leads capturados
└── logs/                   ← Analytics
```

---

## 💰 Planes de Publicidad

| Plan | Precio | Usuarios | Característica |
|------|--------|----------|-----------------|
| 🌱 Básico | 19€/mes | 5k | Inicio perfecto |
| ⭐ Premium | 34€/mes | 15k | Popular |
| 👑 Featured | 64€/mes | 30k | Premium |
| 🎁 Anual | 199€/año | 15k | Mejor valor |

**Personalizable:** Edita `config/luna_config.py`

---

## 🎯 Características

✨ **Dinámico**
- Burbujas que se abren automáticamente
- Mensajes diferentes por hora del día
- Interacciones conversacionales

🎨 **Atractivo**
- Mascota búho lindísima (🦉)
- Animaciones suaves
- Responsive (mobile-first)

🌐 **Bilingüe**
- Español por defecto
- English automático
- Cambio en tiempo real

💬 **Inteligente**
- Detecta intención del usuario
- Responde FAQ automáticamente
- Propone siguiente paso

📊 **Medible**
- Analytics completo
- Tracking de conversaciones
- Leads estructurados

---

## 🔌 Endpoints API

```
POST   /api/bot/advertising           ← Chat principal
GET    /api/bot/advertising/plans     ← Lista de planes
GET    /api/bot/advertising/plans/{id}← Detalle de plan
POST   /api/bot/advertising/inquiry   ← Capturar lead
GET    /api/bot/advertising/greeting  ← Saludos dinámicos
GET    /api/bot/advertising/testimonials ← Testimonios
GET    /api/bot/advertising/health    ← Status check
```

---

## 📚 Documentación

| Documento | Para qué |
|-----------|----------|
| [LUNA_IMPLEMENTATION_COMPLETE.md](LUNA_IMPLEMENTATION_COMPLETE.md) | Guía completa de implementación |
| [docs/LUNA_BOT_DOCUMENTATION.md](docs/LUNA_BOT_DOCUMENTATION.md) | Documentación técnica detallada |
| [LUNA_INTEGRATION_GUIDE.md](LUNA_INTEGRATION_GUIDE.md) | Pasos de integración |
| [LUNA_BOT_SUMMARY.md](LUNA_BOT_SUMMARY.md) | Resumen de archivos creados |

---

## 🎨 Personalización (Sin Código)

Edita `config/luna_config.py` para cambiar:
- 💰 Planes y precios
- 💬 Mensajes y saludos
- 🎨 Colores y tema
- 🦉 Mascota
- ⭐ Testimonios
- ❓ FAQ

---

## 📊 Analytics

Luna registra automáticamente todas las conversaciones:

```
data/logs/advertising_conversations.jsonl
```

Cada línea = una interacción (JSON)

**Analizar:**
```python
import json
with open('data/logs/advertising_conversations.jsonl') as f:
    for line in f:
        interaction = json.loads(line)
        print(f"{interaction['message']} → {interaction['response_type']}")
```

---

## 🆘 Troubleshooting

| Problema | Solución |
|----------|----------|
| Widget no aparece | Revisa ruta de JS/CSS en HTML |
| Chat no responde | Verifica que API está registrada |
| Estilos rotos | Limpia cache (Ctrl+Shift+R) |
| Leads no se guardan | Crea `data/inquiries/` |

---

## 📈 Próximas Mejoras

- [ ] Pago directo en chat (Stripe)
- [ ] Dashboard de vendedor
- [ ] A/B testing automático
- [ ] Whatsapp integration
- [ ] Videollamadas
- [ ] CRM integration

---

## 💡 Tips

1. **Personaliza los mensajes** - Luna es más efectiva con tu voz
2. **Actualiza testimonios** - Clientes reales = más confianza
3. **Monitorea logs** - Aprende de tus usuarios
4. **Itera rápido** - Cambia config sin desplegar

---

## 🚀 Siguientes Pasos

1. ✅ Ejecutar `setup_luna.py`
2. ✅ Registrar blueprint en app
3. ✅ Incluir en HTML
4. ✅ Probar demo
5. ✅ Personalizar planes
6. ✅ Implementar en sitio
7. ✅ Monitorear

---

**¿Preguntas? Revisa la documentación o abre `widget/luna-demo.html` para ver todo en acción.**

---

**Luna está lista para vender. ¡Adelante! 🦉🚀**
