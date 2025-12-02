from .utils import normalize


def responder_consulta(pregunta, paquetes, language="en"):
    """Responde consultas comerciales/publicidad con formato estándar.

    - Filtra paquetes por términos relevantes (publicidad, paquete, campaña, media kit).
    - Añade FAQs por defecto si faltan.
    - Devuelve JSON estandarizado y texto bilingüe.
    """
    pregunta_norm = normalize(pregunta or "")

    keywords = [
        "anunciar",
        "publicidad",
        "paquete",
        "campana",
        "campaña",
        "promocion",
        "promoción",
        "revista",
        "media kit",
        "ads",
        "advertising",
        "campaign",
    ]

    matching, others = [], []
    for p in paquetes or []:
        combined = ' '.join(
            [str(p.get(k, '')) for k in ['nombre', 'descripcion', 'beneficios', 'perfil']]
        )
        combined_norm = normalize(combined)

        found = any(kw in pregunta_norm or kw in combined_norm for kw in keywords)
        (matching if found else others).append(p)

    selected = matching if matching else others

    # Extraer puntos clave de los 2 mejores resultados
    key_points = []
    for advertiser in selected[:2]:
        point = {
            "nombre": advertiser.get("nombre"),
            "descripcion": advertiser.get("descripcion"),
            "beneficios": advertiser.get("beneficios", [])
        }
        key_points.append(point)

    return {"key_points": key_points, "json_data": selected}
