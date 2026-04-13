# bots/orchestrator.py
import json
import os
import random
from pathlib import Path

# ML dependencies para clasificación semántica
# ML dependencies para clasificación semántica (opcionales en producción)
try:
    import torch
    from sentence_transformers import SentenceTransformer, util as st_util
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    torch = None
    SentenceTransformer = None
    st_util = None

# En producción evitamos cargar modelos pesados para estabilidad.
if os.getenv("PRODUCTION", "false").lower() == "true" or os.getenv("DISABLE_ML", "false").lower() == "true":
    ML_AVAILABLE = False

from .utils import normalize
from .content_manager import ContentManager
from .logger import logger
from .rss_manager import get_rss_manager
from .directory_connector import get_directory_connector

# Importa bots disponibles
from .bot_accommodation import responder_consulta as acc_responder
from .bot_legal import responder_consulta as leg_responder
from .bot_comercial import responder_consulta as com_responder
from .bot_education import responder_consulta as edu_responder
from .bot_healthcare import responder_consulta as hea_responder
from .bot_work import responder_consulta as work_responder
from .bot_service import responder_consulta as srv_responder
from .bot_immigration import ImmigrationBot


def generic_responder(pregunta, anunciantes, language="en"):
    """
    Un bot genérico que no hace ningún filtrado adicional.
    Devuelve todos los anunciantes que el orquestador ha
    seleccionado para esa categoría.
    El orquestador se encargará de aplicar limit/offset.
    """
    return {"key_points": [], "json_data": anunciantes}


