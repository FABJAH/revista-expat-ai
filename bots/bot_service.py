from .response_format import make_standard_response


def responder_consulta(pregunta, anunciantes=None):
    """
    Responde a consultas sobre el servicio de creación de bots para anunciantes.
    """
    # Este bot no usa la lista de anunciantes, sino que tiene información fija.
    info_servicio = [
        {
            "nombre": "Bot de Agendamiento de Citas",
            "descripcion": "Un bot especializado para tu web que gestiona citas con tus clientes 24/7. Ideal para consultorios, abogados, y servicios profesionales.",
            "beneficios": ["Ahorro de tiempo administrativo", "Disponibilidad 24/7", "Reducción de no-shows con recordatorios automáticos"],
            "precio": "Desde 99€/mes (requiere ser anunciante)",
            "contacto": "bots@revistametropolitana.com",
            "faq": [
                {"q": "¿Se integra con mi calendario?", "a": "Sí, podemos integrarlo con Google Calendar y otros sistemas."},
                {"q": "¿Es personalizable?", "a": "Totalmente. Adaptamos el diálogo y la apariencia a tu marca."}
            ]
        },
        {
            "nombre": "Bot de Reservas para Restaurantes",
            "descripcion": "Un asistente virtual para tu restaurante que toma reservas, responde preguntas sobre el menú y gestiona cancelaciones.",
            "beneficios": ["Optimiza la ocupación de mesas", "Libera al personal del teléfono", "Mejora la experiencia del cliente"],
            "precio": "Desde 120€/mes (requiere ser anunciante)",
            "contacto": "bots@revistametropolitana.com"
        }
    ]

    return make_standard_response("BotService", info_servicio, pregunta)
