from .response_format import make_standard_response
from .utils import normalize


def responder_consulta(pregunta, anunciantes):
    """Responde consultas de alojamiento con formato estándar.

    - Filtra por términos relevantes (hotel, apartamento, alquiler, piso...)
    - Añade FAQ por defecto si faltan
    - Devuelve estructura JSON y texto bilingüe
    """
    pregunta_norm = normalize(pregunta or "")

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

    matching, others = [], []
    for a in anunciantes or []:
        combined = ' '.join(
            [str(a.get(k, '')) for k in ['nombre', 'descripcion', 'ubicacion', 'perfil']]
        )
        combined_norm = normalize(combined)

        found = any(kw in pregunta_norm or kw in combined_norm for kw in keywords)
        (matching if found else others).append(a)

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
