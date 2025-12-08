from .utils import filter_advertisers_by_keywords


def responder_consulta(pregunta, anunciantes, language="en"):
    """
    Responde a consultas sobre empleo y networking utilizando la función de filtrado central.
    """
    keywords = [
        "trabajo", "empleo", "oferta", "job", "vacante", "coworking", "networking",
        "remoto", "reclutador", "reclutamiento", "negocio", "empresa", "corporativo",
        "consultoria", "asesoria", "oficina", "business", "company", "corporate",
        "consulting", "services"
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
