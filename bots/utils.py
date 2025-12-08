import unicodedata


def normalize(s):
    if not s:
        return ""
    s = str(s).strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()

def filter_advertisers_by_keywords(pregunta, anunciantes, keywords, search_fields=['nombre', 'descripcion', 'perfil', 'ubicacion']):
    """
    Función reutilizable para filtrar una lista de anunciantes.

    - Prioriza los anunciantes que coinciden con las palabras clave.
    - Si no hay coincidencias, devuelve el resto.
    """
    if not anunciantes:
        return []

    pregunta_norm = normalize(pregunta or "")

    matching, others = [], []
    for a in anunciantes:
        # Combina el contenido de los campos relevantes del anunciante en un solo texto
        combined_text = ' '.join([str(a.get(k, '')) for k in search_fields])
        combined_norm = normalize(combined_text)

        # Comprueba si alguna palabra clave está en la pregunta del usuario o en el texto del anunciante
        found = any(kw in pregunta_norm or kw in combined_norm for kw in keywords)
        (matching if found else others).append(a)

    return matching if matching else others
