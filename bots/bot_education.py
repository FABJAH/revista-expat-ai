from .utils import normalize


def responder_consulta(pregunta, anunciantes, language="en"):
    """Responde consultas educativas con formato estándar.

    - Filtra por términos relevantes (escuela, curso, idiomas, universidad, academia).
    - Añade FAQs por defecto si faltan.
    - Devuelve JSON estandarizado y texto bilingüe.
    """
    pregunta_norm = normalize(pregunta or "")

    keywords = [
        "escuela",
        "colegio",
        "universidad",
        "curso",
        "idiomas",
        "academia",
        "language",
        "course",
        "training",
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
                {"q": "¿Hay certificación?", "a": "Consulta con el proveedor si emiten certificado al terminar."},
                {"q": "¿Hay clases online?", "a": "Muchos cursos ofrecen modalidad presencial y online; pregunta al anunciante."}
            ]

    return make_standard_response("Education", selected, pregunta, language)
