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
                "Accommodation": ["hotel", "apartamento", "alojamiento", "vivienda", "alquiler", "piso", "hostal", "renta"],
                "Arts and Culture": ["museo", "galeria", "exposicion", "arte", "cultural", "teatro", "concierto"],
                "Bars and Clubs": ["bar", "discoteca", "pub", "copas", "noche", "fiesta", "club", "karaoke", "terraza", "coctel"],
                "Beauty and Well-Being": ["spa", "masaje", "estetica", "belleza", "bienestar", "peluqueria", "manicura", "facial"],
                "Business Services": ["negocio", "empresa", "corporativo", "consultoria", "asesoria", "oficina", "coworking"],
                "Education": ["escuela", "colegio", "universidad", "curso", "idiomas", "academia", "formacion"],
                "Healthcare": ["medico", "hospital", "clinica", "dentista", "seguro", "salud", "doctor", "pediatra", "ginecologo"],
                "Home Services": ["reparacion", "limpieza", "fontanero", "electricista", "carpintero", "mudanza", "pintor", "jardineria"],
                "Legal and Financial": ["abogado", "legal", "financiero", "impuestos", "banco", "contrato", "visado", "nie", "residencia", "permiso", "nif"],
                "Recreation and Leisure": ["ocio", "recreacion", "deporte", "gimnasio", "parque", "entretenimiento"],
                "Restaurants": ["restaurante", "comida", "cenar", "menu", "reserva", "terraza", "cocina"],
                "Retail": ["tienda", "compras", "producto", "ropa", "moda", "centro comercial"],
                "Comercial": ["anunciar", "publicidad", "paquete", "campaña", "promocion", "revista", "media kit"],
                "BotService": ["bot", "agendamiento", "citas", "reservas", "asistente virtual", "chatbot"]
            },
            "en": {
                "Accommodation": ["hotel", "apartment", "housing", "flat", "hostel", "room", "rent", "accommodation"],
                "Arts and Culture": ["museum", "gallery", "exhibition", "art", "cultural", "theater", "concert"],
                "Bars and Clubs": ["bar", "club", "pub", "drinks", "night", "party", "karaoke", "terrace", "cocktail", "nightlife"],
                "Beauty and Well-Being": ["spa", "massage", "beauty", "wellness", "hairdresser", "manicure", "facial", "salon"],
                "Business Services": ["business", "company", "corporate", "consulting", "office", "services", "coworking"],
                "Education": ["school", "college", "university", "course", "languages", "academy", "training"],
                "Healthcare": ["doctor", "hospital", "clinic", "dentist", "insurance", "health", "pediatrician", "gynecologist"],
                "Home Services": ["repair", "cleaning", "plumber", "electrician", "carpenter", "moving", "painter", "gardening"],
                "Legal and Financial": ["lawyer", "legal", "financial", "tax", "bank", "contract", "visa", "nie", "residency", "permit"],
                "Recreation and Leisure": ["leisure", "recreation", "sports", "gym", "park", "entertainment", "fun"],
                "Restaurants": ["restaurant", "food", "dinner", "menu", "reservation", "terrace", "lunch", "cuisine"],
                "Retail": ["store", "shopping", "retail", "product", "clothes", "fashion", "shop", "mall", "clothing"],
                "Comercial": ["advertise", "advertising", "package", "campaign", "promotion", "magazine", "media kit", "ads", "marketing"],
                "BotService": ["bot", "scheduling", "appointments", "booking", "virtual assistant", "chatbot"]
            }
        }

        # Respuestas amigables por categoría
        self.responses_map = {
            "es": {
                "Healthcare": [
                    "Veo que preguntas sobre salud. Te conecto con nuestro bot de Salud.",
                    "Parece que necesitas información médica. Nuestro bot de Salud puede guiarte.",
                    "Los temas de salud son importantes. Dejaré que nuestro bot de Salud te ayude."
                ],
                "Legal and Financial": [
                    "Parece que necesitas ayuda legal o financiera. Nuestro bot Legal te ayudará.",
                    "Esto parece una pregunta sobre visados o contratos. Te conecto con el bot Legal.",
                    "Los asuntos legales y financieros pueden ser complicados. Nuestro bot Legal está aquí para ayudar."
                ],
                "Accommodation": [
                    "¿Buscando alojamiento? El bot de Alojamiento te mostrará opciones.",
                    "Estás buscando un lugar donde quedarte. Te conecto con nuestro bot de Alojamiento.",
                    "Las preguntas sobre alojamiento son comunes. Nuestro bot puede guiarte."
                ],
                "Education": [
                    "¿Interesado en escuelas o cursos? Nuestro bot de Educación puede guiarte.",
                    "¿Buscas clases de idiomas o universidades? El bot de Educación tiene los detalles.",
                    "La educación es clave. Te conecto con nuestro bot de Educación."
                ],
                "Work and Networking": [
                    "¿Buscando trabajo u oportunidades de networking? El bot de Empleo puede ayudarte.",
                    "Las preguntas sobre carrera son importantes. Nuestro bot de Empleo te guiará.",
                    "Te conectamos con el bot de Empleo para oportunidades profesionales."
                ],
                "Social and Cultural": [
                    "¿Quieres explorar la vida social y cultural? El bot Social puede guiarte.",
                    "¿Buscas eventos o actividades culturales? El bot Social tiene sugerencias.",
                    "Las experiencias sociales y culturales importan. Te conecto con nuestro bot Social."
                ],
                "Comercial": [
                    "¿Interesado en anunciarte con nosotros? El bot Comercial puede explicarte los paquetes.",
                    "¿Buscas oportunidades de promoción? El bot Comercial te guiará.",
                    "El marketing y la publicidad son importantes. Te conectamos con nuestro bot Comercial."
                ],
                "BotService": [
                    "Parece que preguntas sobre nuestros servicios de bots personalizados. Te doy los detalles.",
                    "¿Interesado en un chatbot para tu negocio? Puedo darte más información.",
                    "Puedo ayudarte con eso. Aquí tienes información sobre los servicios de bot que ofrecemos."
                ]
            },
            "en": {
                "Healthcare": [
                    "I see you’re asking about health. Let me connect you with our Healthcare bot.",
                    "Looks like you need medical information. Our Healthcare bot can guide you to clinics and doctors.",
                    "Health matters are important. I’ll bring in our Healthcare bot to assist you."
                ],
                "Legal and Financial": [
                    "You seem to need legal or financial help. Our Legal bot will assist you.",
                    "This looks like a question about visas or contracts. Let’s connect you with the Legal bot.",
                    "Legal and financial issues can be tricky. Our Legal bot is here to help."
                ],
                "Accommodation": [
                    "Searching for housing? The Accommodation bot will show you options.",
                    "You’re looking for a place to stay. Let me connect you with our Accommodation bot.",
                    "Accommodation questions are common. Our bot can guide you to rentals and housing."
                ],
                "Education": [
                    "Interested in schools or courses? Our Education bot can guide you.",
                    "Looking for language classes or universities? The Education bot has the details.",
                    "Education is key. Let me connect you with our Education bot."
                ],
                "Work and Networking": [
                    "Searching for jobs or networking opportunities? The Work bot can help.",
                    "Career questions are important. Our Work bot will guide you.",
                    "Let’s connect you with the Work bot for professional opportunities."
                ],
                "Social and Cultural": [
                    "Want to explore culture and social life? The Social bot can guide you.",
                    "Looking for events or cultural activities? The Social bot has suggestions.",
                    "Social and cultural experiences matter. Let me connect you with our Social bot."
                ],
                "Comercial": [
                    "Interested in advertising with us? The Comercial bot can explain packages.",
                    "Looking for promotion opportunities? The Comercial bot will guide you.",
                    "Marketing and ads are important. Let’s connect you with our Comercial bot."
                ],
                "BotService": [
                    "It looks like you're asking about our custom bot services. Let me get you the details.",
                    "Interested in a chatbot for your business? I can provide more information on that.",
                    "I can help with that. Here is some information about the bot services we offer to advertisers."
                ]
            }
        }

    def classify_intent(self, question, language="en"):
        qn = normalize(question)
        lang = language if language in self.category_patterns else "en"
        patterns_to_use = self.category_patterns[lang]
        best_match, best_score = None, 0
        for category, patterns in patterns_to_use.items():
            score = sum(1 for p in patterns if p in qn)
            if score > best_score:
                best_score, best_match = score, category
        if best_match:
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
                resp = self.bots_map[categoria](question, resultados)
                return {
                    "respuesta": resp.get("text", ""),
                    "agente": categoria,
                    "confidence": confidence,
                    "json": resp.get("json", {}),
                    "friendly": friendly_msg
                }
            except Exception as e:
                print("Error en bot:", categoria, e)

        # Fallback: respuesta básica estandarizada
        resp = make_standard_response(categoria, resultados, question)
        return {
            "respuesta": resp.get("text", ""),
            "agente": categoria,
            "confidence": confidence,
            "json": resp.get("json", {}),
            "friendly": friendly_msg or "I couldn’t classify your question clearly. Try rephrasing it or use our search bar."
        }
