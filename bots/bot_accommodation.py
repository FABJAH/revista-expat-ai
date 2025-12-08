from .utils import filter_advertisers_by_keywords


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
