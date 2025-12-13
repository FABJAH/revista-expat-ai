# bots/maps_integration.py
"""
Integración con APIs de mapas para buscar servicios locales.
Prioriza siempre los anunciantes pagos sobre los resultados gratuitos.
"""

import os
import requests
from typing import List, Dict

def search_healthcare_barcelona(query: str = "hospital", limit: int = 5) -> List[Dict]:
    """
    Busca servicios de salud en Barcelona usando Nominatim (OpenStreetMap).
    API gratuita, sin necesidad de clave. Alternativa a Google Places.

    Args:
        query: Tipo de servicio (hospital, clinic, pharmacy, etc.)
        limit: Número máximo de resultados

    Returns:
        Lista de diccionarios con información de los lugares
    """
    try:
        # Nominatim API (OpenStreetMap) - No requiere API key
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"{query} Barcelona Spain",
            "format": "json",
            "limit": limit,
            "addressdetails": 1,
            "extratags": 1
        }
        headers = {
            "User-Agent": "RevistaExpatsAI/1.0 (contact@revistaexpats.com)"
        }

        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Formatear resultados al formato de anunciantes
        formatted_results = []
        for place in data:
            result = {
                "nombre": place.get("display_name", "").split(",")[0],
                "descripcion": f"Servicio médico encontrado en {place.get('address', {}).get('suburb', 'Barcelona')}",
                "contacto": "Información disponible en Google Maps",
                "beneficios": ["Servicio público/privado", "Ubicación verificada"],
                "precio": "Consultar tarifas",
                "idiomas": "Consultar disponibilidad",
                "ubicacion": place.get("display_name", "Barcelona"),
                "lat": place.get("lat"),
                "lon": place.get("lon"),
                "es_anunciante": False  # Marca para distinguir de anunciantes pagos
            }
            formatted_results.append(result)

        return formatted_results

    except Exception as e:
        print(f"⚠️  Error buscando en Maps: {e}")
        return []


def search_google_places(query: str, location: str = "Barcelona, Spain") -> List[Dict]:
    """
    Busca en Google Places API (requiere API key).
    Esta es la versión premium si quieres integrarla después.

    Configuración:
    1. Obtén una API key en: https://console.cloud.google.com/
    2. Activa Google Places API
    3. Configura la variable de entorno: GOOGLE_PLACES_API_KEY
    """
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    if not api_key:
        print("⚠️  Google Places API key no configurada. Usando Nominatim gratuito.")
        return search_healthcare_barcelona(query)

    try:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": f"{query} in {location}",
            "key": api_key,
            "language": "es"
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = []
        for place in data.get("results", [])[:5]:
            result = {
                "nombre": place.get("name"),
                "descripcion": f"Ubicado en {place.get('formatted_address', 'Barcelona')}",
                "contacto": "Ver en Google Maps para más detalles",
                "beneficios": ["Valoración: " + str(place.get("rating", "N/A"))],
                "precio": "Consultar tarifas",
                "idiomas": "Consultar disponibilidad",
                "ubicacion": place.get("formatted_address", "Barcelona"),
                "es_anunciante": False
            }
            results.append(result)

        return results

    except Exception as e:
        print(f"⚠️  Error con Google Places: {e}")
        return search_healthcare_barcelona(query)
