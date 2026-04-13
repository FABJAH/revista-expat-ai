from .utils import filter_advertisers_by_keywords, build_key_points


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

    key_points = build_key_points(selected_advertisers)

    # Devolver lista completa; el orquestador aplicará limit/offset
    return {"key_points": key_points, "json_data": selected_advertisers}
