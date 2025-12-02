# bots/orchestrator.py
import json
import re
import random
from pathlib import Path
from .response_format import make_standard_response
from .utils import normalize

# Importa bots disponibles
from .bot_accommodation import responder_consulta as acc_responder
from .bot_legal import responder_consulta as leg_responder
from .bot_comercial import responder_consulta as com_responder
from .bot_education import responder_consulta as edu_responder
from .bot_healthcare import responder_consulta as hea_responder
from .bot_social import responder_consulta as soc_responder
from .bot_work import responder_consulta as work_responder
from .bot_service import responder_consulta as srv_responder

class Orchestrator:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent
        data_path = base_dir / "data" / "anunciantes.json"
        try:
            with open(str(data_path), 'r', encoding='utf-8') as f:
                self.advertisers = json.load(f)
            print("✅ Base de datos cargada.")
        except Exception as e:
            print(f"❌ ERROR cargando base de datos: {e}")
            self.advertisers = {}

        # Mapa de bots
        self.bots_map = {
            "Accommodation": acc_responder,
            "Legal and Financial": leg_responder,
            "Comercial": com_responder,
            "Education": edu_responder,
            "Healthcare": hea_responder,
            "Social and Cultural": soc_responder,
            "Work and Networking": work_responder,
            "BotService": srv_responder,
        }

        # Patrones de intención (depurados)
        self.category_patterns = { # Separado por idioma
            "es": {
                "Accommodation": ["hotel", "apartamento", "alojamiento", "vivienda", "alquiler", "piso", "hostal", "renta", "habitacion", "hospedaje", "estancia"],
                "Arts and Culture": ["museo", "galeria", "exposicion", "arte", "cultural", "teatro", "concierto"],
                "Bars and Clubs": ["bar", "discoteca", "pub", "copas", "noche", "fiesta", "club", "karaoke", "terraza", "coctel"],
                "Beauty and Well-Being": ["spa", "masaje", "estetica", "belleza", "bienestar", "peluqueria", "manicura", "facial"],
                "Business Services": ["negocio", "empresa", "corporativo", "consultoria", "asesoria", "oficina", "coworking"],
                "Education": ["escuela", "colegio", "universidad", "curso", "idiomas", "academia", "formacion", "master", "postgrado", "clases", "taller"],
                "Healthcare": ["medico", "hospital", "clinica", "dentista", "seguro", "salud", "doctor", "pediatra", "ginecologo", "farmacia", "urgencias", "especialista", "psicologo", "terapia"],
                "Home Services": ["reparacion", "limpieza", "fontanero", "electricista", "carpintero", "mudanza", "pintor", "jardineria"],
                "Legal and Financial": ["abogado", "legal", "financiero", "impuestos", "banco", "contrato", "visado", "nie", "residencia", "permiso", "nif", "gestoria", "gestor", "inmigracion", "extranjeria", "cuenta bancaria", "declaracion renta"],
                "Recreation and Leisure": ["ocio", "recreacion", "deporte", "gimnasio", "parque", "entretenimiento"],
                "Restaurants": ["restaurante", "comida", "cenar", "menu", "reserva", "terraza", "cocina", "tapas", "brunch", "desayuno", "almuerzo", "pizzeria"],
                "Retail": ["tienda", "compras", "producto", "ropa", "moda", "centro comercial"],
                "Comercial": ["anunciar", "publicidad", "paquete", "campaña", "promocion", "revista", "media kit", "marketing", "anunciate", "colaborar", "patrocinar"],
                "BotService": ["bot", "agendamiento", "citas", "reservas", "asistente virtual", "chatbot"]
            },
            "en": {
                "Accommodation": ["hotel", "apartment", "housing", "flat", "hostel", "room", "rent", "accommodation"],
                "Arts and Culture": ["museum", "gallery", "exhibition", "art", "cultural", "theater", "concert"],
                "Bars and Clubs": ["bar", "club", "pub", "drinks", "night", "party", "karaoke", "terrace", "cocktail", "nightlife"],
                "Beauty and Well-Being": ["spa", "massage", "beauty", "wellness", "hairdresser", "manicure", "facial", "salon"],
                "Business Services": ["business", "company", "corporate", "consulting", "office", "services", "coworking"],
                "Education": ["school", "college", "university", "course", "languages", "academy", "training", "master", "postgraduate", "classes", "workshop"],
                "Healthcare": ["doctor", "hospital", "clinic", "dentist", "insurance", "health", "pediatrician", "gynecologist", "pharmacy", "emergency", "specialist", "psychologist", "therapy"],
                "Home Services": ["repair", "cleaning", "plumber", "electrician", "carpenter", "moving", "painter", "gardening"],
                "Legal and Financial": ["lawyer", "legal", "financial", "tax", "bank", "contract", "visa", "nie", "residency", "permit", "immigration", "residency permit", "bank account", "tax return", "consultant"],
                "Recreation and Leisure": ["leisure", "recreation", "sports", "gym", "park", "entertainment", "fun"],
                "Restaurants": ["restaurant", "food", "dinner", "menu", "reservation", "terrace", "lunch", "cuisine", "tapas", "brunch", "breakfast", "pizzeria"],
                "Retail": ["store", "shopping", "retail", "product", "clothes", "fashion", "shop", "mall", "clothing"],
                "Comercial": ["advertise", "advertising", "package", "campaign", "promotion", "magazine", "media kit", "ads", "marketing", "collaborate", "sponsorship", "partner"],
                "BotService": ["bot", "scheduling", "appointments", "booking", "virtual assistant", "chatbot"]
            }
        }

        # Respuestas amigables por categoría
        self.responses_map = {
            "es": {
                "Healthcare": [
                    "Veo que preguntas sobre salud. Te conecto con nuestro bot de Salud.",
                    "Parece que necesitas información médica. Nuestro bot de Salud puede guiarte.",
                    "Los temas de salud son importantes. Dejaré que nuestro bot de Salud te ayude.",
                    "Claro, aquí tienes información sobre servicios de salud en Barcelona.",
                    "Entendido, buscando opciones de salud para ti."
                ],
                "Legal and Financial": [
                    "Parece que necesitas ayuda legal o financiera. Nuestro bot Legal te ayudará.",
                    "Esto parece una pregunta sobre visados o contratos. Te conecto con el bot Legal.",
                    "Los asuntos legales y financieros pueden ser complicados. Nuestro bot Legal está aquí para ayudar.",
                    "¡Por supuesto! Navegar la burocracia puede ser difícil. Aquí tienes algunos expertos.",
                    "Entendido. Te muestro especialistas en temas legales y financieros."
                ],
                "Accommodation": [
                    "¿Buscando alojamiento? El bot de Alojamiento te mostrará opciones.",
                    "Estás buscando un lugar donde quedarte. Te conecto con nuestro bot de Alojamiento.",
                    "Las preguntas sobre alojamiento son comunes. Nuestro bot puede guiarte.",
                    "¡Claro! Te ayudo a encontrar tu próximo hogar en Barcelona. Aquí tienes algunas opciones:",
                    "Entendido, buscando el lugar perfecto para ti. Te paso con nuestro especialista en alojamiento."
                ],
                "Education": [
                    "¿Interesado en escuelas o cursos? Nuestro bot de Educación puede guiarte.",
                    "¿Buscas clases de idiomas o universidades? El bot de Educación tiene los detalles.",
                    "La educación es clave. Te conecto con nuestro bot de Educación.",
                    "Perfecto, aquí tienes información sobre centros educativos en la ciudad.",
                    "¡Genial! Invertir en formación siempre es una buena idea. Mira estas opciones:"
                ],
                "Work and Networking": [
                    "¿Buscando trabajo u oportunidades de networking? El bot de Empleo puede ayudarte.",
                    "Las preguntas sobre carrera son importantes. Nuestro bot de Empleo te guiará.",
                    "Te conectamos con el bot de Empleo para oportunidades profesionales.",
                    "Claro, te muestro información sobre el mercado laboral y eventos de networking.",
                    "¡A por ello! Aquí tienes recursos para tu carrera profesional en Barcelona."
                ],
                "Social and Cultural": [
                    "¿Quieres explorar la vida social y cultural? El bot Social puede guiarte.",
                    "¿Buscas eventos o actividades culturales? El bot Social tiene sugerencias.",
                    "Las experiencias sociales y culturales importan. Te conecto con nuestro bot Social.",
                    "¡Fantástico! Barcelona tiene una vida cultural increíble. Aquí tienes algunas ideas:",
                    "Perfecto, te ayudo a descubrir los mejores planes sociales y culturales."
                ],
                "Comercial": [
                    "¿Interesado en anunciarte con nosotros? El bot Comercial puede explicarte los paquetes.",
                    "¿Buscas oportunidades de promoción? El bot Comercial te guiará.",
                    "El marketing y la publicidad son importantes. Te conectamos con nuestro bot Comercial.",
                    "¡Genial que quieras colaborar! Aquí tienes la información sobre nuestros paquetes de publicidad.",
                    "Claro, te muestro cómo tu negocio puede llegar a miles de expatriados en Barcelona."
                ],
                "BotService": [
                    "Parece que preguntas sobre nuestros servicios de bots personalizados. Te doy los detalles.",
                    "¿Interesado en un chatbot para tu negocio? Puedo darte más información.",
                    "Puedo ayudarte con eso. Aquí tienes información sobre los servicios de bot que ofrecemos.",
                    "¡Claro! Un asistente virtual puede transformar tu negocio. Esto es lo que ofrecemos:",
                    "Detecto que preguntas por mis 'poderes'. ¡Te cuento cómo puedes tener un asistente como yo!"
                ]
            },
            "en": {
                "Healthcare": [
                    "I see you’re asking about health. Let me connect you with our Healthcare bot.",
                    "Looks like you need medical information. Our Healthcare bot can guide you to clinics and doctors.",
                    "Health matters are important. I’ll bring in our Healthcare bot to assist you.",
                    "Of course, here is some information about healthcare services in Barcelona.",
                    "Understood, looking for health options for you."
                ],
                "Legal and Financial": [
                    "You seem to need legal or financial help. Our Legal bot will assist you.",
                    "This looks like a question about visas or contracts. Let’s connect you with the Legal bot.",
                    "Legal and financial issues can be tricky. Our Legal bot is here to help.",
                    "Of course! Navigating bureaucracy can be tough. Here are some experts.",
                    "Understood. I'll show you specialists in legal and financial matters."
                ],
                "Accommodation": [
                    "Searching for housing? The Accommodation bot will show you options.",
                    "You’re looking for a place to stay. Let me connect you with our Accommodation bot.",
                    "Accommodation questions are common. Our bot can guide you to rentals and housing.",
                    "Sure! Let me help you find your next home in Barcelona. Here are some options:",
                    "Got it, looking for the perfect place for you. I'll connect you with our accommodation specialist."
                ],
                "Education": [
                    "Interested in schools or courses? Our Education bot can guide you.",
                    "Looking for language classes or universities? The Education bot has the details.",
                    "Education is key. Let me connect you with our Education bot.",
                    "Perfect, here is some information about educational centers in the city.",
                    "Great! Investing in training is always a good idea. Check out these options:"
                ],
                "Work and Networking": [
                    "Searching for jobs or networking opportunities? The Work bot can help.",
                    "Career questions are important. Our Work bot will guide you.",
                    "Let’s connect you with the Work bot for professional opportunities.",
                    "Sure, I'll show you information about the job market and networking events.",
                    "Let's do it! Here are resources for your professional career in Barcelona."
                ],
                "Social and Cultural": [
                    "Want to explore culture and social life? The Social bot can guide you.",
                    "Looking for events or cultural activities? The Social bot has suggestions.",
                    "Social and cultural experiences matter. Let me connect you with our Social bot.",
                    "Fantastic! Barcelona has an incredible cultural life. Here are some ideas:",
                    "Perfect, I'll help you discover the best social and cultural plans."
                ],
                "Comercial": [
                    "Interested in advertising with us? The Comercial bot can explain packages.",
                    "Looking for promotion opportunities? The Comercial bot will guide you.",
                    "Marketing and ads are important. Let’s connect you with our Comercial bot.",
                    "Great that you want to collaborate! Here is the information about our advertising packages.",
                    "Sure, I'll show you how your business can reach thousands of expats in Barcelona."
                ],
                "BotService": [
                    "It looks like you're asking about our custom bot services. Let me get you the details.",
                    "Interested in a chatbot for your business? I can provide more information on that.",
                    "I can help with that. Here is some information about the bot services we offer to advertisers.",
                    "Of course! A virtual assistant can transform your business. Here's what we offer:",
                    "I detect you're asking about my 'powers'. I'll tell you how you can have an assistant like me!"
                ]
            }
        }

    def classify_intent(self, question, language="en"):
        qn = normalize(question)

        # --- MEJORA: Usar patrones de ambos idiomas para una detección más robusta ---
        patterns_es = self.category_patterns.get("es", {})
        patterns_en = self.category_patterns.get("en", {})

        best_match, best_score = None, 0

        # Unimos todas las categorías de ambos idiomas para no perder ninguna
        all_categories = set(patterns_es.keys()) | set(patterns_en.keys())

        for category in all_categories:
            # Sumar puntos por coincidencias en español e inglés
            score = sum(1 for p in patterns_es.get(category, []) if p in qn)
            score += sum(1 for p in patterns_en.get(category, []) if p in qn)
            if score > best_score:
                best_score, best_match = score, category
        if best_match:
            # DEBUG: Imprime la categoría detectada
            print(f"DEBUG: Pregunta '{question}' (normalizada: '{qn}') clasificada como '{best_match}' con puntuación {best_score}")

            confidence = min(0.1 * best_score + 0.5, 0.95)
            return best_match, confidence, None

        # Coincidencias con negocios
        for category, businesses in self.advertisers.items():
            for business in businesses:
                name = normalize(business.get('nombre', ''))
                desc = normalize(business.get('descripcion', ''))
                if name and name in qn:
                    return category, 0.9, business
                common = set(re.findall(r"\w+", desc)) & set(re.findall(r"\w+", qn))
                if len(common) >= 2:
                    return category, 0.8, business

        return "Desconocida", 0.3, None

    def process_query(self, question, language="en"):
        categoria, confidence, advertiser = self.classify_intent(question, language)
        lang = language if language in self.responses_map else "en"
        resultados = self.advertisers.get(categoria, [])
        if advertiser and advertiser not in resultados:
            resultados.insert(0, advertiser)

        # Mensaje amigable del orquestador
        friendly_msg = ""
        if categoria in self.responses_map[lang]:
            friendly_msg = random.choice(self.responses_map[lang][categoria])

        # Si hay bot específico para la categoría, usarlo
        if categoria in self.bots_map:
            try:
                bot_response = self.bots_map[categoria](question, resultados, lang)
                key_points = bot_response.get("key_points", [])

                # --- NUEVA LÓGICA DE GENERACIÓN DE RESPUESTA ---
                final_response_text = friendly_msg

                if key_points:
                    summary_parts = []
                    for point in key_points:
                        beneficios_str = ""
                        if point.get('beneficios'):
                            beneficios_str = " Sus puntos fuertes son: " + ", ".join(point['beneficios'][:2]) + "."

                        summary_parts.append(
                            f"{point.get('nombre')}, que es {point.get('descripcion', '').lower()}{beneficios_str}"
                        )

                    final_response_text += " He encontrado un par de opciones que podrían interesarte: " + " También está ".join(summary_parts) + "."
                    final_response_text += " Te muestro la lista completa para que la explores."
                else:
                    # Si el bot no devuelve puntos clave, usamos una respuesta más genérica.
                    final_response_text += " Aquí tienes una lista de contactos que podrían ayudarte."

                return {
                    "respuesta": final_response_text,
                    "agente": categoria,
                    "confidence": confidence,
                    "json": bot_response.get("json_data", resultados),
                    "friendly": friendly_msg
                }
            except Exception as e:
                print("Error en bot:", categoria, e)

        # Fallback: respuesta básica estandarizada
        fallback_text = friendly_msg or "No he podido clasificar tu pregunta con claridad. Intenta reformularla o usa la barra de búsqueda."
        if resultados:
            fallback_text += " De todos modos, aquí tienes algunos contactos que podrían ser de utilidad."

        resp = make_standard_response(categoria, resultados, question, lang)
        return { "respuesta": fallback_text, "agente": categoria, "confidence": confidence, "json": resp.get("json", {}), "friendly": friendly_msg }
