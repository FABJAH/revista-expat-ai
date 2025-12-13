# bots/bot_healthcare.py
from .utils import filter_advertisers_by_keywords
from .maps_integration import search_healthcare_barcelona

def responder_consulta(pregunta, anunciantes, language="en"):
    """
    Responde a consultas sobre salud.
    PRIORIDAD 1: Anunciantes pagos (siempre primero)
    PRIORIDAD 2: Resultados de Google Maps/Nominatim (complemento gratuito)
    """
    keywords = [
        "medico", "hospital", "clinica", "dentista", "seguro", "salud",
        "doctor", "pediatra", "ginecologo", "farmacia", "urgencias",
        "especialista", "psicologo", "terapia", "clinic", "dentist",
        "insurance", "health", "pediatrician", "gynecologist", "pharmacy",
        "emergency", "specialist", "psychologist", "therapy"
    ]

    # 1. PRIMERO: Filtrar anunciantes pagos
    selected_advertisers = filter_advertisers_by_keywords(pregunta, anunciantes, keywords)

    # Marcar anunciantes como pagos para que el frontend los destaque
    for advertiser in selected_advertisers:
        advertiser["es_anunciante"] = True

    # 2. SEGUNDO: Si hay pocos anunciantes (menos de 3), complementar con resultados de Maps
    if len(selected_advertisers) < 3:
        # Determinar qué buscar según la pregunta
        search_term = "hospital"
        pregunta_lower = pregunta.lower()

        if any(word in pregunta_lower for word in ["dentista", "dental", "dentist"]):
            search_term = "dentist"
        elif any(word in pregunta_lower for word in ["farmacia", "pharmacy"]):
            search_term = "pharmacy"
        elif any(word in pregunta_lower for word in ["clinica", "clinic", "centro medico"]):
            search_term = "clinic"
        elif any(word in pregunta_lower for word in ["urgencia", "emergency", "emergencia"]):
            search_term = "emergency hospital"

        # Buscar en Maps
        maps_results = search_healthcare_barcelona(search_term, limit=5)

        # Agregar resultados de Maps DESPUÉS de los anunciantes
        selected_advertisers.extend(maps_results)

    # Extraer puntos clave de los 2 mejores resultados (priorizando anunciantes)
    key_points = []
    for advertiser in selected_advertisers[:2]:
        point = {
            "nombre": advertiser.get("nombre"),
            "descripcion": advertiser.get("descripcion"),
            "beneficios": advertiser.get("beneficios", [])
        }
        key_points.append(point)

    return {"key_points": key_points, "json_data": selected_advertisers}
