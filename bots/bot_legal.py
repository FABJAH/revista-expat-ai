from .utils import filter_advertisers_by_keywords, build_key_points


def responder_consulta(pregunta, anunciantes, language="en"):
    """
    Responde a consultas legales y financieras utilizando la función de filtrado central.
    """
    keywords = [
        "abogado", "legal", "financiero", "impuestos", "banco", "contrato",
        "visado", "nie", "residencia", "permiso", "nif", "gestoria", "gestor",
        "inmigracion", "extranjeria", "cuenta bancaria", "declaracion renta",
        "lawyer", "financial", "tax", "bank", "visa", "residency", "permit",
        "immigration", "consultant"
    ]

    selected_advertisers = filter_advertisers_by_keywords(pregunta, anunciantes, keywords)
    key_points = build_key_points(selected_advertisers)

    # Devolver lista completa; el orquestador aplicará limit/offset
    return {"key_points": key_points, "json_data": selected_advertisers}
