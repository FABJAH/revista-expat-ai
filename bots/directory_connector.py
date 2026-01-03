# bots/directory_connector.py
"""
Conector con el directorio real de Barcelona Metropolitan
Obtiene anunciantes desde la API real, fallback a JSON local
"""

import requests
from typing import List, Dict, Optional
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from .logger import logger


class DirectoryConnector:
    """
    Conecta con la API del directorio de Barcelona Metropolitan.
    Si la API no está disponible, usa anunciantes.json como fallback.
    """

    def __init__(self):
        # URLs y credenciales desde variables de entorno
        self.base_url = os.getenv(
            "BM_DIRECTORY_API_URL",
            "https://www.barcelona-metropolitan.com/api"
        )
        self.api_key = os.getenv("BM_API_KEY", "")
        self.timeout = 5
        self.max_retries = 2
        self.retry_delay = 1  # segundos

        # Cache local
        base_dir = Path(__file__).resolve().parent.parent
        self.cache_file = base_dir / "data" / "directory_cache.json"
        self.cache_hours = 24
        self.local_data_file = base_dir / "data" / "anunciantes.json"

        logger.info(
            f"DirectoryConnector inicializado con URL: {self.base_url}"
        )

    def get_all_advertisers(self, category: str = None,
                           limit: int = 50) -> List[Dict]:
        """
        Obtiene todos los anunciantes del directorio.

        Args:
            category: Filtrar por categoría (Healthcare, Legal, etc.)
            limit: Máximo de resultados

        Returns:
            Lista de anunciantes con todos sus datos
        """
        try:
            logger.info(
                f"Obteniendo anunciantes (categoría={category}, "
                f"limit={limit})"
            )

            # Intentar obtener del directorio real
            params = {"limit": limit}
            if category:
                params["category"] = category

            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            response = requests.get(
                f"{self.base_url}/advertisers",
                headers=headers,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                advertisers = data.get("advertisers", [])
                logger.info(
                    f"✅ Obtenidos {len(advertisers)} anunciantes de API"
                )
                return advertisers
            else:
                logger.warning(
                    f"⚠️ Error API Directorio: {response.status_code}"
                )
                return self._load_from_local()

        except requests.exceptions.Timeout:
            logger.warning(
                "⚠️ Timeout conectando con directorio (>5s)"
            )
            return self._load_from_local()
        except requests.exceptions.ConnectionError as e:
            logger.warning(
                f"⚠️ Error de conexión con API directorio: {e}"
            )
            return self._load_from_local()
        except Exception as e:
            logger.error(f"❌ Error conectando con API: {e}",
                        exc_info=True)
            return self._load_from_local()

    def search_advertisers(self, query: str, category: str = None, limit: int = 10) -> List[Dict]:
        """
        Busca anunciantes por keywords.

        Args:
            query: Término de búsqueda
            category: Categoría opcional
            limit: Máximo de resultados

        Returns:
            Lista de anunciantes que coinciden
        """
        try:
            logger.info(f"Buscando anunciantes: '{query}'")

            params = {"q": query, "limit": limit}
            if category:
                params["category"] = category

            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            response = requests.get(
                f"{self.base_url}/advertisers/search",
                headers=headers,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 200:
                results = response.json().get("results", [])
                logger.info(f"✅ Encontrados {len(results)} resultados para '{query}'")
                return results

            # Si falla API, hacer búsqueda local
            logger.info("Fallback a búsqueda local")
            return self._search_local(query, category)

        except Exception as e:
            logger.warning(f"⚠️ Error en búsqueda: {e}")
            return self._search_local(query, category)

    def get_advertiser_details(self, advertiser_id: str) -> Optional[Dict]:
        """
        Obtiene detalles completos de UN anunciante específico.

        Args:
            advertiser_id: ID del anunciante

        Returns:
            Diccionario con datos del anunciante
        """
        try:
            logger.info(f"Obteniendo detalles anunciante: {advertiser_id}")

            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            response = requests.get(
                f"{self.base_url}/advertisers/{advertiser_id}",
                headers=headers,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()

            return None

        except Exception as e:
            logger.warning(f"⚠️ Error obteniendo detalles: {e}")
            return None

    def get_by_category(self, category: str, limit: int = 50) -> List[Dict]:
        """
        Obtiene anunciantes por categoría.

        Args:
            category: Nombre de categoría
            limit: Máximo de resultados

        Returns:
            Lista de anunciantes de esa categoría
        """
        return self.get_all_advertisers(category=category, limit=limit)

    def track_recommendation(self, advertiser_id: str, query: str, session_id: str):
        """
        Notifica al directorio que el bot recomendó un anunciante.
        Útil para analytics y facturación.

        Args:
            advertiser_id: ID del anunciante recomendado
            query: Pregunta del usuario
            session_id: ID de sesión
        """
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            requests.post(
                f"{self.base_url}/analytics/recommendation",
                headers=headers,
                json={
                    "advertiser_id": advertiser_id,
                    "query": query,
                    "session_id": session_id,
                    "source": "expat_ai_bot",
                    "timestamp": datetime.now().isoformat()
                },
                timeout=3
            )
            logger.info(f"✅ Recomendación tracked: {advertiser_id}")
        except Exception as e:
            logger.debug(f"⚠️ No se pudo trackear recomendación: {e}")
            # No bloquear si falla el tracking
            pass

    def _load_from_local(self) -> List[Dict]:
        """
        Fallback: Carga anunciantes desde JSON local.
        """
        try:
            logger.info("📄 Usando anunciantes.json local como fallback")
            with open(self.local_data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Aplanar estructura (convertir dict por categorías a lista)
            all_advertisers = []
            for category, items in data.items():
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict):
                            item['category'] = category
                            all_advertisers.append(item)

            logger.info(f"✅ Cargados {len(all_advertisers)} anunciantes locales")
            return all_advertisers

        except Exception as e:
            logger.error(f"❌ Error cargando JSON local: {e}")
            return []

    def _search_local(self, query: str, category: str = None) -> List[Dict]:
        """
        Busca en anunciantes locales.
        """
        try:
            all_advertisers = self._load_from_local()
            query_lower = query.lower()

            results = []
            for advertiser in all_advertisers:
                # Filtrar por categoría si se especifica
                if category and advertiser.get('category') != category:
                    continue

                # Buscar en nombre y descripción
                nombre = str(advertiser.get('nombre', '')).lower()
                descripcion = str(advertiser.get('descripcion', '')).lower()

                if query_lower in nombre or query_lower in descripcion:
                    results.append(advertiser)

            logger.info(f"✅ Búsqueda local: {len(results)} resultados para '{query}'")
            return results

        except Exception as e:
            logger.error(f"❌ Error en búsqueda local: {e}")
            return []

    def refresh_cache(self) -> bool:
        """
        Fuerza actualización del cache de anunciantes.

        Returns:
            True si fue exitoso, False en caso contrario
        """
        try:
            logger.info("🔄 Refrescando cache de anunciantes...")
            advertisers = self.get_all_advertisers(limit=500)

            if advertisers:
                self.cache_file.parent.mkdir(parents=True, exist_ok=True)
                with open(self.cache_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'timestamp': datetime.now().isoformat(),
                        'advertisers': advertisers
                    }, f, ensure_ascii=False, indent=2)

                logger.info(f"✅ Cache refrescado: {len(advertisers)} anunciantes")
                return True

            return False

        except Exception as e:
            logger.error(f"❌ Error refrescando cache: {e}")
            return False


# Instancia global del conector
_directory_connector = None


def get_directory_connector() -> DirectoryConnector:
    """
    Obtiene la instancia global del DirectoryConnector.
    Patrón singleton para evitar múltiples conexiones.
    """
    global _directory_connector
    if _directory_connector is None:
        _directory_connector = DirectoryConnector()
    return _directory_connector
