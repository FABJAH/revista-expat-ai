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


def make_standard_response(categoria, anunciantes, pregunta=None, language="en"):
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

    # Generar el mensaje amigable en el idioma correcto
    friendly_text = ""
    if not opciones:
        if language == "es":
            friendly_text = "Lo siento, no se encontraron coincidencias para tu búsqueda en esta categoría."
        else: # Default a inglés
            friendly_text = "Sorry, no matches were found for your search in this category."
    else:
        if language == "es":
            friendly_text = f"Aquí tienes algunos anunciantes de {categoria} que podrían interesarte. Si necesitas más información de otros lugares, puedes utilizar Google u otra plataforma mientras actualizamos nuestra base de datos."
        else:
            friendly_text = f"Here are some {categoria} advertisers that might interest you. If you need more information about other places, you can use Google or another platform while we update our database."

    # Devolvemos el mensaje amigable y la lista de opciones directamente
    return {
        "friendly": friendly_text,
        "json": opciones # Aseguramos que sea la lista de anunciantes directamente
    }
