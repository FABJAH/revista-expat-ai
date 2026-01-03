from .utils import filter_advertisers_by_keywords


def responder_consulta(pregunta, anunciantes, language="en"):
    """
    Responde a consultas sobre restaurantes utilizando la función de filtrado central.
    """
    keywords = [
        "restaurante", "comida", "cenar", "menu", "reserva", "terraza",
        "cocina", "tapas", "brunch", "desayuno", "almuerzo", "pizzeria",
        "restaurant", "food", "dinner", "reservation", "lunch", "cuisine",
        "breakfast"
    ]

    selected_advertisers = filter_advertisers_by_keywords(pregunta, anunciantes, keywords)

    key_points = []
    for advertiser in selected_advertisers[:2]:
        point = {
            "nombre": advertiser.get("nombre"),
            "descripcion": advertiser.get("descripcion"),
            "beneficios": advertiser.get("beneficios", [])
        }
        key_points.append(point)

    # Devolver lista completa; el orquestador aplicará limit/offset
    return {"key_points": key_points, "json_data": selected_advertisers}
