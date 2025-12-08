from .utils import filter_advertisers_by_keywords


def responder_consulta(pregunta, anunciantes, language="en"):
    """
    Responde a consultas sociales/culturales utilizando la función de filtrado central.
    """
    keywords = [
        "museo", "galeria", "exposicion", "arte", "cultural", "teatro", "concierto",
        "bar", "discoteca", "pub", "copas", "noche", "fiesta", "club", "karaoke",
        "ocio", "recreacion", "deporte", "gimnasio", "parque", "entretenimiento",
        "museum", "gallery", "exhibition", "art", "theater", "concert", "nightlife",
        "leisure", "sports", "gym", "park", "entertainment", "fun", "social"
    ]

    selected_advertisers = filter_advertisers_by_keywords(pregunta, anunciantes, keywords)

    # Extraer puntos clave de los 2 mejores resultados
    key_points = []
    for advertiser in selected_advertisers[:2]:
        point = {
            "nombre": advertiser.get("nombre"),
            "descripcion": advertiser.get("descripcion"),
            "beneficios": advertiser.get("beneficios", [])
        }
        key_points.append(point)

    return {"key_points": key_points, "json_data": selected_advertisers}
