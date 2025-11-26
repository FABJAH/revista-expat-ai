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
    """Responde consultas legales/financieras con formato estándar.

    - Filtra anunciantes por coincidencia de términos (NIE, residencia, impuestos, banco, abogado).
    - Si hay coincidencias, devuelve JSON estandarizado y texto bilingüe.
    - Si no, indica claramente en ambos idiomas.
    """
    pregunta_norm = _normalize(pregunta or "")

    keywords = ["nie", "residencia", "residencial", "impuesto", "impuestos",
                "banco", "abogado", "lawyer", "tax", "permiso", "documento", "nif"]

    # Priorizar anunciantes cuyos campos contengan alguna keyword
    matching = []
    others = []
    for a in anunciantes or []:
        hay = False
        combined = ' '.join([str(a.get(k, '')) for k in ['nombre', 'descripcion', 'perfil', 'contacto']])
        combined_norm = _normalize(combined)
        for kw in keywords:
            if kw in pregunta_norm or kw in combined_norm:
                hay = True
                break
        if hay:
            matching.append(a)
        else:
            others.append(a)

    selected = matching if matching else others

    # Añadir FAQ genéricas si no vienen en los datos
    for a in selected:
        if not a.get('faq'):
            a['faq'] = [
                {"q": "¿Cómo solicito un NIE?", "a": "Solicita cita en la oficina de extranjería o tramite online."},
                {"q": "¿Necesito un abogado para residencia?", "a": "Depende de la complejidad; un profesional puede ayudar con documentación."}
            ]

    return make_standard_response("Legal and Financial", selected, pregunta)
