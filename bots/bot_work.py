from .utils import normalize


def responder_consulta(pregunta, anunciantes, language="en"):
    """Responde consultas sobre empleo y networking con formato estándar.

    - Filtra por términos relevantes (trabajo, empleo, oferta, coworking, networking).
    - Añade FAQs por defecto si faltan.
    - Devuelve JSON estandarizado y texto bilingüe.
    """
    pregunta_norm = normalize(pregunta or "")

    keywords = [
        "trabajo",
        "empleo",
        "oferta",
        "job",
        "vacante",
        "coworking",
        "networking",
        "remoto",
        "reclutador",
        "reclutamiento",
    ]

    matching, others = [], []
    for a in anunciantes or []:
        combined = ' '.join(
            [str(a.get(k, '')) for k in ['nombre', 'descripcion', 'ubicacion', 'perfil']]
        )
        combined_norm = normalize(combined)

        found = any(kw in pregunta_norm or kw in combined_norm for kw in keywords)
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
