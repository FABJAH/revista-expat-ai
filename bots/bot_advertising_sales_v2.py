"""
Luna Bot - Vendedor de Espacios de Publicidad Bilingual
Estructura: Directorio + Campañas de Marketing
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

MASCOT = "🦉"
BOT_NAME = "Luna"

INTENTS = {
    "saludo": ["hola", "hello", "buenos", "buenos días", "buenos días", "hi", "hey", "qué tal", "buenos días", "buenas noches", "buenas tardes"],
    "planes": ["plan", "precio", "costo", "coste", "cuánto", "cuanto", "tarifa", "planes", "prices", "cost", "package", "subscription"],
    "directorio": ["directorio", "directory", "listing", "aparece", "visibility", "visibilidad", "encontrar", "find"],
    "campana": ["campaña", "campaign", "marketing", "publicidad", "advertising", "promoción", "promotion"],
    "descuento": ["descuento", "discount", "anual", "annual", "oferta", "offer", "10%"],
    "contacto": ["contacto", "contact", "email", "teléfono", "phone", "cómo", "how", "ayuda", "help"],
    "negociable": ["negociar", "negotiate", "precio", "budget", "presupuesto", "personalizado", "custom"],
}

RESPONSES_DIRECTORIO = {
    "es": {
        "breve": "📍 Nuestro **Directorio** es simple: **34€/mes** apareces ante 12,000+ usuarios mensuales.",
        "completo": "📍 **DIRECTORIO - 34€/mes**\n- Perfil completo con foto y descripción\n- Visible a 12,000+ usuarios/mes\n- Analytics de visitas\n- Soporte por email\n- SIN campaña de marketing",
        "vs_campana": "**Directorio** = Estar listado (34€)\n**Campaña** = Marketing activo (159€+)\n¿Cuál prefieres?"
    },
    "en": {
        "breve": "📍 Our **Directory** is simple: **34€/month** appear to 12,000+ monthly users.",
        "completo": "📍 **DIRECTORY - 34€/month**\n- Complete profile with photo and description\n- Visible to 12,000+ users/month\n- Visit analytics\n- Email support\n- NO marketing campaign",
        "vs_campana": "**Directory** = Being listed (34€)\n**Campaign** = Active marketing (159€+)\nWhich do you prefer?"
    }
}

RESPONSES_CAMPANA = {
    "es": {
        "breve": "📢 Nuestras **Campañas** te ayudan a llegar nuevos clientes: desde **159€/mes** (mín. 6 meses).",
        "opciones": "📢 **CAMPAÑAS DE MARKETING**\n\n🔹 **Básica** (159€/mes) - Estrategia inicial\n🔹 **Profesional** (199€/mes) - La más popular\n🔹 **Premium** (299€/mes) - Máximo impacto\n\nTodas incluyen: acompañamiento de la revista, análisis y soporte.",
        "minimo": "⏰ Mínimo **6 meses**. Si pagas 12 meses = **10% descuento**.",
        "negociable": "💬 Los precios son **negociables** según tus necesidades. ¿Hablamos?"
    },
    "en": {
        "breve": "📢 Our **Campaigns** help you reach new customers: from **159€/month** (min. 6 months).",
        "opciones": "📢 **MARKETING CAMPAIGNS**\n\n🔹 **Basic** (159€/month) - Initial strategy\n🔹 **Professional** (199€/month) - Most popular\n🔹 **Premium** (299€/month) - Maximum impact\n\nAll include: magazine support, analysis and support.",
        "minimo": "⏰ Minimum **6 months**. Pay 12 months = **10% discount**.",
        "negociable": "💬 Prices are **negotiable** based on your needs. Let's talk?"
    }
}

TESTIMONIOS = {
    "es": [
        {
            "empresa": "Restaurante La Viña",
            "sector": "Restaurante",
            "testimonio": "Pasamos de 5 clientes nuevos/mes a 45 con la campaña profesional. Luna nos ayudó a llegar a más personas.",
            "resultado": "+800% clientes nuevos"
        },
        {
            "empresa": "Academia Idiomas Plus",
            "sector": "Educación",
            "testimonio": "El directorio nos dio visibilidad y la campaña nos dio resultados. Muy recomendado.",
            "resultado": "+12 estudiantes nuevos"
        },
        {
            "empresa": "Clínica Dental Smile",
            "sector": "Salud",
            "testimonio": "Excelente equipo. Nos explicaron la estrategia paso a paso. Hemos triplicado nuestras llamadas.",
            "resultado": "+45 pacientes nuevos"
        }
    ],
    "en": [
        {
            "empresa": "Restaurant La Viña",
            "sector": "Restaurant",
            "testimonio": "We went from 5 new customers/month to 45 with the professional campaign. Luna helped us reach more people.",
            "resultado": "+800% new customers"
        },
        {
            "empresa": "Languages Academy Plus",
            "sector": "Education",
            "testimonio": "The directory gave us visibility and the campaign gave us results. Highly recommended.",
            "resultado": "+12 new students"
        },
        {
            "empresa": "Smile Dental Clinic",
            "sector": "Health",
            "testimonio": "Excellent team. They explained the strategy step by step. We tripled our calls.",
            "resultado": "+45 new patients"
        }
    ]
}

FAQ = {
    "es": {
        "¿cuál es la diferencia entre directorio y campaña?": "📍 **Directorio** (34€) = Estás listado, usuarios te encuentran. 📢 **Campaña** (159€+) = Nosotros te promocionamos activamente para traerte clientes nuevos.",
        "¿son negociables los precios?": "💬 Sí, los precios de campaña son negociables. Depende de tus necesidades, sector y presupuesto. ¡Hablemos!",
        "¿cuál es el mínimo para campañas?": "⏰ Mínimo **6 meses**. Anual = **10% descuento**.",
        "¿qué incluye el directorio?": "✅ Perfil completo, visibilidad ante 12k+ usuarios, analytics, soporte. NO incluye marketing.",
        "¿qué incluye la campaña?": "✅ Todo del directorio + Marketing activo + Estrategia personalizada + Acompañamiento + Reportes.",
        "¿hay descuento anual?": "🎁 Sí! Si contratas **12 meses** = **10% descuento** en campaña. Básica: 159×12×0.9 = 1.721€/año.",
        "¿cómo es el acompañamiento?": "👥 Equipo dedicado, reportes mensuales, ajustes continuos, soporte email/teléfono.",
        "¿puedo cancelar antes?": "❌ Mínimo 6 meses para campañas. Directorio es flexible.",
    },
    "en": {
        "what's the difference between directory and campaign?": "📍 **Directory** (34€) = You're listed, users find you. 📢 **Campaign** (159€+) = We actively promote you to bring new customers.",
        "are prices negotiable?": "💬 Yes, campaign prices are negotiable. Depends on your needs, sector and budget. Let's talk!",
        "what's the minimum for campaigns?": "⏰ Minimum **6 months**. Annual = **10% discount**.",
        "what's included in the directory?": "✅ Complete profile, visibility to 12k+ users, analytics, support. NO marketing.",
        "what's included in the campaign?": "✅ Everything from directory + Active marketing + Personalized strategy + Support + Reports.",
        "is there an annual discount?": "🎁 Yes! If you contract **12 months** = **10% discount** on campaign. Basic: 159×12×0.9 = 1,721€/year.",
        "what's the support like?": "👥 Dedicated team, monthly reports, continuous adjustments, email/phone support.",
        "can i cancel early?": "❌ Minimum 6 months for campaigns. Directory is flexible.",
    }
}

# ============================================================================
# CLASE BOT
# ============================================================================

class AdvertisingSalesBot:
    """Bot de Luna para venta de espacios publicitarios."""

    def __init__(self, language: str = "es"):
        self.language = language.lower()
        if self.language not in ["es", "en"]:
            self.language = "es"

    def detect_language(self, text: str) -> str:
        """Detectar idioma del texto."""
        spanish_words = ["hola", "buenos", "qué", "cómo", "dónde", "cuándo", "presupuesto"]
        english_words = ["hello", "hi", "how", "what", "where", "budget", "price"]

        text_lower = text.lower()
        spanish_count = sum(1 for word in spanish_words if word in text_lower)
        english_count = sum(1 for word in english_words if word in text_lower)

        return "en" if english_count > spanish_count else "es"

    def detect_intent(self, text: str) -> str:
        """Detectar intención del usuario."""
        text_lower = text.lower()

        for intent, keywords in INTENTS.items():
            if any(keyword in text_lower for keyword in keywords):
                return intent

        return "general"

    def get_greeting(self) -> str:
        """Saludo inicial."""
        hour = datetime.now().hour

        if self.language == "es":
            if 6 <= hour < 12:
                return f"{MASCOT} ¡Buenos días! Soy **Luna**. Aquí ayudamos a que tu negocio crezca. 📍 **Directorio** (34€/mes) o 📢 **Campaña** (desde 159€/mes). ¿Cuál te interesa?"
            elif 12 <= hour < 18:
                return f"{MASCOT} ¡Buenas tardes! Soy **Luna**. 280+ negocios ya están con nosotros. ¿Quieres unirte?"
            else:
                return f"{MASCOT} ¡Buenas noches! Soy **Luna**, tu asistente de marketing. Cuéntame de tu negocio. {MASCOT}"
        else:
            if 6 <= hour < 12:
                return f"{MASCOT} Good morning! I'm **Luna**. We help your business grow. 📍 **Directory** (34€/month) or 📢 **Campaign** (from 159€/month). Which interests you?"
            elif 12 <= hour < 18:
                return f"{MASCOT} Good afternoon! I'm **Luna**. 280+ businesses are already with us. Want to join?"
            else:
                return f"{MASCOT} Good evening! I'm **Luna**, your marketing assistant. Tell me about your business. {MASCOT}"

    def get_plans_comparison(self) -> str:
        """Comparación de planes."""
        if self.language == "es":
            return """
