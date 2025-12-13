# Revista Expats AI

Asistente virtual inteligente para expatriados en Barcelona con bots orquestadores especializados.

## 🚀 Instalación

1. **Clona el repositorio**
   ```bash
   git clone <tu-repo>
   cd Revista-expats-ai
   ```

2. **Crea y activa el entorno virtual**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Linux/Mac
   # .venv\Scripts\activate   # En Windows
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Ejecución

### Servidor principal (FastAPI + Frontend)
```bash
uvicorn main:app --reload --port 8000
```

Luego abre en tu navegador: `http://127.0.0.1:8000`

El frontend se sirve automáticamente desde la carpeta `frontend/`.

### Página de prueba de API
Abre `http://127.0.0.1:8000/landing.html` para probar la conexión con el backend.

## 📁 Estructura del Proyecto

```
Revista-expats-ai/
├── frontend/              # Frontend (HTML, CSS, JS)
│   ├── index.html        # Página principal
│   ├── script.js         # Lógica del chat
│   └── styles.css        # Estilos
├── bots/                 # Bots especializados
│   ├── orchestrator.py   # Orquestador principal
│   ├── bot_*.py          # Bots por categoría
│   └── utils.py          # Utilidades
├── data/                 # Base de datos
│   └── anunciantes.json  # Datos de anunciantes
├── main.py               # ⭐ Servidor principal FastAPI
├── landing.html          # Página de prueba de API
└── requirements.txt      # Dependencias

```

## 🤖 Bots Disponibles

- **Accommodation** - Alojamiento y vivienda
- **Healthcare** - Servicios médicos y salud
- **Legal and Financial** - Asesoría legal y financiera
- **Education** - Cursos, escuelas y universidades
- **Restaurants** - Gastronomía y restaurantes
- **Comercial** - Publicidad y marketing
- **BotService** - Chatbots personalizados

## 🛠️ Tecnologías

- **Backend**: FastAPI, Sentence Transformers, Torch
- **Frontend**: Vanilla JavaScript, CSS3
- **IA**: Clasificación semántica de intenciones con ML


