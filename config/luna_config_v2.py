"""
Configuración de Luna - Bot de Publicidad (ACTUALIZADO)
Estructura: Directorio + Planes de Campaña con descuentos anuales

SERVICIOS:
1. DIRECTORIO: 34€/mes (para estar listado)
2. CAMPAÑAS: 159€/199€/299€/mes (mínimo 6 meses, 10% descuento anual, precios negociables)
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

# ============================================================================
# CONFIGURACIÓN DE MASCOTA
# ============================================================================

MASCOT_CONFIG = {
    "name": "Luna",
    "emoji": "🦉",
    "description": "Un simpático búho con grandes ojos curiosos",
    "color_primary": "#FF6B6B",
    "color_secondary": "#FB5607",
    "personality": "Amigable, curioso, motivador",
    "animation_speed": "normal"
}

# ============================================================================
# PLANES: DIRECTORIO
# ============================================================================

DIRECTORIO_PLANS = {
    "es": [
        {
            "id": "directorio_mensual",
            "nombre": "Directorio - Mensual",
            "emoji": "📍",
            "tipo": "directorio",
            "precio": 34,
            "moneda": "€",
            "periodo": "mes",
            "descripcion_corta": "Aparece en nuestro directorio",
            "beneficios": [
                "✅ Listing en directorio digital",
                "✅ Perfil completo (foto, descripción, contacto)",
                "✅ Categorías sin límite",
                "✅ Visible para 12,000+ usuarios/mes",
                "✅ Analytics de visitas y clics",
                "✅ Soporte por email",
                "✅ Actualización ilimitada de perfil"
            ],
            "ideal_para": "Todos los negocios",
            "cta": "Contratar directorio"
        },
        {
            "id": "directorio_anual",
            "nombre": "Directorio - Anual (10% Descuento)",
            "emoji": "🎁",
            "tipo": "directorio",
            "precio": 367.2,
            "precio_original": 408,
            "moneda": "€",
            "periodo": "año",
            "descripcion_corta": "Contrata por un año y ahorra",
            "beneficios": [
                "✅ TODO del plan mensual",
                "✅ 10% DESCUENTO (34€ x 12 = 408€ → 367€/año)",
                "✅ Visibilidad garantizada todo el año",
                "✅ 1 sesión de asesoramiento estratégico GRATIS",
                "✅ Soporte prioritario",
                "✅ Newsletter semanal exclusiva",
                "✅ Acceso a eventos de la revista"
            ],
            "ahorro_porcentaje": 10,
            "ideal_para": "Compromisos a largo plazo",
            "cta": "Contratar anualmente (10% OFF)"
        }
    ],
    "en": [
        {
            "id": "directorio_mensual",
            "nombre": "Directory - Monthly",
            "emoji": "📍",
            "tipo": "directorio",
            "precio": 34,
            "moneda": "€",
            "periodo": "month",
            "descripcion_corta": "Appear in our directory",
            "beneficios": [
                "✅ Digital directory listing",
                "✅ Complete profile (photo, description, contact)",
                "✅ Unlimited categories",
                "✅ Visible to 12,000+ users/month",
                "✅ Analytics of visits and clicks",
                "✅ Email support",
                "✅ Unlimited profile updates"
            ],
            "ideal_para": "All businesses",
            "cta": "Subscribe to directory"
        },
        {
            "id": "directorio_anual",
            "nombre": "Directory - Annual (10% Discount)",
            "emoji": "🎁",
            "tipo": "directorio",
            "precio": 367.2,
            "precio_original": 408,
            "moneda": "€",
            "periodo": "year",
            "descripcion_corta": "Annual subscription with savings",
            "beneficios": [
                "✅ EVERYTHING from monthly plan",
                "✅ 10% DISCOUNT (34€ x 12 = 408€ → 367€/year)",
                "✅ Guaranteed visibility all year",
                "✅ 1 FREE strategic consultation session",
                "✅ Priority support",
                "✅ Exclusive weekly newsletter",
                "✅ Access to magazine events"
            ],
            "ahorro_porcentaje": 10,
            "ideal_para": "Long-term commitments",
            "cta": "Subscribe annually (10% OFF)"
        }
    ]
}

# ============================================================================
# PLANES: CAMPAÑAS DE MARKETING
# ============================================================================

CAMPANA_PLANS = {
    "es": [
        {
            "id": "campana_basica",
            "nombre": "Campaña - Básica",
            "emoji": "📢",
            "tipo": "campana",
            "precio": 159,
            "moneda": "€",
            "periodo": "mes",
            "descripcion_corta": "Llega a más clientes",
            "minimo_meses": 6,
            "beneficios": [
                "✅ TODO del Directorio",
                "✅ Campaña de marketing dedicada",
                "✅ Estrategia para llegar nuevos clientes",
                "✅ Visibilidad aumentada",
                "✅ Newsletter promocional",
                "✅ Acompañamiento de la revista",
                "✅ Análisis y reportes",
                "✅ Mínimo 6 meses"
            ],
            "ideal_para": "Negocios que quieren crecer",
            "cta": "Solicitar Campaña Básica",
            "negociable": True,
            "popular": False
        },
        {
            "id": "campana_profesional",
            "nombre": "Campaña - Profesional",
            "emoji": "🎯",
            "tipo": "campana",
            "precio": 199,
            "moneda": "€",
            "periodo": "mes",
            "descripcion_corta": "Campaña optimizada",
            "minimo_meses": 6,
            "beneficios": [
                "✅ TODO de Campaña Básica",
                "✅ Estrategia avanzada de marketing",
                "✅ Múltiples canales de difusión",
                "✅ Soporte dedicado",
                "✅ Optimización continua",
                "✅ Reportes detallados",
                "✅ Mejor ROI",
                "✅ Mínimo 6 meses"
            ],
            "ideal_para": "Negocios establecidos",
            "cta": "Solicitar Campaña Profesional",
            "negociable": True,
            "popular": True
        },
        {
            "id": "campana_premium",
            "nombre": "Campaña - Premium",
            "emoji": "👑",
            "tipo": "campana",
            "precio": 299,
            "moneda": "€",
            "periodo": "mes",
            "descripcion_corta": "Máximo impacto",
            "minimo_meses": 6,
            "beneficios": [
                "✅ TODO de Campaña Profesional",
                "✅ Campañas personalizadas complejas",
                "✅ Equipo dedicado",
                "✅ Consultoría estratégica",
                "✅ Premium placement",
                "✅ Soporte 24/7",
                "✅ Garantía de resultados",
                "✅ Mínimo 6 meses"
            ],
            "ideal_para": "Empresas grandes",
            "cta": "Solicitar Campaña Premium",
            "negociable": True,
            "popular": False
        }
    ],
    "en": [
        {
            "id": "campana_basica",
            "nombre": "Campaign - Basic",
            "emoji": "📢",
            "tipo": "campana",
            "precio": 159,
            "moneda": "€",
            "periodo": "month",
            "descripcion_corta": "Reach more customers",
            "minimo_meses": 6,
            "beneficios": [
                "✅ EVERYTHING from Directory",
                "✅ Dedicated marketing campaign",
                "✅ Strategy to reach new customers",
                "✅ Increased visibility",
                "✅ Promotional newsletter",
                "✅ Magazine support",
                "✅ Analysis and reports",
                "✅ Minimum 6 months"
            ],
            "ideal_para": "Businesses wanting to grow",
            "cta": "Request Basic Campaign",
            "negociable": True,
            "popular": False
        },
        {
            "id": "campana_profesional",
            "nombre": "Campaign - Professional",
            "emoji": "🎯",
            "tipo": "campana",
            "precio": 199,
            "moneda": "€",
            "periodo": "month",
            "descripcion_corta": "Optimized campaign",
            "minimo_meses": 6,
            "beneficios": [
                "✅ EVERYTHING from Basic Campaign",
                "✅ Advanced marketing strategy",
                "✅ Multiple distribution channels",
                "✅ Dedicated support",
                "✅ Continuous optimization",
                "✅ Detailed reports",
                "✅ Better ROI",
                "✅ Minimum 6 months"
            ],
            "ideal_para": "Established businesses",
            "cta": "Request Professional Campaign",
            "negociable": True,
            "popular": True
        },
        {
            "id": "campana_premium",
            "nombre": "Campaign - Premium",
            "emoji": "👑",
            "tipo": "campana",
            "precio": 299,
            "moneda": "€",
            "periodo": "month",
            "descripcion_corta": "Maximum impact",
            "minimo_meses": 6,
            "beneficios": [
                "✅ EVERYTHING from Professional Campaign",
                "✅ Complex personalized campaigns",
                "✅ Dedicated team",
                "✅ Strategic consulting",
                "✅ Premium placement",
                "✅ 24/7 support",
                "✅ Results guarantee",
                "✅ Minimum 6 months"
            ],
            "ideal_para": "Large companies",
            "cta": "Request Premium Campaign",
            "negociable": True,
            "popular": False
        }
    ]
}

# ============================================================================
# DESCUENTOS ANUALES
# ============================================================================

DESCUENTOS_ANUALES = {
    "es": {
        "campana_basica": {
            "precio_mensual": 159,
            "precio_6_meses": 159 * 6,
            "precio_anual": 159 * 12 * 0.9,  # 10% descuento
            "ahorro_anual": 159 * 12 * 0.1,
            "descripcion": "10% descuento pagando 12 meses"
        },
        "campana_profesional": {
            "precio_mensual": 199,
            "precio_6_meses": 199 * 6,
            "precio_anual": 199 * 12 * 0.9,  # 10% descuento
            "ahorro_anual": 199 * 12 * 0.1,
            "descripcion": "10% descuento pagando 12 meses"
        },
        "campana_premium": {
            "precio_mensual": 299,
            "precio_6_meses": 299 * 6,
            "precio_anual": 299 * 12 * 0.9,  # 10% descuento
            "ahorro_anual": 299 * 12 * 0.1,
            "descripcion": "10% descuento pagando 12 meses"
        }
    },
    "en": {
        "campana_basica": {
            "precio_mensual": 159,
            "precio_6_meses": 159 * 6,
            "precio_anual": 159 * 12 * 0.9,
            "ahorro_anual": 159 * 12 * 0.1,
            "descripcion": "10% discount for annual payment"
        },
        "campana_profesional": {
            "precio_mensual": 199,
            "precio_6_meses": 199 * 6,
            "precio_anual": 199 * 12 * 0.9,
            "ahorro_anual": 199 * 12 * 0.1,
            "descripcion": "10% discount for annual payment"
        },
        "campana_premium": {
            "precio_mensual": 299,
            "precio_6_meses": 299 * 6,
            "precio_anual": 299 * 12 * 0.9,
            "ahorro_anual": 299 * 12 * 0.1,
            "descripcion": "10% discount for annual payment"
        }
    }
}

# ============================================================================
# MENSAJES DINÁMICOS
# ============================================================================

DYNAMIC_MESSAGES = {
    "es": {
        "greeting": {
            "morning": "¡Hola! 👋 ¿Quieres que tu negocio aparezca en nuestro directorio? Solo 34€/mes.",
            "afternoon": "¡Hey! 🌟 Negocios como el tuyo ya están en nuestro directorio. ¿Te unes?",
            "evening": "¡Buenas noches! 🌙 Aparece en nuestro directorio desde 34€/mes."
        },
        "proactive_questions": [
            "💼 ¿Buscas aumentar visibilidad? Únete a 280+ negocios en nuestro directorio.",
            "📢 ¿Quieres hacer una campaña de marketing? Tenemos planes de 159€, 199€ y 299€/mes.",
            "🚀 ¿Buscas llegar a nuevos clientes? Nuestras campañas te ayudan.",
            "🎁 Contratando por un año: 10% descuento = Ahorras mucho dinero",
        ],
        "sales": {
            "directorio": "Directorio: 34€/mes - Aparece ante 12,000+ usuarios mensuales",
            "campana": "Campañas: Desde 159€/mes - Estrategia personalizada para nuevos clientes",
            "anual": "Anual: 10% descuento en todo - Contrata 12 meses y ahorra"
        }
    },
    "en": {
        "greeting": {
            "morning": "Hello! 👋 Want your business in our directory? Just 34€/month.",
            "afternoon": "Hey! 🌟 Businesses like yours are already in our directory. Join us?",
            "evening": "Good evening! 🌙 Appear in our directory from 34€/month."
        },
        "proactive_questions": [
            "💼 Looking to increase visibility? Join 280+ businesses in our directory.",
            "📢 Want to run a marketing campaign? We have plans from 159€, 199€ and 299€/month.",
            "🚀 Looking to reach new customers? Our campaigns help you.",
            "🎁 Annual subscription: 10% discount = Save big money",
        ],
        "sales": {
            "directorio": "Directory: 34€/month - Appear to 12,000+ monthly users",
            "campana": "Campaigns: From 159€/month - Personalized strategy for new customers",
            "anual": "Annual: 10% discount on everything - Subscribe 12 months and save"
        }
    }
}

# ============================================================================
# UTILIDADES
# ============================================================================

def get_directorio_plans(language: str = "es") -> List[Dict]:
    """Obtener planes de directorio."""
    return DIRECTORIO_PLANS.get(language, DIRECTORIO_PLANS["es"])

def get_campana_plans(language: str = "es") -> List[Dict]:
    """Obtener planes de campaña."""
    return CAMPANA_PLANS.get(language, CAMPANA_PLANS["es"])

def get_all_plans(language: str = "es") -> Dict:
    """Obtener todos los planes (directorio + campañas)."""
    return {
        "directorio": get_directorio_plans(language),
        "campanas": get_campana_plans(language)
    }

def get_annual_discount(plan_id: str, language: str = "es") -> Optional[Dict]:
    """Obtener información de descuento anual."""
    discounts = DESCUENTOS_ANUALES.get(language, DESCUENTOS_ANUALES["es"])
    return discounts.get(plan_id)

def calculate_annual_price(plan_id: str, monthly_price: float) -> float:
    """Calcular precio anual con 10% descuento."""
    return monthly_price * 12 * 0.9

def format_price(price: float, currency: str = "€") -> str:
    """Formatear precio."""
    return f"{price:,.2f}{currency}".replace(",", ".")

# ============================================================================
# EXPORTAR
# ============================================================================

if __name__ == "__main__":
    print("🦉 Luna Bot - Configuración de Precios")
    print("=" * 50)

    print("\n📍 PLANES DE DIRECTORIO:")
    for plan in get_directorio_plans("es"):
        print(f"  {plan['emoji']} {plan['nombre']}: {plan['precio']}€/{plan['periodo']}")

    print("\n📢 PLANES DE CAMPAÑA:")
    for plan in get_campana_plans("es"):
        print(f"  {plan['emoji']} {plan['nombre']}: {plan['precio']}€/{plan['periodo']} (mín. {plan['minimo_meses']}m)")

    print("\n💰 DESCUENTOS ANUALES:")
    for plan_id, discount in DESCUENTOS_ANUALES["es"].items():
        print(f"  {plan_id}: {discount['precio_anual']:,.0f}€/año (ahorras {discount['ahorro_anual']:,.0f}€)")
