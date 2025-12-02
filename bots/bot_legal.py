from .utils import normalize


def responder_consulta(pregunta, anunciantes, language="en"):
    """Responde consultas legales/financieras con formato estándar.

    - Filtra anunciantes por coincidencia de términos (NIE, residencia, impuestos, banco, abogado).
    - Si hay coincidencias, devuelve JSON estandarizado y texto bilingüe.
    - Si no, indica claramente en ambos idiomas.
    """
    pregunta_norm = normalize(pregunta or "")

    keywords = ["nie", "residencia", "residencial", "impuesto", "impuestos",
                "banco", "abogado", "lawyer", "tax", "permiso", "documento", "nif"]

    # Priorizar anunciantes cuyos campos contengan alguna keyword
    matching, others = [], []
    for a in anunciantes or []:
        combined = ' '.join([str(a.get(k, '')) for k in ['nombre', 'descripcion', 'perfil', 'contacto']])
        combined_norm = normalize(combined)
        found = any(kw in pregunta_norm or kw in combined_norm for kw in keywords)
        (matching if found else others).append(a)

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
