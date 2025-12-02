# bots/bot_healthcare.py
from .utils import normalize

def responder_consulta(pregunta, anunciantes, language="en"):
    pregunta_norm = normalize(pregunta or "")
    keywords = [
        "medico","médico","doctor","hospital","clinica","clínica","dentista",
        "odontologia","pediatra","ginecologo","seguro","salud","insurance","clinic","health"
    ]

    matching, others = [], []
    for a in anunciantes or []:
        combined = ' '.join([str(a.get(k, '')) for k in ['nombre','descripcion','perfil','contacto','ubicacion']])
        cn = normalize(combined)
        found = any(kw in pregunta_norm or kw in cn for kw in keywords)
        (matching if found else others).append(a)

    selected = matching if matching else others

    # Extraer puntos clave de los 2 mejores resultados
    key_points = []
    for advertiser in selected[:2]:
        point = {
            "nombre": advertiser.get("nombre"),
            "descripcion": advertiser.get("descripcion"),
            "beneficios": advertiser.get("beneficios", [])
        }
        key_points.append(point)

    return {"key_points": key_points, "json_data": selected}
