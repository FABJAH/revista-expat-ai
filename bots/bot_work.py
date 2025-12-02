from .response_format import make_standard_response
from .utils import normalize


def responder_consulta(pregunta, anunciantes):
    """Responde consultas sobre empleo y networking con formato estándar.

    - Filtra por términos relevantes (trabajo, empleo, oferta, coworking, networking).
    - Añade FAQs por defecto si faltan.
    - Devuelve JSON estandarizado y texto bilingüe.
    """
    pregunta_norm = normalize(pregunta or "")

    keywords = [
        "trabajo",
        "empleo",
        "oferta",
        "job",
        "vacante",
        "coworking",
        "networking",
        "remoto",
        "reclutador",
        "reclutamiento",
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
                {"q": "¿Cómo aplico a una oferta?", "a": "Envia tu CV al contacto indicado o sigue las instrucciones en la oferta."},
                {"q": "¿Hay posibilidad de trabajo remoto?", "a": "Depende del puesto; consulta con el anunciante."}
            ]

    return make_standard_response("Work and Networking", selected, pregunta)
