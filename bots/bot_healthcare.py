# bots/bot_healthcare.py
from .utils import filter_advertisers_by_keywords

def responder_consulta(pregunta, anunciantes, language="en"):
    """
    Responde a consultas sobre salud utilizando la función de filtrado central.
    """
    keywords = [
        "medico", "hospital", "clinica", "dentista", "seguro", "salud",
        "doctor", "pediatra", "ginecologo", "farmacia", "urgencias",
        "especialista", "psicologo", "terapia", "clinic", "dentist",
        "insurance", "health", "pediatrician", "gynecologist", "pharmacy",
        "emergency", "specialist", "psychologist", "therapy"
    ]

    selected_advertisers = filter_advertisers_by_keywords(pregunta, anunciantes, keywords)

    key_points = []
    for advertiser in selected_advertisers[:2]:
        point = {
            "nombre": advertiser.get("nombre"),
            "descripcion": advertiser.get("descripcion"),
            "beneficios": advertiser.get("beneficios", [])
        }
        key_points.append(point)

    return {"key_points": key_points, "json_data": selected_advertisers}
