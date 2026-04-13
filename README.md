# Revista Expats AI
# Revista Expats AI

**Revista digital inteligente para expatriados en Barcelona.**

Plataforma full-stack con frontend web completo, asistente de chat integrado y bots especializados por categoría (alojamiento, salud, legal, educación, inmigración y más). Desplegada en Render con sincronización automática de contenido RSS.

🌐 **Demo en vivo:** [https://revista-expats-ai.onrender.com](https://revista-expats-ai.onrender.com)

---

## ✨ Características

- **Frontend web completo** — revista digital con secciones de artículos, guías y servicios
- **Asistente de chat** — widget integrado que entiende preguntas en español e inglés
- **Bots especializados** — 9 bots independientes (alojamiento, salud, legal, educación, trabajo, inmigración, restaurantes, comercial y más)
- **Directorio de anunciantes** — integración con directorio de Barcelona Metropolitan
- **RSS automático** — sincronización de artículos cada 6 horas
- **Dashboard de métricas** — panel interno con exportación CSV/JSON/HTML
- **Rate limiting y CORS** — protección de API en producción
- **Despliegue en Render** — configurado con `render.yaml` para auto-deploy desde GitHub

---

## 🚀 Instalación local

```bash
git clone https://github.com/FABJAH/revista-expat-ai.git
cd revista-expat-ai
python3 -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt  # incluye torch para clasificación semántica ML
uvicorn main:app --reload --port 8000
```

Abre `http://127.0.0.1:8000` — el frontend se sirve automáticamente.

> **Nota:** `requirements.txt` incluye `torch` y `sentence-transformers` para clasificación semántica avanzada. Para producción/Render se usa `requirements-prod.txt` (sin ML, clasificación por palabras clave).

---

## 🌐 Despliegue en Render

El repositorio incluye `render.yaml` preconfigurado. Para desplegar:

1. Conecta este repositorio en [render.com](https://render.com)
2. Render detecta `render.yaml` automáticamente y usa `requirements-prod.txt`
3. Cada push a `main` dispara un re-despliegue automático

---

## 📁 Estructura del proyecto

```
revista-expat-ai/
├── frontend/                # Frontend web (servido en /)
│   ├── index.html           # Página principal de la revista
│   ├── script.js            # Chat widget + lógica de la UI
│   ├── styles.css           # Estilos
│   └── assets/images/       # Imágenes de artículos
├── bots/
│   ├── orchestrator.py      # Clasificador de intención + router
│   ├── bot_immigration.py   # Bot de inmigración y visados
│   ├── bot_healthcare.py    # Bot de salud
│   ├── bot_legal.py         # Bot legal y financiero
│   ├── bot_education.py     # Bot de educación
│   ├── bot_accommodation.py # Bot de alojamiento
│   ├── bot_work.py          # Bot de empleo
│   ├── bot_service.py       # Bot de servicios
│   ├── bot_comercial.py     # Bot comercial/publicidad
│   ├── rss_manager.py       # Gestor de feeds RSS
│   └── directory_connector.py # Conector directorio BM
├── widget/                  # Widget Luna (embebible)
├── routes/                  # Rutas adicionales de la API
├── data/
│   ├── anunciantes.json     # Base de datos de anunciantes
│   └── guides/              # Guías editoriales JSON
├── main.py                  # Servidor FastAPI principal
├── metrics_storage.py       # Almacenamiento SQLite de métricas
├── dashboard.html           # Dashboard interno de métricas
├── render.yaml              # Configuración de despliegue Render
├── requirements.txt         # Deps local (con ML)
└── requirements-prod.txt    # Deps producción (sin torch)
```

---

## 🤖 Bots disponibles

| Bot | Categoría | Descripción |
|-----|-----------|-------------|
| `bot_immigration` | Inmigración | NIE, visados, empadronamiento, residencia |
| `bot_healthcare` | Salud | Médicos, clínicas, seguros, farmacias |
| `bot_legal` | Legal y financiero | Abogados, gestorías, bancos, impuestos |
| `bot_education` | Educación | Escuelas, idiomas, universidades, cursos |
| `bot_accommodation` | Alojamiento | Pisos, alquiler, barrios, agencias |
| `bot_work` | Empleo | Trabajo, networking, CV, sectores |
| `bot_service` | Servicios bot | Chatbots personalizados para negocios |
| `bot_comercial` | Comercial | Publicidad en la revista |
| Generic | Resto | Restaurantes, ocio, retail, cultura |

---

## 📊 API principal

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Frontend web principal |
| `/api/query` | POST | Consulta al asistente |
| `/api/status` | GET | Estado del servidor |
| `/api/metrics` | GET | Métricas en tiempo real |
| `/api/export/metrics` | GET | Exportar métricas (CSV/JSON/HTML) |
| `/dashboard` | GET | Dashboard interno |
| `/docs` | GET | Documentación Swagger automática |

---

## 🛠️ Tecnologías

- **Backend:** FastAPI, Uvicorn, APScheduler, SlowAPI
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Datos:** SQLite (métricas), JSON (anunciantes/guías), RSS feeds
- **ML (opcional local):** sentence-transformers, torch — clasificación semántica de intenciones
- **Despliegue:** Render (render.yaml)