**COMPARA NUESTROS SERVICIOS**

┌─────────────────┬──────────────┬──────────────────┐
│                 │ DIRECTORIO   │ CAMPAÑA          │
├─────────────────┼──────────────┼──────────────────┤
│ 💵 Precio       │ 34€/mes      │ 159-299€/mes     │
│ ⏰ Mínimo       │ Flexible     │ 6 meses          │
│ 📍 Listado      │ ✅ Sí        │ ✅ Sí            │
│ 📢 Marketing    │ ❌ No        │ ✅ Sí            │
│ 👥 Soporte      │ ✅ Básico    │ ✅ Dedicado      │
│ 📊 Analytics    │ ✅ Sí        │ ✅ Completo      │
│ 🎯 Objetivo     │ Visibilidad  │ Clientes nuevos  │
└─────────────────┴──────────────┴──────────────────┘

📌 **Empieza pequeño con Directorio, crece con Campaña**
💡 **¿No sabes cuál elegir? Hablemos de tu negocio.**
"""
        else:
            return """
**COMPARE OUR SERVICES**

┌─────────────────┬──────────────┬──────────────────┐
│                 │ DIRECTORY    │ CAMPAIGN         │
├─────────────────┼──────────────┼──────────────────┤
│ 💵 Price        │ 34€/month    │ 159-299€/month   │
│ ⏰ Minimum      │ Flexible     │ 6 months         │
│ 📍 Listing      │ ✅ Yes       │ ✅ Yes           │
│ 📢 Marketing    │ ❌ No        │ ✅ Yes           │
│ 👥 Support      │ ✅ Basic     │ ✅ Dedicated     │
│ 📊 Analytics    │ ✅ Yes       │ ✅ Complete      │
│ 🎯 Goal         │ Visibility   │ New customers    │
└─────────────────┴──────────────┴──────────────────┘

