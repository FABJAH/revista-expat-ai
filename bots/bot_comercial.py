from .utils import filter_advertisers_by_keywords


def responder_consulta(pregunta, paquetes, language="en"):
    """
    Responde a consultas comerciales/publicidad utilizando la función de filtrado central.
    """
    keywords = [
        "anunciar", "publicidad", "paquete", "campaña", "promocion", "revista",
        "media kit", "marketing", "anunciate", "colaborar", "patrocinar",
        "advertise", "advertising", "package", "campaign", "promotion", "magazine",
        "ads", "collaborate", "sponsorship", "partner"
    ]

    # El argumento 'anunciantes' aquí contiene los 'paquetes'
    selected_advertisers = filter_advertisers_by_keywords(pregunta, paquetes, keywords)

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
