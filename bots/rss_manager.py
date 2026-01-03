"""
RSS Feed Manager: parsea feeds de la revista y cachea artículos localmente.
Actualiza cada 6-12 horas en background.
"""

import json
import feedparser
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from .logger import logger
import socket

# OPTIMIZACIÓN: Timeout global para feedparser (evita colgarse indefinidamente)
socket.setdefaulttimeout(10)

class RSSManager:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.cache_dir = self.base_dir / "data" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.articles_cache = self.cache_dir / "articles.json"

        # URLs de feeds a parsear (Barcelona Metropolitan)
        self.feed_urls = [
            "https://www.barcelona-metropolitan.com/directory/index.rss",  # Directorio
            # Opcionales en el futuro:
            # "https://www.barcelona-metropolitan.com/feed",  # Blog/artículos
            # "https://www.barcelona-metropolitan.com/topics/best-of/feed",
        ]

        self.articles = self.load_cache()
        logger.info(f"RSS Manager inicializado. {len(self.articles)} artículos en caché.")

    def load_cache(self) -> List[Dict]:
        """Carga artículos desde caché local."""
        if self.articles_cache.exists():
            try:
                with open(self.articles_cache, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error cargando caché: {e}")
        return []

    def save_cache(self):
        """Persiste artículos en caché local."""
        try:
            with open(self.articles_cache, 'w', encoding='utf-8') as f:
                json.dump(self.articles, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error guardando caché: {e}")

    def sync_feeds(self) -> int:
        """
        Parsea todos los feeds y actualiza caché.
        Retorna número de artículos nuevos/actualizados.
        """
        new_count = 0
        existing_urls = {a.get('url') for a in self.articles}

        for feed_url in self.feed_urls:
            try:
                logger.info(f"Parseando feed: {feed_url}")
                feed = feedparser.parse(feed_url)

                # Validar que el feed se parseó correctamente
                if not feed.entries:
                    logger.warning(f"Feed vacío o no accesible: {feed_url}")
                    continue

                entries_count = 0
                for entry in feed.entries[:50]:  # Limitar a últimos 50 por feed
                    article = {
                        "url": entry.get('link', '') or entry.get('id', ''),
                        "title": entry.get('title', 'Sin título'),
                        "description": entry.get('summary', entry.get('description', ''))[:500],  # Primeros 500 chars
                        "published": entry.get('published', entry.get('updated', '')),
                        "categories": [t.get('term') if isinstance(t, dict) else str(t)
                                      for t in entry.get('tags', [])],
                        "source": feed.feed.get('title', 'Barcelona Metropolitan'),
                        "synced_at": datetime.utcnow().isoformat()
                    }

                    # Evitar duplicados
                    if article['url'] and article['url'] not in existing_urls:
                        self.articles.append(article)
                        existing_urls.add(article['url'])
                        new_count += 1
                        entries_count += 1

                logger.info(f"Feed '{feed.feed.get('title', 'Unknown')}': {entries_count} nuevas entradas parseadas.")

            except Exception as e:
                logger.error(f"Error parseando {feed_url}: {e}")

        # Limitar a últimos 1000 artículos para no crecer indefinidamente
        if len(self.articles) > 1000:
            self.articles = sorted(self.articles, key=lambda x: x.get('synced_at', ''), reverse=True)[:1000]

        self.save_cache()
        logger.info(f"Sync completado: {new_count} artículos nuevos. Total: {len(self.articles)}")
        return new_count

    def search_articles(self, keywords: List[str], limit: int = 5) -> List[Dict]:
        """
        Busca artículos por palabras clave.
        Retorna los más relevantes ordenados por matches.
        OPTIMIZADO: Pre-procesa texto una vez, early exit cuando encuentra suficientes matches
        """
        if not keywords or not self.articles:
            return []

        keyword_set = {kw.lower() for kw in keywords if len(kw) > 2}
        if not keyword_set:
            return []

        scored = []
        # OPTIMIZACIÓN: Limitar búsqueda a últimos 500 artículos (más recientes)
        recent_articles = self.articles[-500:] if len(self.articles) > 500 else self.articles

        for article in recent_articles:
            # OPTIMIZACIÓN: Caché de texto procesado (podría mejorarse más con un índice invertido)
            if 'cached_search_text' not in article:
                categories_text = ' '.join([t.get('term', '') if isinstance(t, dict) else str(t) for t in article.get('categories', [])])
                article['cached_search_text'] = f"{article.get('title', '')} {article.get('description', '')} {categories_text}".lower()

            text = article['cached_search_text']
            score = sum(1 for kw in keyword_set if kw in text)
            if score > 0:
                scored.append((score, article))

        # Ordenar por score descendente
        scored.sort(key=lambda x: x[0], reverse=True)
        return [article for _, article in scored[:limit]]

    def get_articles_by_category(self, category: str, limit: int = 3) -> List[Dict]:
        """
        Retorna artículos de una categoría específica (mapeo manual).
        """
        category_keywords = {
            "Legal and Financial": ["legal", "visa", "nie", "impuesto", "contrato", "bank", "immigration"],
            "Healthcare": ["salud", "doctor", "hospital", "dentista", "health", "medical", "clinic"],
            "Education": ["escuela", "colegio", "university", "idioma", "course", "school", "education"],
            "Accommodation": ["alojamiento", "hotel", "apartamento", "vivienda", "housing", "apartment", "rent"],
            "Restaurants": ["restaurante", "comida", "food", "restaurant", "dining", "cuisine"],
            "Arts and Culture": ["arte", "cultura", "museo", "gallery", "culture", "exhibition"],
            "Work and Networking": ["trabajo", "empleo", "job", "networking", "business", "work"],
        }

        keywords = category_keywords.get(category, [])
        return self.search_articles(keywords, limit)

# Instancia global
_rss_manager: Optional[RSSManager] = None

def get_rss_manager() -> RSSManager:
    """Singleton para acceso al RSS Manager."""
    global _rss_manager
    if _rss_manager is None:
        _rss_manager = RSSManager()
    return _rss_manager
