import unicodedata
from typing import List, Dict
from config import settings


def build_key_points(advertisers: List[Dict], max_items: int = None) -> List[Dict]:
    """
    Extrae puntos clave (nombre, descripción, beneficios) de los primeros N anunciantes.
    Centraliza la lógica que antes se repetía en cada bot.

    Args:
        advertisers: Lista de anunciantes
        max_items: Número máximo de puntos clave (default: settings.MAX_KEY_POINTS)

    Returns:
        Lista de dicts con {nombre, descripcion, beneficios}
    """
    if max_items is None:
        max_items = settings.MAX_KEY_POINTS

    key_points = []
    for advertiser in advertisers[:max_items]:
        point = {
            "nombre": advertiser.get("nombre"),
            "descripcion": advertiser.get("descripcion"),
            "beneficios": advertiser.get("beneficios", [])
        }
        key_points.append(point)

    return key_points


def normalize(s):
    if not s:
        return ""
    s = str(s).strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()

def filter_advertisers_by_keywords(pregunta, anunciantes, keywords, search_fields=['nombre', 'descripcion', 'perfil', 'ubicacion']):
    """
    Función reutilizable para filtrar una lista de anunciantes.

    - Prioriza los anunciantes que coinciden con las palabras clave.
    - Si no hay coincidencias, devuelve el resto.
    """
    if not anunciantes:
        return []

    pregunta_norm = normalize(pregunta or "")

    matching, others = [], []
    for a in anunciantes:
        # Combina el contenido de los campos relevantes del anunciante en un solo texto
        combined_text = ' '.join([str(a.get(k, '')) for k in search_fields])
        combined_norm = normalize(combined_text)

        # Comprueba si alguna palabra clave está en la pregunta del usuario o en el texto del anunciante
        found = any(kw in pregunta_norm or kw in combined_norm for kw in keywords)
        (matching if found else others).append(a)
    # Ordenar priorizando anunciantes patrocinados/destacados
    def sponsor_key(item):
        flag = item.get('es_anunciante') or item.get('sponsored') or item.get('featured')
        return 1 if flag else 0

    if matching:
        matching.sort(key=sponsor_key, reverse=True)
        return matching
    else:
        others.sort(key=sponsor_key, reverse=True)
        return others
