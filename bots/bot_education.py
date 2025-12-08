from .utils import filter_advertisers_by_keywords


def responder_consulta(pregunta, anunciantes, language="en"):
    """
    Responde a consultas sobre educación utilizando la función de filtrado central.
    """
    keywords = [
        "escuela", "colegio", "universidad", "curso", "idiomas", "academia",
        "formacion", "master", "postgrado", "clases", "taller", "school",
        "college", "university", "course", "languages", "academy", "training",
        "workshop"
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
