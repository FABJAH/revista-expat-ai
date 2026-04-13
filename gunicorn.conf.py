import os

# Render requiere bind en 0.0.0.0 y puerto dinámico ($PORT)
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"

# FastAPI es ASGI; con este worker gunicorn funciona correctamente
worker_class = "uvicorn.workers.UvicornWorker"
workers = int(os.getenv("WEB_CONCURRENCY", "1"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "120"))
