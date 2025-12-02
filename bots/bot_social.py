from .response_format import make_standard_response
from .utils import normalize


def responder_consulta(pregunta, anunciantes):
    """Responde consultas sociales/culturales con formato estándar.

    - Filtra por términos relevantes (evento, asociación, restaurante, actividad).
    - Añade FAQs por defecto si faltan.
    - Devuelve JSON estandarizado y texto bilingüe.
    """
    pregunta_norm = normalize(pregunta or "")

    keywords = [
        "expat",
        "expats",
        "asociacion",
        "asociación",
        "evento",
        "restaurante",
        "actividad",
        "ocio",
        "meetup",
        "cultural",
        "festival",
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
                    "q": "¿Cómo me apunto al evento?",
                    "a": "Consulta el contacto del organizador para inscribirte o reserva mediante su web."
                },
                {
                    "q": "¿Hay actividades para familias?",
                    "a": "Depende del evento; revisa la descripción o pregunta al organizador."
                }
            ]

    return make_standard_response("Social and Cultural", selected, pregunta)
