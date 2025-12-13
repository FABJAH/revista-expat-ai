# bots/bot_education.py
from .utils import filter_advertisers_by_keywords
from .maps_integration import search_healthcare_barcelona

def responder_consulta(pregunta, anunciantes, language="en"):
    """
    Responde a consultas sobre educación.
    PRIORIDAD 1: Anunciantes pagos (escuelas, academias)
    PRIORIDAD 2: Resultados de búsqueda complementaria
    """
    keywords = [
        "escuela", "colegio", "universidad", "curso", "idiomas", "academia",
        "formacion", "master", "postgrado", "clases", "taller", "school",
        "college", "university", "course", "languages", "academy", "training",
        "workshop", "preescolar", "infantil", "primaria", "secundaria"
    ]

    # 1. PRIMERO: Filtrar anunciantes pagos
    selected_advertisers = filter_advertisers_by_keywords(pregunta, anunciantes, keywords)

    # Marcar anunciantes como pagos
    for advertiser in selected_advertisers:
        advertiser["es_anunciante"] = True

    # 2. SEGUNDO: Si hay pocos anunciantes, complementar con info adicional
    if len(selected_advertisers) < 2:
        # Determinar qué tipo de educación buscan
        pregunta_lower = pregunta.lower()

        # Crear resultados informativos basados en la pregunta
        if any(word in pregunta_lower for word in ["idioma", "español", "ingles", "catalan", "language"]):
            selected_advertisers.append({
                "nombre": "📚 Escuelas de Idiomas en Barcelona",
                "descripcion": "Barcelona cuenta con numerosas academias de idiomas. Las más populares: International House, Speakeasy, Kingsbrook, Don Quijote.",
                "contacto": "Ver nuestros anunciantes para contacto directo",
                "beneficios": ["Cursos desde A1 hasta C2", "Clases presenciales y online", "Preparación exámenes oficiales"],
                "precio": "€120-400/mes según intensidad",
                "idiomas": "Español, Inglés, Catalán, Francés, Alemán",
                "ubicacion": "Varias ubicaciones en Barcelona",
                "es_anunciante": False
            })
        elif any(word in pregunta_lower for word in ["colegio", "escuela", "school", "niños", "kids"]):
            selected_advertisers.append({
                "nombre": "🏫 Colegios en Barcelona",
                "descripcion": "Barcelona ofrece colegios públicos (gratuitos), concertados (subvencionados) e internacionales privados (IB, británicos, americanos).",
                "contacto": "Ver guía completa en nuestra revista",
                "beneficios": ["Opciones públicas gratuitas", "Colegios internacionales desde €6k/año", "Sistema educativo de calidad"],
                "precio": "Desde gratuito hasta €20,000/año",
                "idiomas": "Según el colegio: Catalán, Español, Inglés",
                "ubicacion": "Toda Barcelona",
                "es_anunciante": False
            })
        elif any(word in pregunta_lower for word in ["universidad", "university", "master", "grado"]):
            selected_advertisers.append({
                "nombre": "🎓 Universidades en Barcelona",
                "descripcion": "Universidades públicas de prestigio: UB, UPF, UAB, UPC. Privadas: ESADE, IED, Ramon Llull.",
                "contacto": "Consulta admisiones en cada universidad",
                "beneficios": ["UPF en Top 10 universidades jóvenes del mundo", "Programas en inglés disponibles", "Matrícula pública €1,500-3,500/año"],
                "precio": "€1,500-4,000/año (públicas) | €8,000-20,000/año (privadas)",
                "idiomas": "Catalán, Español, Inglés",
                "ubicacion": "Barcelona y área metropolitana",
                "es_anunciante": False
            })

    # Extraer puntos clave de los 2 mejores resultados
    key_points = []
    for advertiser in selected_advertisers[:2]:
        point = {
            "nombre": advertiser.get("nombre"),
            "descripcion": advertiser.get("descripcion"),
            "beneficios": advertiser.get("beneficios", [])
        }
        key_points.append(point)

    return {"key_points": key_points, "json_data": selected_advertisers}
