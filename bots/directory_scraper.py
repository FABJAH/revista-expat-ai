# bots/directory_scraper.py
"""
Scraper del directorio de Barcelona Metropolitan
Se usa si NO existe API REST de Barcelona Metropolitan.
Scrapea el sitio web y cachea los resultados.
"""

from bs4 import BeautifulSoup
import requests
from typing import List, Dict, Optional
import json
from pathlib import Path
from datetime import datetime, timedelta
from .logger import logger


class DirectoryScraper:
    """
    Scrapea el directorio de Barcelona Metropolitan.
    Cachea resultados para no sobrecargar el sitio.
    """

    def __init__(self, base_url: str = "https://www.barcelona-metropolitan.com"):
        self.base_url = base_url

        base_dir = Path(__file__).resolve().parent.parent
        self.cache_file = base_dir / "data" / "directory_cache.json"
        self.cache_hours = 24

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        logger.info(f"DirectoryScraper inicializado con URL: {base_url}")

    def get_advertisers(self, category: str = None) -> List[Dict]:
        """
        Obtiene anunciantes del directorio.

        Args:
            category: Filtrar por categoría (opcional)

        Returns:
            Lista de anunciantes
        """
        # Intentar cargar desde cache
        cached = self._load_cache()
        if cached:
            if category:
                return [a for a in cached if a.get('category') == category]
            return cached

        # Si no hay cache válido, scrapear
        return self._scrape_and_cache()

    def _load_cache(self) -> Optional[List[Dict]]:
        """
        Carga cache si existe y es reciente.
        """
        if not self.cache_file.exists():
            return None

        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cache_time = datetime.fromisoformat(
                    data.get('timestamp', '2020-01-01')
                )

                # Verificar si cache sigue siendo válido
                if datetime.now() - cache_time < timedelta(hours=self.cache_hours):
                    advertisers = data.get('advertisers', [])
                    logger.info(
                        f"✅ Cache válido: {len(advertisers)} anunciantes"
                    )
                    return advertisers

            logger.info("⚠️ Cache expirado, scrapeando nuevo")
            return None

        except Exception as e:
            logger.warning(f"⚠️ Error cargando cache: {e}")
            return None

    def _scrape_and_cache(self) -> List[Dict]:
        """
        Scrapea el directorio y lo cachea.

        NOTA: Los selectores CSS necesitan ajustarse según la estructura
        HTML real de Barcelona Metropolitan.
        """
        try:
            logger.info("🔄 Scrapeando directorio de Barcelona Metropolitan...")

            # URL del directorio (ajustar según URL real)
            directory_url = f"{self.base_url}/directory"

            response = requests.get(
                directory_url,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            advertisers = []

            # ============================================
            # IMPORTANTE: Ajustar selectores según HTML real
            # ============================================
            # Ejemplo de selectores (ESTOS SON HIPOTÉTICOS)
            # Necesitas inspeccionar el HTML real y ajustar:
            # - '.directory-listing' → clase real del contenedor
            # - '.business-name' → clase del nombre
            # - '.category' → clase de categoría
            # etc.

            listings = soup.select('.directory-listing')  # AJUSTAR

            for listing in listings:
                try:
                    advertiser = {
                        'id': listing.get('data-id', ''),
                        'nombre': listing.select_one('.business-name')?.text.strip(),
                        'descripcion': listing.select_one('.description')?.text.strip(),
                        'categoria': listing.select_one('.category')?.text.strip(),
                        'contacto': listing.select_one('.phone')?.text.strip(),
                        'email': listing.select_one('.email')?.text.strip(),
                        'website': listing.select_one('a.website')?.get('href'),
                        'direccion': listing.select_one('.address')?.text.strip(),
                        'url_directorio': f"{self.base_url}{listing.select_one('a')?.get('href')}",
                        'scraped_at': datetime.now().isoformat()
                    }

                    # Solo agregar si tiene datos válidos
                    if advertiser['nombre']:
                        advertisers.append(advertiser)

                except Exception as e:
                    logger.warning(f"⚠️ Error parseando anunciante: {e}")
                    continue

            # Guardar en cache
            self._save_cache(advertisers)

            logger.info(f"✅ Scraping completado: {len(advertisers)} anunciantes")
            return advertisers

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error HTTP scrapeando: {e}")
            return self._load_fallback()
        except Exception as e:
            logger.error(f"❌ Error scrapeando directorio: {e}")
            return self._load_fallback()

    def _save_cache(self, advertisers: List[Dict]) -> bool:
        """Guarda anunciantes en cache."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'advertisers': advertisers,
                    'source': 'scraper'
                }, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            logger.error(f"❌ Error guardando cache: {e}")
            return False

    def _load_fallback(self) -> List[Dict]:
        """Fallback a anunciantes.json si falla el scraping."""
        try:
            logger.info("📄 Usando fallback a anunciantes.json local")

            base_dir = Path(__file__).resolve().parent.parent
            data_path = base_dir / "data" / "anunciantes.json"

            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Aplanar estructura
            all_advertisers = []
            for category, items in data.items():
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            item['category'] = category
                            all_advertisers.append(item)

            logger.info(f"✅ Fallback cargado: {len(all_advertisers)} anunciantes")
            return all_advertisers

        except Exception as e:
            logger.error(f"❌ Error en fallback: {e}")
            return []

    def search(self, query: str, category: str = None) -> List[Dict]:
        """Busca anunciantes localmente."""
        try:
            all_advertisers = self.get_advertisers(category)
            query_lower = query.lower()

            results = []
            for advertiser in all_advertisers:
                nombre = str(advertiser.get('nombre', '')).lower()
                descripcion = str(advertiser.get('descripcion', '')).lower()

                if query_lower in nombre or query_lower in descripcion:
                    results.append(advertiser)

            logger.info(f"✅ Búsqueda local: {len(results)} resultados")
            return results

        except Exception as e:
            logger.error(f"❌ Error en búsqueda: {e}")
            return []


# Instancia global del scraper
_directory_scraper = None


def get_directory_scraper(base_url: str = None) -> DirectoryScraper:
    """
    Obtiene la instancia global del DirectoryScraper.
    """
    global _directory_scraper
    if _directory_scraper is None:
        _directory_scraper = DirectoryScraper(
            base_url=base_url or "https://www.barcelona-metropolitan.com"
        )
    return _directory_scraper
