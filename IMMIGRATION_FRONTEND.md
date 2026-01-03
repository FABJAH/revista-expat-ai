# 🌍 Bot de Inmigración - Implementación Frontend

## ✅ Completado

### Backend
- ✅ `routes/immigration_api.py` - Nuevo blueprint con endpoint `/api/immigration`
- ✅ `app.py` - Registrado el blueprint immigration_api
- ✅ `bots/bot_immigration.py` - Carga dinámica de anunciantes legales desde `data/anunciantes.json`

### Frontend
- ✅ `landing.html` - Mejorado `consultarImmigration()` para mostrar firmas legales
- ✅ `test_immigration.html` - Página de prueba dedicada para el bot
- ✅ `start_immigration_test.sh` - Script de inicio rápido

## 🚀 Cómo usar

### Opción 1: Inicio rápido con script
```bash
./start_immigration_test.sh
```

### Opción 2: Manual
```bash
# 1. Iniciar servidor
python3 app.py

# 2. Abrir en navegador
# - http://127.0.0.1:8000/ (landing principal)
# - test_immigration.html (página de prueba)
```

## 📡 Endpoints disponibles

### `/api/immigration` (POST)
Bot especializado en visados, NIE y documentación para extranjeros.

**Request:**
```json
{
  "message": "¿Qué necesito para mudarme desde USA?",
  "language": "es"
}
```

**Response:**
```json
{
  "message": "📋 **Información de Visado para USA**...",
  "legal_ads": [
    {
      "nombre": "Klev&Vera International Law Firm",
      "contacto": "info@klevvera.com",
      "descripcion": "Abogados especializados en inmigración...",
      "beneficios": ["Abogados inglés-parlantes", "..."],
      "precio": "€150-300 / hora",
      "idiomas": "Inglés, Español, Ruso",
      "ubicacion": "Barcelona",
      "es_anunciante": true
    }
  ],
  "type": "immigration",
  "language": "es"
}
```

### `/api/immigration/health` (GET)
Health check del bot de inmigración.

## 🎯 Características implementadas

### 1. Carga dinámica de anunciantes
El bot carga automáticamente las firmas legales desde `data/anunciantes.json`:
- Filtra por categoría "Legal and Financial"
- Prioriza los que tienen `es_anunciante: true`
- Máximo 3 firmas mostradas

### 2. Frontend mejorado
El frontend ahora muestra:
- **Mensaje principal** del bot con información de visados/NIE
- **Tarjetas de firmas legales** con:
  - Nombre y descripción
  - Contacto y precio
  - Idiomas disponibles
  - Ubicación
  - Lista de beneficios
  - FAQ (si existe)

### 3. Soporte multiidioma
- Español (`es`)
- Inglés (`en`)

### 4. Países soportados
El bot tiene información detallada de:
- **América:** USA, Canadá, Argentina, Colombia, México, Brasil
- **Europa:** Reino Unido, Alemania, Francia, Italia, Países Bajos, Portugal, Suiza, Noruega, Irlanda
- **Asia-Pacífico:** Australia, Nueva Zelanda, China, India

## 🔧 Pruebas

### Test con curl
```bash
curl -X POST http://127.0.0.1:8000/api/immigration \
  -H "Content-Type: application/json" \
  -d '{"message": "info sobre USA", "language": "es"}'
```

### Test con Python
```python
from routes.immigration_api import immigration_api
from flask import Flask

app = Flask(__name__)
app.register_blueprint(immigration_api)

with app.test_client() as client:
    response = client.post('/api/immigration',
                          json={'message': 'info sobre USA', 'language': 'es'})
    print(response.get_json())
```

## 📁 Archivos modificados

```
/home/fleet/Escritorio/Revista-expats-ai/
├── app.py                          # ✏️ Registrado immigration_api blueprint
├── routes/
│   └── immigration_api.py          # 🆕 Nuevo endpoint /api/immigration
├── bots/
│   └── bot_immigration.py          # ✏️ Carga dinámica de anunciantes
├── landing.html                    # ✏️ Mejorado consultarImmigration()
├── test_immigration.html           # 🆕 Página de prueba dedicada
├── start_immigration_test.sh       # 🆕 Script de inicio rápido
└── IMMIGRATION_FRONTEND.md         # 🆕 Esta documentación
```

## 🎨 Captura del frontend

El frontend muestra:

```
┌─────────────────────────────────────────┐
│ Tu pregunta: [¿Qué necesito para...?]  │
│ Idioma: [Español ▼]                    │
│ [Consultar]                            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 📋 Información de Visado para USA      │
│                                         │
│ 🎫 Visado: No requerido (90 días)      │
│ ⏱️ Duración: 90 días                   │
│ 🆔 NIE: Sí, para residencia...         │
│ ...                                     │
│                                         │
│ 🤝 Recomendamos consultar con un       │
│ profesional en leyes de extranjería    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 📋 Firmas Anunciantes en la Revista    │
│                                         │
│ ┌───────────────────────────────────┐  │
│ │ Klev&Vera International Law Firm  │  │
│ │ Abogados especializados en...     │  │
│ │ 📞 info@klevvera.com              │  │
│ │ 💰 €150-300 / hora                │  │
│ │ 🗣️ Inglés, Español, Ruso          │  │
│ │ 📍 Barcelona                       │  │
│ │ ✨ Beneficios:                     │  │
│ │   • Abogados inglés-parlantes     │  │
│ │   • Experiencia internacional     │  │
│ │   • Consulta inicial gratuita     │  │
│ └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## 🎯 Próximos pasos (opcional)

- [ ] Añadir más firmas legales a `data/anunciantes.json`
- [ ] Implementar filtros por país en el frontend
- [ ] Agregar chat widget persistente para inmigración
- [ ] Integrar con el orquestador principal para consultas mixtas
- [ ] Analytics de consultas más frecuentes

## 📞 Soporte

Si tienes problemas:
1. Verifica que el servidor esté corriendo: `curl http://127.0.0.1:8000/api/immigration/health`
2. Revisa los logs del servidor
3. Verifica que `data/anunciantes.json` existe y tiene la categoría "Legal and Financial"
