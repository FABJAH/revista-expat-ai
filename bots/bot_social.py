from .utils import filter_advertisers_by_keywords, build_key_points


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

    key_points = build_key_points(selected_advertisers)

    return {"key_points": key_points, "json_data": selected_advertisers}
