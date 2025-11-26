from .response_format import make_standard_response
import unicodedata


def _normalize(s):
    if not s:
        return ""
    s = str(s).strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def responder_consulta(pregunta, paquetes):
    """Responde consultas comerciales/publicidad con formato estándar.

    - Filtra paquetes por términos relevantes (publicidad, paquete, campaña, media kit).
    - Añade FAQs por defecto si faltan.
    - Devuelve JSON estandarizado y texto bilingüe.
    """
    pregunta_norm = _normalize(pregunta or "")

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

    matching = []
    others = []
    for p in paquetes or []:
        combined = ' '.join(
            [str(p.get(k, '')) for k in ['nombre', 'descripcion', 'beneficios', 'perfil']]
        )
        combined_norm = _normalize(combined)

        found = False
        for kw in keywords:
            if kw in pregunta_norm or kw in combined_norm:
                found = True
                break

        if found:
            matching.append(p)
        else:
            others.append(p)

    selected = matching if matching else others

    # Añadir FAQ genéricas si no vienen en los datos
    for p in selected:
        if not p.get('faq'):
            p['faq'] = [
                {
                    "q": "¿Qué incluye el paquete?",
                    "a": "Descripción de espacios, duración y formatos incluidos; consultar detalles con el equipo comercial."
                },
                {
                    "q": "¿Cuál es el plazo de contratación?",
                    "a": "Depende del paquete; normalmente se requieren 7-14 días hábiles para preparar la campaña."
                },
                {
                    "q": "¿Podéis personalizar una propuesta?",
                    "a": "Sí, ofrecemos propuestas personalizadas según objetivos y presupuesto."
                }
            ]

    return make_standard_response("Comercial", selected, pregunta)
