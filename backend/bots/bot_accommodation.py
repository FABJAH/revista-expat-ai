from .response_format import make_standard_response
import unicodedata


def _normalize(s):
    if not s:
        return ""
    s = str(s)
    s = s.strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def responder_consulta(pregunta, anunciantes):
    """Responde consultas de alojamiento con formato estándar.

    - Filtra por términos relevantes (hotel, apartamento, alquiler, piso...)
    - Añade FAQ por defecto si faltan
    - Devuelve estructura JSON y texto bilingüe
    """
    pregunta_norm = _normalize(pregunta or "")

    keywords = [
        "hotel",
        "apartamento",
        "alojamiento",
        "vivienda",
        "alquiler",
        "piso",
        "hostal",
        "room",
        "rent",
        "renta",
    ]

    matching = []
    others = []
    for a in anunciantes or []:
        combined = ' '.join(
            [str(a.get(k, '')) for k in ['nombre', 'descripcion', 'ubicacion', 'perfil']]
        )
        combined_norm = _normalize(combined)

        found = False
        for kw in keywords:
            if kw in pregunta_norm or kw in combined_norm:
                found = True
                break

        if found:
            matching.append(a)
        else:
            others.append(a)

    selected = matching if matching else others

    # Añadir FAQ genéricas si no vienen en los datos
    for a in selected:
        if not a.get('faq'):
            a['faq'] = [
                {
                    "q": "¿Cuál es el horario de check-in?",
                    "a": "El horario de entrada suele ser a partir de las 14:00, confirme con el anunciante."
                },
                {
                    "q": "¿Cuál es la política de cancelación?",
                    "a": "Depende del proveedor; consulte las condiciones al reservar."
                }
            ]

    return make_standard_response("Accommodation", selected, pregunta)
