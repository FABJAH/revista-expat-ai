# bots/bot_healthcare.py
from .response_format import make_standard_response
from .utils import normalize

def responder_consulta(pregunta, anunciantes):
    """Responde consultas de salud con formato estándar."""
    pregunta_norm = normalize(pregunta or "")
    keywords = [
        "medico","médico","doctor","hospital","clinica","clínica","dentista",
        "odontologia","pediatra","ginecologo","seguro","salud","insurance","clinic","health"
    ]

    matching, others = [], []
    for a in anunciantes or []:
        combined = ' '.join([str(a.get(k, '')) for k in ['nombre','descripcion','perfil','contacto','ubicacion']])
        cn = normalize(combined)
        found = any(kw in pregunta_norm or kw in cn for kw in keywords)
        (matching if found else others).append(a)

    selected = matching if matching else others

    for a in selected:
        if not a.get('faq'):
            a['faq'] = [
                {"q":"¿Aceptan seguro médico?","a":"Consulta directamente qué aseguradoras aceptan."},
                {"q":"¿Atención en inglés?","a":"Muchos centros atienden en inglés; confirma al reservar."}
            ]

    return make_standard_response("Healthcare", selected, pregunta)