📌 **Start small with Directory, grow with Campaign**
💡 **Unsure which to choose? Let's talk about your business.**
"""

    def respond_to_question(self, question: str, intent: str) -> str:
        """Responder pregunta según intención."""

        if intent == "directorio":
            return RESPONSES_DIRECTORIO[self.language]["completo"]

        elif intent == "campana":
            return RESPONSES_CAMPANA[self.language]["opciones"]

        elif intent == "descuento":
            return RESPONSES_CAMPANA[self.language]["minimo"]

        elif intent == "negociable":
            return RESPONSES_CAMPANA[self.language]["negociable"]

        else:
            # Buscar en FAQ
            for faq_key, faq_response in FAQ[self.language].items():
                if any(word in question.lower() for word in faq_key.split()):
                    return faq_response

            # Respuesta genérica
            if self.language == "es":
                return f"{MASCOT} No estoy seguro sobre eso. ¿Puedo ayudarte con **Directorio** (34€), **Campaña** (desde 159€) o tus dudas?"
            else:
                return f"{MASCOT} I'm not sure about that. Can I help you with **Directory** (34€), **Campaign** (from 159€) or your questions?"

    def get_testimonials(self) -> str:
        """Mostrar testimonios."""
        testimonios = TESTIMONIOS[self.language]

        response = "⭐ **CASOS DE ÉXITO**\n\n"
        for t in testimonios:
            response += f"**{t['empresa']}** ({t['sector']})\n"
            response += f"\"{t['testimonio']}\"\n"
            response += f"📈 {t['resultado']}\n\n"

        return response

    def create_inquiry(self, contact: str, plan_type: str, message: str = "") -> Dict:
        """Crear consulta/lead."""
        return {
            "timestamp": datetime.now().isoformat(),
            "contact": contact,
            "plan_type": plan_type,
            "language": self.language,
            "message": message,
            "status": "new"
        }

    def get_response(self, user_input: str) -> str:
        """Obtener respuesta del bot."""
        # Detectar idioma
        detected_lang = self.detect_language(user_input)
        if detected_lang != self.language:
            self.language = detected_lang

        # Detectar intención
        intent = self.detect_intent(user_input)

        # Responder según intención
        if intent == "saludo":
            return self.get_greeting()
        elif intent == "planes":
            return self.get_plans_comparison()
        else:
            return self.respond_to_question(user_input, intent)


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    print("🦉 Luna Bot - Test\n")

    # Test en español
    bot_es = AdvertisingSalesBot("es")
    print("ESPAÑOL:")
    print(bot_es.get_greeting())
    print("\n" + "="*50 + "\n")
    print(bot_es.get_plans_comparison())
    print("\n" + "="*50 + "\n")

    # Test en inglés
    bot_en = AdvertisingSalesBot("en")
    print("ENGLISH:")
    print(bot_en.get_greeting())
    print("\n" + "="*50 + "\n")
    print(bot_en.get_plans_comparison())
