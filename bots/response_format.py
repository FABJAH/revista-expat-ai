import unicodedata
import json


def _normalize_text(s):
    if not s:
        return ""
    s = str(s)
    s = s.strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s


def make_standard_response(categoria, anunciantes, pregunta=None):
    """
    Devuelve un dict con la estructura solicitada y un texto amigable bilingüe.

    JSON fields: categoria, opciones (cada una con nombre, descripcion,
    beneficios, precio, contacto, idiomas, ubicacion, faq)
    """
    categoria = categoria or "Desconocida"
    opciones = []
    for a in anunciantes or []:
        opcion = {
            "nombre": a.get("nombre") or a.get("title") or None,
            "descripcion": a.get("descripcion") or a.get("descripcion_corta") or a.get("description") or None,
            "beneficios": a.get("beneficios") if isinstance(a.get("beneficios"), list) else ([a.get("beneficios")] if a.get("beneficios") else []),
            "precio": a.get("precio") or a.get("price") or None,
            "contacto": a.get("contacto") or a.get("contact") or None,
            "idiomas": a.get("idiomas") or a.get("languages") or None,
            "ubicacion": a.get("ubicacion") or a.get("location") or None,
            "faq": a.get("faq") or a.get("faqs") or []
        }
        opciones.append(opcion)

    json_resp = {
        "categoria": categoria,
        "opciones": opciones
    }

    # Texto amigable bilingüe
    if not opciones:
        text_es = "No se encontraron coincidencias para tu búsqueda."
        text_en = "No matches were found for your search."
        text = f"ES: {text_es}\nEN: {text_en}"
        return {"json": json_resp, "text": text}

    # Construir resumen en español
    lines_es = [f"Categoría detectada: {categoria}"]
    if pregunta:
        lines_es.append(f"Consulta: {pregunta}")
    lines_es.append("Resultados:")
    for opt in opciones:
        lines_es.append(f"- {opt['nombre']}: {opt['descripcion']}")
        if opt['beneficios']:
            lines_es.append(f"  Beneficios: {', '.join([str(b) for b in opt['beneficios']])}")
        if opt['precio']:
            lines_es.append(f"  Precio: {opt['precio']}")
        if opt['contacto']:
            lines_es.append(f"  Contacto: {opt['contacto']}")
        if opt['idiomas']:
            lines_es.append(f"  Idiomas: {opt['idiomas']}")
        if opt['ubicacion']:
            lines_es.append(f"  Ubicación: {opt['ubicacion']}")

    # Construir resumen en inglés (simple, literal)
    lines_en = [f"Category detected: {categoria}"]
    if pregunta:
        lines_en.append(f"Query: {pregunta}")
    lines_en.append("Results:")
    for opt in opciones:
        lines_en.append(f"- {opt['nombre']}: {opt['descripcion']}")
        if opt['beneficios']:
            lines_en.append(f"  Benefits: {', '.join([str(b) for b in opt['beneficios']])}")
        if opt['precio']:
            lines_en.append(f"  Price: {opt['precio']}")
        if opt['contacto']:
            lines_en.append(f"  Contact: {opt['contacto']}")
        if opt['idiomas']:
            lines_en.append(f"  Languages: {opt['idiomas']}")
        if opt['ubicacion']:
            lines_en.append(f"  Location: {opt['ubicacion']}")

    text = "ES:\n" + "\n".join(lines_es) + "\n\nEN:\n" + "\n".join(lines_en)

    return {"json": json_resp, "text": text}
