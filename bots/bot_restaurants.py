from .utils import filter_advertisers_by_keywords, build_key_points


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

    key_points = build_key_points(selected_advertisers)

    # Devolver lista completa; el orquestador aplicará limit/offset
    return {"key_points": key_points, "json_data": selected_advertisers}
