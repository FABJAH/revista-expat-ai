from .utils import filter_advertisers_by_keywords, build_key_points


def responder_consulta(pregunta, anunciantes, language="en"):
    """
    Responde a consultas sobre alojamiento utilizando la función de filtrado central.
    """
    # Keywords from orchestrator.py for consistency
    keywords = [
        "hotel", "apartamento", "alojamiento", "vivienda", "alquiler", "piso",
        "hostal", "renta", "habitacion", "hospedaje", "estancia", "apartment",
        "housing", "flat", "hostel", "room", "rent", "accommodation"
    ]

    # Usamos la nueva función centralizada para encontrar los anunciantes relevantes
    selected_advertisers = filter_advertisers_by_keywords(pregunta, anunciantes, keywords)
    key_points = build_key_points(selected_advertisers)

    # Devolver lista completa; el orquestador aplicará limit/offset
    return {"key_points": key_points, "json_data": selected_advertisers}