class Orchestrator:
    def __init__(self):
        # --- INICIALIZAR CONECTOR CON DIRECTORIO REAL ---
        # Esto intenta conectar con Barcelona Metropolitan
        # Si falla, usa anunciantes.json como fallback
        self.directory = get_directory_connector()
        self.use_remote_directory = not (
            os.getenv("PRODUCTION", "false").lower() == "true"
            or os.getenv("FORCE_LOCAL_DIRECTORY", "false").lower() == "true"
        )
        self.enable_recommendation_tracking = (
            os.getenv("ENABLE_RECOMMENDATION_TRACKING", "false").lower() == "true"
        )

        # Cargar anunciantes desde directorio real (o JSON local)
        self.advertisers = self._load_advertisers_from_directory()

        # --- INICIALIZAR GESTOR DE CONTENIDO EDITORIAL ---
        self.content_manager = ContentManager()

        # --- INICIALIZAR RSS MANAGER ---
        self.rss_manager = get_rss_manager()

        # Modelo semántico para clasificación inteligente
        # Modelo semántico para clasificación inteligente (opcional)
        if ML_AVAILABLE:
            model_name = 'paraphrase-multilingual-MiniLM-L12-v2'
            self.model = SentenceTransformer(model_name)
        else:
            self.model = None
            logger.warning("Torch/sentence-transformers no disponible. Clasificación por palabras clave.")

        # Patrones de intención (depurados) - Versión simplificada sin ML
        self.category_patterns = {  # Separado por idioma
            "es": {
                "Accommodation": [
                    "hotel", "apartamento", "alojamiento", "vivienda",
                    "alquiler", "piso", "hostal", "renta", "habitacion",
                    "hospedaje", "estancia"
                ],
                "Arts and Culture": [
                    "museo", "galeria", "exposicion", "arte", "cultural",
                    "teatro", "concierto"
                ],
                "Bars and Clubs": [
                    "bar", "discoteca", "pub", "copas", "noche", "fiesta",
                    "club", "karaoke", "terraza", "coctel"
                ],
                "Beauty and Well-Being": [
                    "spa", "masaje", "estetica", "belleza", "bienestar",
                    "peluqueria", "manicura", "facial", "salon"
                ],
                "Business Services": [
                    "negocio", "empresa", "corporativo", "consultoría",
                    "oficina", "servicios", "coworking"
                ],
                "Education": [
                    "escuela", "colegio", "universidad", "curso",
                    "idiomas", "academia", "formacion", "master",
                    "posgrado", "clases", "taller"
                ],
                "Healthcare": [
                    "doctor", "hospital", "clinica", "dentista", "seguro",
                    "salud", "pediatra", "ginecologo", "farmacia",
                    "emergencia", "especialista", "psicologo", "terapia"
                ],
                "Home Services": [
                    "reparacion", "limpieza", "fontanero", "electricista",
                    "carpintero", "mudanza", "pintor", "jardineria"
                ],
                "Legal and Financial": [
                    "abogado", "legal", "financiero", "impuestos", "banco",
                    "contrato", "nif", "gestoria", "gestor",
                    "cuenta bancaria", "declaracion renta"
                ],
                "Immigration": [
                    "visado", "visa", "nie", "residencia", "permiso",
                    "inmigracion", "extranjeria", "empadronamiento",
                    "mudanza", "mudarme", "vivir en españa", "requisitos",
                    "documentacion", "primeros pasos", "extranjero",
                    "inmigrar", "emigrar", "trasladarme", "formulario",
                    "mudarse", "trasladarse", "venir", "venir a españa",
                    "llegar a españa", "desde usa", "desde reino unido",
                    "desde canada", "desde australia", "necesito para",
                    "que necesito", "como emigrar", "como inmigrar",
                    "pasaporte", "tramites", "papeles", "certificado"
                ],
                "Recreation and Leisure": [
                    "ocio", "recreacion", "deporte", "gimnasio", "parque",
                    "entretenimiento"
                ],
                "Restaurants": [
                    "restaurante", "comida", "cenar", "menu", "reserva",
                    "terraza", "cocina", "tapas", "brunch", "desayuno",
                    "almuerzo", "pizzeria"
                ],
                "Retail": [
                    "tienda", "compras", "producto", "ropa", "moda",
                    "centro comercial"
                ],
                "Comercial": [
                    "anunciar", "publicidad", "paquete", "campaña",
                    "promocion", "revista", "media kit", "marketing",
                    "anunciate", "colaborar", "patrocinar"
                ],
                "BotService": [
                    "bot", "agendamiento", "citas", "reservas",
                    "asistente virtual", "chatbot"
                ]
            },
            "en": {
                "Accommodation": [
                    "hotel", "apartment", "housing", "flat", "hostel",
                    "room", "rent", "accommodation"
                ],
                "Arts and Culture": [
                    "museum", "gallery", "exhibition", "art", "cultural",
                    "theater", "concert"
                ],
                "Bars and Clubs": [
                    "bar", "club", "pub", "drinks", "night", "party",
                    "karaoke", "terrace", "cocktail", "nightlife"
                ],
                "Beauty and Well-Being": [
                    "spa", "massage", "beauty", "wellness", "hairdresser",
                    "manicure", "facial", "salon"
                ],
                "Business Services": [
                    "business", "company", "corporate", "consulting",
                    "office", "services", "coworking"
                ],
                "Education": [
                    "school", "college", "university", "course",
                    "languages", "academy", "training", "master",
                    "postgraduate", "classes", "workshop"
                ],
                "Healthcare": [
                    "doctor", "hospital", "clinic", "dentist", "insurance",
                    "health", "pediatrician", "gynecologist", "pharmacy",
                    "emergency", "specialist", "psychologist", "therapy"
                ],
                "Home Services": [
                    "repair", "cleaning", "plumber", "electrician",
                    "carpenter", "moving", "painter", "gardening"
                ],
                "Legal and Financial": [
                    "lawyer", "legal", "financial", "tax", "bank",
                    "contract", "bank account",
                    "tax return", "consultant"
                ],
                "Immigration": [
                    "visa", "nie", "residency", "permit",
                    "immigration", "residency permit", "move to spain",
                    "living in spain", "requirements", "documentation",
                    "first steps", "foreigner", "relocate", "relocating",
                    "emigrate", "immigrate", "registration", "empadronamiento",
                    "moving", "settle", "from usa", "from uk", "from canada",
                    "from australia", "citizenship", "papers",
                    "procedures", "formalities", "passport"
                ],
                "Recreation and Leisure": [
                    "leisure", "recreation", "sports", "gym", "park",
                    "entertainment", "fun"
                ],
                "Restaurants": [
                    "restaurant", "food", "dinner", "menu", "reservation",
                    "terrace", "lunch", "cuisine", "tapas", "brunch",
                    "breakfast", "pizzeria"
                ],
                "Retail": [
                    "store", "shopping", "retail", "product", "clothes",
                    "fashion", "shop", "mall", "clothing"
                ],
                "Comercial": [
                    "advertise", "advertising", "package", "campaign",
                    "promotion", "magazine", "media kit", "ads",
                    "marketing", "collaborate", "sponsorship", "partner"
                ],
                "BotService": [
                    "bot", "scheduling", "appointments", "booking",
                    "virtual assistant", "chatbot"
                ]
            }
        }

        # --- MAPA DE BOTS UNIFICADO ---
        # Ahora, todas las categorías tienen un bot asignado.
        # Usamos el bot genérico para las categorías que no
        # necesitan lógica especial.
        self.bots_map = {
            "Accommodation": acc_responder,
            "Legal and Financial": leg_responder,
            "Comercial": com_responder,
            "Education": edu_responder,
            "Healthcare": hea_responder,
            "Work and Networking": work_responder,  # Categoría faltante
            "BotService": srv_responder,
            "Immigration": self._immigration_responder,  # Bot de inmigración
            # Bots que usan la lógica genérica
            "Arts and Culture": generic_responder,
            "Bars and Clubs": generic_responder,
            "Beauty and Well-Being": generic_responder,
            "Business Services": generic_responder,
            "Home Services": generic_responder,
            "Recreation and Leisure": generic_responder,
            "Restaurants": generic_responder,
            "Retail": generic_responder,
        }

        # Respuestas amigables por categoría
        self.responses_map = {
            "es": {
                "Healthcare": [
                    ("Veo que preguntas sobre salud. Te conecto con "
                     "nuestro bot de Salud."),
                    "Parece que necesitas información médica. "
                    "Nuestro bot de Salud puede guiarte.",
                    "Los temas de salud son importantes. "
                    "Nuestro bot de Salud te ayudará con esto.",
                    "Claro, aquí tienes información sobre servicios "
                    "de salud en Barcelona.",
                    "Entendido, buscando opciones de salud para ti."
                ],
                "Legal and Financial": [
                    "Parece que necesitas ayuda legal o financiera. "
                    "Nuestro bot Legal te ayudará.",
                    "Esto parece una pregunta sobre visados o contratos. "
                    "Te conecto con el bot Legal.",
                    ("Los asuntos legales y financieros pueden ser "
                     "complicados. Nuestro bot Legal está aquí para "
                     "ayudar."),
                    "¡Por supuesto! Navegar la burocracia puede ser "
                    "difícil. Aquí tienes algunos expertos.",
                    "Entendido. Te muestro especialistas en temas "
                    "legales y financieros."
                ],
                "Accommodation": [
                    "¿Buscando alojamiento? El bot de Alojamiento te "
                    "mostrará opciones.",
                    "Estás buscando un lugar donde quedarte. Te conecto "
                    "con nuestro bot de Alojamiento.",
                    "Las preguntas sobre alojamiento son comunes. "
                    "Nuestro bot puede guiarte.",
                    ("¡Claro! Te ayudo a encontrar tu próximo hogar en "
                     "Barcelona. Aquí tienes algunas opciones:"),
                    ("Entendido, buscando el lugar perfecto para ti. Te paso "
                     "con nuestro especialista en alojamiento."),
                ],
                "Education": [
                    ("¿Interesado en escuelas o cursos? Nuestro bot de "
                     "Educación puede guiarte."),
                    ("¿Buscas clases de idiomas o universidades? El bot de "
                     "Educación tiene los detalles."),
                    "La educación es clave. Te conecto con nuestro bot "
                    "de Educación.",
                    "Perfecto, aquí tienes información sobre centros "
                    "educativos en la ciudad.",
                    ("¡Genial! Invertir en formación siempre es una buena "
                     "idea. Mira estas opciones:"),
                ],
                "Work and Networking": [
                    ("¿Buscando trabajo u oportunidades de networking? El "
                     "bot de Empleo puede ayudarte."),
                    ("Las preguntas sobre carrera son importantes. Nuestro "
                     "bot de Empleo te guiará."),
                    ("Te conectamos con el bot de Empleo para oportunidades "
                     "profesionales."),
                    ("Claro, te muestro información sobre el mercado laboral "
                     "y eventos de networking."),
                    ("¡A por ello! Aquí tienes recursos para tu carrera "
                     "profesional en Barcelona."),
                ],
                "Social and Cultural": [
                    ("¿Quieres explorar la vida social y cultural? El bot "
                     "Social puede guiarte."),
                    ("¿Buscas eventos o actividades culturales? El bot "
                     "Social tiene sugerencias."),
                    ("Las experiencias sociales y culturales importan. Te "
                     "conecto con nuestro bot Social."),
                    ("¡Fantástico! Barcelona tiene una vida cultural increíble. "
                     "Aquí tienes algunas ideas:"),
                    ("Perfecto, te ayudo a descubrir los mejores planes "
                     "sociales y culturales."),
                ],
                "Comercial": [
                    ("¿Interesado en anunciarte con nosotros? El bot "
                     "Comercial puede explicarte los paquetes."),
                    ("¿Buscas oportunidades de promoción? El bot Comercial "
                     "te guiará."),
                    ("El marketing y la publicidad son importantes. Te "
                     "conectamos con nuestro bot Comercial."),
                    ("¡Genial que quieras colaborar! Aquí tienes la "
                     "información sobre nuestros paquetes de publicidad."),
                    ("Claro, te muestro cómo tu negocio puede llegar a miles "
                     "de expatriados en Barcelona."),
                ],
                "BotService": [
                    ("Parece que preguntas sobre nuestros servicios de bots "
                     "personalizados. Te doy los detalles."),
                    ("¿Interesado en un chatbot para tu negocio? Puedo "
                     "darte más información."),
                    ("Puedo ayudarte con eso. Aquí tienes información sobre "
                     "los servicios de bot que ofrecemos."),
                    ("¡Claro! Un asistente virtual puede transformar tu "
                     "negocio. Esto es lo que ofrecemos:"),
                    ("Detecto que preguntas por mis 'poderes'. ¡Te cuento "
                     "cómo puedes tener un asistente como yo!")
                ],
                "Immigration": [
                    ("Veo que preguntas sobre inmigración y documentación. "
                     "Nuestro bot especializado te ayudará."),
                    ("¿Planeas mudarte a España? El bot de Inmigración "
                     "tiene toda la información que necesitas."),
                    ("Los trámites de inmigración pueden ser complejos. Te "
                     "conecto con nuestro experto."),
                    ("¡Perfecto! Te ayudo con visados, NIE y primeros pasos "
                     "para vivir en España."),
                    ("Entendido, aquí tienes información detallada sobre "
                     "requisitos de inmigración."),
                ]
            },
            "en": {
                "Healthcare": [
                    ("I see you're asking about health. Let me connect "
                     "you with our Healthcare bot."),
                    ("Looks like you need medical information. Our "
                     "Healthcare bot can guide you to clinics and doctors."),
                    ("Health matters are important. I'll let our "
                     "Healthcare bot assist you."),
                    ("Of course, here's some information about healthcare "
                     "services in Barcelona."),
                    "Understood, looking for health options for you."
                ],
                "Legal and Financial": [
                    ("You seem to need legal or financial help. Our Legal "
                     "bot will assist you."),
                    ("This looks like a question about visas or contracts. "
                     "Let's connect you with the Legal bot."),
                    ("Legal and financial issues can be tricky. Our Legal "
                     "bot is here to help."),
                    ("Of course! Navigating bureaucracy can be tough. Here "
                     "are some experts."),
                    ("Understood. I'll show you specialists for legal and "
                     "financial matters.")
                ],
                "Accommodation": [
                    ("Searching for housing? The Accommodation bot will "
                     "show you options."),
                    ("You're looking for a place to stay. Let me connect "
                     "you with our Accommodation bot."),
                    ("Accommodation questions are common. Our bot can guide "
                     "you to rentals and housing."),
                    ("Sure! Let me help you find your next home in "
                     "Barcelona. Here are some options:"),
                    ("Got it, looking for the perfect place for you. I'll "
                     "connect you with our accommodation specialist.")
                ],
                "Education": [
                    ("Interested in schools or courses? Our Education bot "
                     "can guide you."),
                    ("Looking for language classes or universities? The "
                     "Education bot has the details."),
                    ("Education is key. Let me connect you with our "
                     "Education bot."),
                    ("Perfect, here's some information about educational "
                     "centers in the city."),
                    ("Great! Investing in training is always a good idea. "
                     "Check out these options:")
                ],
                "Work and Networking": [
                    ("Searching for jobs or networking opportunities? The "
                     "Work bot can help."),
                    ("Career questions are important. Our Work bot will "
                     "guide you."),
                    ("Let's connect you with the Work bot for professional "
                     "opportunities."),
                    ("Sure, I'll show you information about the job market "
                     "and networking events."),
                    ("Let's do it! Here are resources for your professional "
                     "career in Barcelona.")
                ],
                "Social and Cultural": [
                    ("Want to explore culture and social life? Our Social "
                     "bot can guide you."),
                    ("Looking for events or cultural activities? The Social "
                     "bot has suggestions."),
                    ("Social and cultural experiences are important. Let me "
                     "connect you with our Social bot."),
                    ("Fantastic! Barcelona has an incredible cultural life. "
                     "Here are some ideas:"),
                    ("Perfect, let me help you discover the best social and "
                     "cultural plans.")
                ],
                "Comercial": [
                    ("Interested in advertising with us? The Comercial bot "
                     "can explain packages."),
                    ("Looking for promotion opportunities? The Comercial bot "
                     "will guide you."),
                    ("Marketing and ads are important. Let's connect you "
                     "with our Comercial bot."),
                    ("Great that you want to collaborate! Here is the "
                     "information about our advertising packages."),
                    ("Sure, I'll show you how your business can reach "
                     "thousands of expats in Barcelona.")
                ],
                "BotService": [
                    ("It looks like you're asking about our custom bot "
                     "services. Let me get you the details."),
                    ("Interested in a chatbot for your business? I can "
                     "provide more information on that."),
                    ("I can help with that. Here is some information about "
                     "the bot services we offer to advertisers."),
                    ("Of course! A virtual assistant can transform your "
                     "business. Here's what we offer:"),
                    ("I detect you're asking about my 'powers'. I'll tell "
                     "you how you can have an assistant like me!")
                ],
                "Immigration": [
                    ("I see you're asking about immigration and "
                     "documentation. Our specialized bot will help you."),
                    ("Planning to move to Spain? The Immigration bot has "
                     "all the information you need."),
                    ("Immigration procedures can be complex. Let me connect "
                     "you with our expert."),
                    ("Perfect! I'll help you with visas, NIE and first "
                     "steps to live in Spain."),
                    ("Understood, here's detailed information about "
                     "immigration requirements.")
                ]
            }
        }

        # --- PRE-CÁLCULO DE EMBEDDINGS PARA CLASIFICACIÓN SEMÁNTICA ---
        # --- PRE-CÁLCULO DE EMBEDDINGS (solo si ML disponible) ---
        self.category_info = []
        self.category_embeddings_tensor = None
        if ML_AVAILABLE and self.model is not None:
            all_categories = set(self.category_patterns.get("es", {}).keys()) | set(self.category_patterns.get("en", {}).keys())
            for category in all_categories:
                keywords_es = self.category_patterns.get("es", {}).get(category, [])
                keywords_en = self.category_patterns.get("en", {}).get(category, [])
                description = f"Servicios sobre {category.lower()}: " + ", ".join(keywords_es + keywords_en)
                self.category_info.append({
                    "name": category,
                    "description": description,
                    "embedding": self.model.encode(description, convert_to_tensor=True)
                })
            self.category_embeddings_tensor = torch.stack([cat["embedding"] for cat in self.category_info])
            logger.info(f"Tensor de embeddings pre-calculado: {self.category_embeddings_tensor.shape}")
        else:
            logger.info("Clasificación semántica deshabilitada. Usando solo palabras clave.")

        # --- OPTIMIZACIÓN: ÍNDICE DE NOMBRES DE NEGOCIOS ---
        # Crea un índice para búsqueda O(1) en lugar de O(n²)
        self.business_name_index = {}
        for category, businesses in self.advertisers.items():
            for business in businesses:
                name = normalize(business.get('nombre', ''))
                if name:
                    self.business_name_index[name] = (category, business)
        logger.info(f"Índice de negocios creado: {len(self.business_name_index)} nombres indexados")

        # --- CONSEJOS RÁPIDOS POR CATEGORÍA ---
        self.tips_map = {
            "es": {
                "Legal and Financial": [
                    "Verifica experiencia en extranjería (NIE/visas) y plazos.",
                    "Solicita presupuesto cerrado y detalle de servicios.",
                    "Pregunta por atención en tu idioma y seguimiento del caso."
                ],
                "Healthcare": [
                    "Confirma seguro aceptado y disponibilidad en tu zona.",
                    "Pregunta por atención en tu idioma y tiempos de cita.",
                    "Revisa especialidades y emergencias 24h si las necesitas."
                ],
                "Education": [
                    "Define idioma de instrucción y programa (IB/británico/español).",
                    "Consulta calendario de admisiones y visitas guiadas.",
                    "Valora distancia, transporte escolar y actividades."
                ],
                "Accommodation": [
                    "Revisa contrato, fianza y gastos incluidos (agua/luz/internet).",
                    "Valora barrio y distancias a trabajo/escuela.",
                    "Pide inventario y fotografías del estado del inmueble."
                ],
                "Restaurants": [
                    "Reserva si es fin de semana o local popular.",
                    "Pregunta por opciones en tu idioma y dietas (sin gluten/veg).",
                    "Revisa ubicación y horarios (brunch, cocina continua)."
                ],
                "Home Services": [
                    "Solicita presupuesto detallado y plazos.",
                    "Pide referencias y garantía del trabajo.",
                    "Confirma disponibilidad en tu zona."
                ],
                "Business Services": [
                    "Aclara entregables y comunicación (idioma/horarios).",
                    "Solicita caso de éxito o referencias.",
                    "Define plazos y cláusulas de revisión."
                ],
                "Bars and Clubs": [
                    "Consulta dress code y horarios de entrada.",
                    "Revisa ubicación y opciones de transporte nocturno.",
                    "Pregunta por eventos/guest list para evitar colas."
                ],
                "Arts and Culture": [
                    "Revisa agenda y entradas anticipadas.",
                    "Valora idiomas de las exposiciones/tours.",
                    "Explora descuentos para residentes/estudiantes."
                ],
                "Recreation and Leisure": [
                    "Consulta niveles/edades si es actividad deportiva.",
                    "Pregunta por horarios y material necesario.",
                    "Valora cercanía y grupos en tu idioma."
                ],
                "Retail": [
                    "Revisa políticas de devoluciones y tallaje.",
                    "Pregunta por atención en tu idioma.",
                    "Valora ubicaciones y horarios extendidos."
                ]
            },
            "en": {
                "Legal and Financial": [
                    "Check immigration (NIE/visa) expertise and timelines.",
                    "Ask for fixed-fee quotes and service breakdown.",
                    "Confirm language support and case follow-up."
                ],
                "Healthcare": [
                    "Confirm accepted insurance and nearby availability.",
                    "Ask about language support and appointment times.",
                    "Check specialties and 24h emergency if needed."
                ],
                "Education": [
                    "Choose language/program (IB/British/Spanish).",
                    "Check admissions calendar and school tours.",
                    "Consider distance, transport and activities."
                ],
                "Accommodation": [
                    "Review contract, deposit and included utilities.",
                    "Consider neighborhood and commute distances.",
                    "Request inventory and property condition photos."
                ]
            }
        }

    def _immigration_responder(self, question, anunciantes, language="es"):
        """
        Bot adapter para inmigración que devuelve formato compatible
        con orquestador.
        Incluye legal_ads en la respuesta.
        """
        bot = ImmigrationBot(language=language)
        mensaje = bot.get_response(question)

        return {
            "key_points": [
                "Información sobre visados, NIE y documentación",
                "Primeros pasos para vivir en España",
                "Firmas legales especializadas en inmigración"
            ],
            "json_data": bot.legal_ads  # Anunciantes legales de la revista
        }

    def _load_advertisers_from_directory(self) -> dict:
        """
        Carga anunciantes desde el directorio real de Barcelona Metropolitan.

        Si la API está disponible, obtiene datos actualizados.
        Si falla, usa anunciantes.json como fallback.

        Organiza los anunciantes por categorías para compatibilidad
        con el código existente.

        Returns:
            Dict con estructura: {"Categoría": [anunciantes]}
        """
        try:
            if not self.use_remote_directory:
                logger.info("Modo local activo: cargando anunciantes desde JSON local")
                return self._load_local_json()

            logger.info(
            "🔄 Cargando anunciantes desde directorio Barcelona Metropolitan..."
        )

            # Obtener todos los anunciantes desde el directorio
            all_advertisers = self.directory.get_all_advertisers(limit=500)

            if not all_advertisers:
                logger.warning("⚠️ El directorio está vacío, usando JSON local")
                return self._load_local_json()

            # Organizar por categorías
            categorized = {}
            for advertiser in all_advertisers:
                category = advertiser.get('category', advertiser.get('categoria', 'Other'))

                if category not in categorized:
                    categorized[category] = []

                categorized[category].append(advertiser)

            logger.info(f"✅ Cargados {len(all_advertisers)} anunciantes de {len(categorized)} categorías")
            return categorized

        except Exception as e:
            logger.error(f"❌ Error cargando directorio: {e}")
            logger.info("📄 Usando anunciantes.json como fallback")
            return self._load_local_json()

    def _load_local_json(self) -> dict:
        """
        Fallback: Carga anunciantes desde JSON local.

        Returns:
            Dict con estructura: {"Categoría": [anunciantes]}
        """
        try:
            base_dir = Path(__file__).resolve().parent.parent
            data_path = base_dir / "data" / "anunciantes.json"

            with open(str(data_path), 'r', encoding='utf-8') as f:
                advertisers = json.load(f)

            logger.info(f"✅ Anunciantes JSON cargados: {len(advertisers)} categorías")
            return advertisers

        except Exception as e:
            logger.error(f"❌ Error cargando JSON local: {e}")
            return {}

    def classify_intent(self, question, language="en"):
        qn = normalize(question)

        # --- PRIORIDAD CRÍTICA: Palabras clave de inmigración ---
        # NIE, visados, mudanza son términos muy específicos que deben ir a Immigration
        critical_immigration_keywords = {
                 'es': ['nie', 'visado', 'visa', 'mudarme', 'mudanza', 'residencia',
                     'empadronamiento', 'empadronar', 'empadronarme', 'trasladarme',
                     'desde usa', 'desde reino unido', 'desde canada', 'desde australia',
                     'inmigrar', 'emigrar', 'permiso de residencia', 'permiso residencia'],
                 'en': ['nie', 'visa', 'residency', 'residence permit', 'relocat',
                     'move to spain', 'moving to spain', 'from usa', 'from uk',
                     'from canada', 'from australia', 'immigrat', 'emigrat',
                     'registration padrón', 'padrón', 'empadronamiento']
        }

        keywords_to_check = critical_immigration_keywords.get(language, critical_immigration_keywords['en'])
        for keyword in keywords_to_check:
            if keyword in qn:
                logger.debug(f"🔒 OVERRIDE CRÍTICO: '{keyword}' detectado → Immigration")
                return "Immigration", 0.95, None

        # --- LÓGICA DE BÚSQUEDA SEMÁNTICA ---
        # --- LÓGICA DE BÚSQUEDA SEMÁNTICA (solo si ML disponible) ---
        best_score = 0.0
        best_match_category = None
        if ML_AVAILABLE and self.model is not None and self.category_embeddings_tensor is not None:
            question_embedding = self.model.encode(question, convert_to_tensor=True)
            cos_scores = st_util.cos_sim(question_embedding, self.category_embeddings_tensor)[0]
            top_result = int(cos_scores.argmax().item())
            best_score = float(cos_scores[top_result].item())
            best_match_category = self.category_info[top_result]["name"]
            logger.debug(f"Clasificación semántica: '{best_match_category}' conf={best_score:.4f}")

        # --- LÓGICA DE OVERRIDE: Coincidencia directa con nombres de negocios ---
        # Si la pregunta menciona un negocio por su nombre, esa intención tiene prioridad.
        # OPTIMIZADO: Usa índice pre-calculado O(n) en lugar de O(n²)
        for name, (category, business) in self.business_name_index.items():
            if name in qn:
                logger.debug(f"Coincidencia directa negocio='{business.get('nombre', '')}' categoria='{category}'")
                return category, 0.9, business

        # --- LÓGICA DE OVERRIDE: Coincidencia por palabras clave declarativas ---
        # Contamos hits por categoría usando los patrones declarados para el idioma.
        kw_map = self.category_patterns.get(language, {})
        best_kw_cat = None
        best_hits = 0
        for cat, kws in kw_map.items():
            hits = sum(1 for kw in kws if kw in qn)
            if hits > best_hits:
                best_hits = hits
                best_kw_cat = cat
        if best_kw_cat and best_hits > 0:
            # Devolvemos la categoría por palabras clave con una confianza mínima razonable
            return best_kw_cat, max(0.25, min(0.9, 0.15 * best_hits + 0.25)), None

        # Si la confianza semántica es alta, la usamos. Si no, consideramos la intención como desconocida.
        if best_score > 0.2: # Umbral de confianza ajustado para consultas cortas
            return best_match_category, best_score, None
        else:
            return "Desconocida", best_score, None

    def process_query(self, question, language="en", limit: int = 3, offset: int = 0):
        categoria, confidence, advertiser = self.classify_intent(question, language)
        lang = language if language in self.responses_map else "en"
        resultados = self.advertisers.get(categoria, [])
        if advertiser and advertiser not in resultados:
            resultados.insert(0, advertiser)

        # Mensaje amigable del orquestador
        friendly_msg = ""
        if categoria in self.responses_map[lang]:
            friendly_msg = random.choice(self.responses_map[lang][categoria])

        # --- BUSCAR CONTENIDO EDITORIAL RELEVANTE ---
        # Buscar guías/artículos relacionados con la pregunta
        keywords = [word.lower() for word in question.split() if len(word) > 3]
        guias_relevantes = self.content_manager.search_guides(keywords, categoria)

        # --- BUSCAR ARTÍCULOS EN RSS CACHE ---
        articulos_revista = self.rss_manager.get_articles_by_category(categoria, limit=3)

        # Agregar referencia a guías en el mensaje si hay contenido relevante
        guias_resumen = []
        if guias_relevantes:
            # Tomar las 2 guías más relevantes
            for guia in guias_relevantes[:2]:
                guias_resumen.append(self.content_manager.get_guide_summary(guia))

            # Mejorar el mensaje con referencia al contenido
            if lang == "es":
                friendly_msg += f"\n\n📖 Para más información, consulta nuestra guía: '{guias_relevantes[0]['titulo']}'"
            else:
                friendly_msg += f"\n\n📖 For more information, check our guide: '{guias_relevantes[0]['titulo']}'"

        # Preparar consejos rápidos
        tips = self.tips_map.get(lang, {}).get(categoria, [])

        # Si hay bot específico para la categoría, usarlo
        if categoria in self.bots_map:
            try:
                # 1. Llamamos al bot específico
                bot_response = self.bots_map[categoria](question, resultados, language=lang)

                # 2. Slicing de resultados en el orquestador
                all_items = bot_response.get("json_data", [])
                total = len(all_items)
                if limit is None or limit == 0:
                    sliced = all_items[offset:]
                else:
                    sliced = all_items[offset:offset + limit]
                has_more = (offset + (limit or 0)) < total if limit not in (None, 0) else False
                next_offset = (offset + (limit or 0)) if has_more else None

                # 2.5 NUEVO: Trackear recomendaciones en el directorio
                if sliced and self.enable_recommendation_tracking:
                    session_id = f"session_{offset}_{hash(question) % 10000}"
                    for advertiser in sliced[:limit or 3]:
                        advertiser_id = advertiser.get('id', advertiser.get('nombre', 'unknown'))
                        try:
                            self.directory.track_recommendation(
                                advertiser_id=advertiser_id,
                                query=question,
                                session_id=session_id
                            )
                        except Exception as e:
                            logger.debug(f"⚠️ Error trackeando recomendación: {e}")
                            pass  # No bloquear si falla el tracking

                # 3. Preparamos la respuesta final para el frontend
                return {
                    "respuesta": friendly_msg,
                    "agente": categoria,
                    "confidence": confidence,
                    "json": sliced,
                    "total_results": total,
                    "has_more": has_more,
                    "next_offset": next_offset,
                    "guias": guias_resumen,
                    "articulos": articulos_revista,
                    "tips": tips
                }
            except Exception as e:
                logger.error(f"ERROR ejecutando bot '{categoria}': {e}")
                import traceback
                traceback.print_exc()
                # Si el bot falla, devolvemos una respuesta de error controlada
                return {
                    "respuesta": f"Lo siento, hubo un problema con el asistente de '{categoria}'. Inténtalo de nuevo.",
                    "agente": categoria, "confidence": 0.5, "json": [], "guias": [], "articulos": [], "has_more": False
                }


        # Si la categoría no está en el mapa de bots (no debería pasar ahora), devolvemos un error.
        return { "respuesta": "Lo siento, no tengo un asistente configurado para esa categoría.", "agente": "Orchestrator", "confidence": confidence, "json": [], "articulos": [], "has_more": False }
