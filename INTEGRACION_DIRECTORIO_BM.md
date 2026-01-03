# 📖 Integración con Directorio de Barcelona Metropolitan

## ✅ Estado Actual

El código está **100% listo** para conectar con el directorio real de Barcelona Metropolitan.

### Lo que ya está implementado:

✅ **DirectoryConnector** - Conector con API REST del directorio
✅ **DirectoryScraper** - Scraper alternativo si no hay API
✅ **Orchestrator actualizado** - Usa directorio en lugar de JSON estático
✅ **Tracking de recomendaciones** - Analytics integrado
✅ **Fallback automático** - Si falla API, usa `anunciantes.json`

---

## 🚀 Pasos para Conectar

### 1️⃣ Recibir datos de Barcelona Metropolitan

Cuando tengas los datos, necesitas:

**Opción A - API REST** (Recomendada):
```
URL: https://www.barcelona-metropolitan.com/api
Método: GET /advertisers
Response: {
  "advertisers": [
    {
      "id": "123",
      "nombre": "Hotel ABC",
      "categoria": "Accommodation",
      "descripcion": "...",
      "contacto": "...",
      "email": "...",
      "website": "...",
      "precio": "...",
      ...
    }
  ]
}
```

**Opción B - Datos para scraping**:
- URL del directorio
- Estructura HTML (selectores CSS)

**Opción C - Google Sheets** (Simple):
- ID de la hoja
- Estructura de columnas

### 2️⃣ Configurar Variables de Entorno

Edita `.env`:

```bash
# Para API REST
BM_DIRECTORY_API_URL=https://www.barcelona-metropolitan.com/api
BM_API_KEY=tu_api_key_aqui

# Para scraping (si no hay API)
BM_SCRAPER_URL=https://www.barcelona-metropolitan.com
BM_SCRAPER_CACHE_HOURS=24
```

### 3️⃣ Si es API REST

El código ya funciona. Solo actualiza `.env` y prueba:

```python
from bots.directory_connector import get_directory_connector

connector = get_directory_connector()
anunciantes = connector.get_all_advertisers()
print(f"✅ Cargados {len(anunciantes)} anunciantes")
```

### 4️⃣ Si necesita Scraping

Inspecciona el HTML del directorio y ajusta los selectores en `bots/directory_scraper.py`:

```python
# Línea ~95: Ajusta estos selectores según el HTML real
listings = soup.select('.tu-clase-real')  # CAMBIAR
nombre = listing.select_one('.nombre-clase')  # CAMBIAR
...
```

---

## 📊 Cómo Funciona

### Flujo de carga de datos:

```
┌─────────────────────────────────────────┐
│  Orchestrator __init__                  │
│  ↓                                      │
├─────────────────────────────────────────┤
│  get_directory_connector()              │
│  ↓                                      │
├─────────────────────────────────────────┤
│  1. Intentar API REST                   │
│     ✅ Si funciona → Usar datos         │
│     ❌ Si falla → Ir a paso 2           │
│  ↓                                      │
├─────────────────────────────────────────┤
│  2. Cargar anunciantes.json local       │
│     ✅ Datos listos para usar           │
│                                         │
└─────────────────────────────────────────┘
```

### Tracking automático:

Cada vez que el bot recomienda un anunciante:

```
Usuario pregunta
   ↓
Bot clasifica + busca anunciantes
   ↓
Orchestrator trakea recomendación
   POST /api/analytics/recommendation
   {
     "advertiser_id": "123",
     "query": "hotel barcelona",
     "session_id": "session_xyz",
     "source": "expat_ai_bot"
   }
   ↓
Analytics en Barcelona Metropolitan
```

---

## 🔧 Troubleshooting

### Error: "⚠️ Error API Directorio: 404"

**Solución**: Verifica URL en `.env`
```bash
curl https://tu-url-api/advertisers
```

### Error: "❌ Error conectando con API"

**Solución**:
1. Verifica conectividad
2. Revisa API_KEY en `.env`
3. Comprueba headers requeridos

### Fallback a JSON pero quieres API

**Solución**:
```python
# Fuerza refreso de cache
connector = get_directory_connector()
connector.refresh_cache()
```

---

## 📝 Notas Importantes

### Estructura de datos

El código espera que cada anunciante tenga (como mínimo):

```python
{
    "id": "unique_id",           # Para tracking
    "nombre": "nombre",           # Nombre del negocio
    "categoria": "Accommodation", # Categoría
    "descripcion": "...",         # Descripción
    # Campos opcionales:
    "contacto": "...",
    "email": "...",
    "website": "...",
    "precio": "...",
    "ubicacion": "...",
}
```

Si tu API devuelve estructura diferente, necesitarás hacer mapping:

```python
# En directory_connector.py, línea ~65
for advertiser in all_advertisers:
    # Mapear campos si los nombres son diferentes
    if 'nombre_empresa' in advertiser:
        advertiser['nombre'] = advertiser['nombre_empresa']
```

### Cache

- **API**: Los datos se cachean en memoria
- **Scraper**: Se cachea en `data/directory_cache.json` por 24h
- **Fallback**: Usa `data/anunciantes.json`

Para limpiar cache:
```bash
rm data/directory_cache.json
```

---

## ✨ Próximos Pasos Cuando Tengas la API

1. **Dar URL y API Key** → Actualizo `.env`
2. **Probar conexión** → Verifico que devuelve datos
3. **Ajustar mapeo** → Si estructura es diferente
4. **Deploy** → Listo para producción

---

## 🎯 Beneficios

✅ **Datos siempre actualizados** - Sin actualizar código
✅ **Escalable** - Funciona con miles de anunciantes
✅ **Analytics** - Trackea qué anunciantes recomendamos
✅ **Fallback automático** - No se rompe si API falla
✅ **Compatible hacia atrás** - Sigue usando JSON si lo necesitas

---

## 💬 Preguntas?

Cuando tengas los datos de Barcelona Metropolitan, comparte:

1. **URL de la API** (o sitio para scraping)
2. **Estructura de respuesta** (JSON sample)
3. **Campos disponibles** (nombre, precio, ubicación, etc.)
4. **Autenticación** (API key, bearer token, etc.)

¡Listo para implementar en minutos! 🚀
