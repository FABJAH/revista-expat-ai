"""
Configuración centralizada para la aplicación usando Pydantic BaseSettings.
Variables de entorno toman precedencia sobre valores por defecto.
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración global de la aplicación."""

    # Servidor
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    # Paginación
    PAGE_SIZE_DEFAULT: int = 5
    PAGE_SIZE_MAX: int = 50

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "https://www.barcelona-metropolitan.com",
        "https://barcelona-metropolitan.com",
        "http://localhost:5500",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:3000",
    ]

    # RSS/Feeds
    FEED_URLS: List[str] = [
        "https://www.barcelona-metropolitan.com/directory/index.rss",
    ]
    RSS_SYNC_HOURS: int = 6
    RSS_LIMIT_PER_FEED: int = 50
    RSS_MAX_ARTICLES: int = 1000

    # Clasificación semántica
    SEMANTIC_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    CONFIDENCE_THRESHOLD: float = 0.2
    KEYWORD_CONFIDENCE_MULTIPLIER: float = 0.15
    KEYWORD_BASE_CONFIDENCE: float = 0.25

    # Bots
    MAX_KEY_POINTS: int = 2
    MAX_ADVERTISERS_PER_QUERY: int = 3

    # Datos
    DATA_DIR: str = "data"
    GUIDES_DIR: str = "data/guides"
    CACHE_DIR: str = "data/cache"
    ANUNCIANTES_FILE: str = "data/anunciantes.json"
    ARTICLES_CACHE_FILE: str = "data/cache/articles.json"
    ANALYTICS_DIR: str = "data/analytics"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instancia global de settings
settings = Settings()
