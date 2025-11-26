from .response_format import make_standard_response
import unicodedata


def _normalize(s):
    if not s:
        return ""
    s = str(s).strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def responder_consulta(pregunta, anunciantes):
    """Responde consultas de salud con formato estándar.

    - Filtra por términos relevantes (médico, clínica, dentista, seguro).
    - Añade FAQs por defecto si faltan.
    - Devuelve JSON estandarizado y texto bilingüe.
    """
    pregunta_norm = _normalize(pregunta or "")

    keywords = [
        "medico",
        "médico",
        "doctor",
        "clinica",
        "clínica",
        "dentista",
        "seguro",
        "salud",
        "hospital",
        "clinic",
        "health",
        "insurance",
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
                    "q": "¿Cómo pido una cita?",
                    "a": "Contacta al número o correo del proveedor; muchos aceptan cita online."
                },
                {
                    "q": "¿Cubre mi seguro la consulta?",
                    "a": "Depende de tu póliza; consulta con tu aseguradora o con el centro médico."
                }
            ]

    return make_standard_response("Healthcare", selected, pregunta)
