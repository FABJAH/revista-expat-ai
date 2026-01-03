"""
Bot de Inmigración para Extranjeros que Buscan Vivir en España
Proporciona información sobre visados, NIE, documentación y primeros pasos
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

EMOJI = "🌍"
BOT_NAME = "Immigration Assistant"
LEGAL_RECOMMENDATIONS = {
    "es": [
        "🔹 Klev&Vera International Law Firm (info@klevvera.com) — abogados de extranjería, anuncio en la revista",
        "🔹 Si necesitas otra firma anunciante, podemos conectarte directamente desde la revista"
    ],
    "en": [
        "🔹 Klev&Vera International Law Firm (info@klevvera.com) — immigration lawyers, advertiser in the magazine",
        "🔹 If you need another advertiser firm, we can connect you directly from the magazine"
    ]
}

# Información por país de origen (EXPANDIDA: USA, UK, Europa y más)
VISA_INFO_BY_COUNTRY = {
    "es": {
        "Argentina": {
            "visado": "No requerido (UE-MERCOSUR)",
            "duracion": "90 días (luego solicitar residencia)",
            "nie": "Sí, después de 90 días",
            "documentacion": ["Pasaporte válido", "Demostrar solvencia económica", "Seguro de salud"],
            "tiempo_tramite": "30-60 días",
            "costo_estimado": "100-300€"
        },
        "Colombia": {
            "visado": "Requerido (visa de turista o residencia)",
            "duracion": "90 días (visa de turista)",
            "nie": "Sí, una vez en España",
            "documentacion": ["Pasaporte válido", "Reserva de alojamiento", "Demostrar fondos (800€/mes)"],
            "tiempo_tramite": "15-30 días",
            "costo_estimado": "80-150€"
        },
        "México": {
            "visado": "No requerido (180 días como turista)",
            "duracion": "180 días",
            "nie": "Sí, después de establecer residencia",
            "documentacion": ["Pasaporte válido", "Billete de vuelta", "Comprobante de fondos"],
            "tiempo_tramite": "Automático al entrar",
            "costo_estimado": "0€ (visado de turista)"
        },
        "Brasil": {
            "visado": "Requerido",
            "duracion": "90 días",
            "nie": "Sí",
            "documentacion": ["Pasaporte válido (6 meses mínimo)", "Comprobante económico", "Certificado de antecedentes"],
            "tiempo_tramite": "10-15 días",
            "costo_estimado": "90-120€"
        },
        "USA": {
            "visado": "No requerido (90 días Schengen) ⚠️ ETIAS 80€ a partir 2025",
            "duracion": "90 días",
            "nie": "Sí, para residencia permanente",
            "documentacion": ["Pasaporte válido (6 meses)", "Billete de vuelta", "Comprobante solvencia (1000€+)"],
            "tiempo_tramite": "Automático + ETIAS online",
            "costo_estimado": "0€ entrada + 80€ ETIAS"
        },
        "Reino Unido": {
            "visado": "No requerido (post-Brexit) - 6 meses",
            "duracion": "180 días",
            "nie": "Sí si permanencia > 6 meses",
            "documentacion": ["Pasaporte británico válido", "Billete de vuelta", "Fondos (1500€+)"],
            "tiempo_tramite": "Automático",
            "costo_estimado": "0€"
        },
        "Alemania": {
            "visado": "No requerido (UE/EEE)",
            "duracion": "Ilimitado",
            "nie": "Sí al residir permanentemente",
            "documentacion": ["DNI/Pasaporte UE", "Fondos mensuales (800€+)", "Contrato alquiler"],
            "tiempo_tramite": "Inmediato",
            "costo_estimado": "0€"
        },
        "Francia": {
            "visado": "No requerido (UE/EEE)",
            "duracion": "Ilimitado",
            "nie": "Sí al residir permanentemente",
            "documentacion": ["DNI/Pasaporte UE", "Fondos mensuales (800€+)", "Contrato alquiler"],
            "tiempo_tramite": "Inmediato",
            "costo_estimado": "0€"
        },
        "Italia": {
            "visado": "No requerido (UE/EEE)",
            "duracion": "Ilimitado",
            "nie": "Sí al residir permanentemente",
            "documentacion": ["DNI/Pasaporte UE", "Fondos mensuales (800€+)", "Contrato alquiler"],
            "tiempo_tramite": "Inmediato",
            "costo_estimado": "0€"
        },
        "Países Bajos": {
            "visado": "No requerido (UE/EEE)",
            "duracion": "Ilimitado",
            "nie": "Sí al residir permanentemente",
            "documentacion": ["DNI/Pasaporte UE", "Fondos mensuales (900€+)", "Contrato alquiler"],
            "tiempo_tramite": "Inmediato",
            "costo_estimado": "0€"
        },
        "Portugal": {
            "visado": "No requerido (UE/EEE)",
            "duracion": "Ilimitado",
            "nie": "Sí al residir permanentemente",
            "documentacion": ["DNI/Pasaporte UE", "Fondos mensuales (700€+)", "Contrato alquiler"],
            "tiempo_tramite": "Inmediato",
            "costo_estimado": "0€"
        },
        "Suiza": {
            "visado": "No requerido (Schengen)",
            "duracion": "90 días",
            "nie": "Sí para residencia permanente",
            "documentacion": ["Pasaporte válido", "Billete de vuelta", "Fondos", "Contrato trabajo/alquiler"],
            "tiempo_tramite": "Automático",
            "costo_estimado": "0€"
        },
        "Noruega": {
            "visado": "No requerido (Schengen/EEE)",
            "duracion": "90 días",
            "nie": "Sí para residencia permanente",
            "documentacion": ["Pasaporte válido", "Billete de vuelta", "Fondos"],
            "tiempo_tramite": "Automático",
            "costo_estimado": "0€"
        },
        "Irlanda": {
            "visado": "No requerido (Common Travel Area)",
            "duracion": "6 meses",
            "nie": "Sí si permanencia > 6 meses",
            "documentacion": ["Pasaporte válido", "Fondos (1200€+)", "Billete de vuelta"],
            "tiempo_tramite": "Automático",
            "costo_estimado": "0€"
        },
        "Canadá": {
            "visado": "No requerido (90 días) - eVisitor 7€",
            "duracion": "90 días",
            "nie": "Sí para residencia",
            "documentacion": ["Pasaporte válido", "eVisitor (trámite online)", "Fondos (1200€+)"],
            "tiempo_tramite": "Online 24-72 horas",
            "costo_estimado": "7€ (eVisitor)"
        },
        "Australia": {
            "visado": "Requerido (eVisitor 20 AUD)",
            "duracion": "90 días",
            "nie": "Sí si trabajas",
            "documentacion": ["Pasaporte válido (6 meses)", "Fondos (1500€+)", "Seguro obligatorio"],
            "tiempo_tramite": "Online 1-2 días",
            "costo_estimado": "20 AUD (≈13€)"
        },
        "Nueva Zelanda": {
            "visado": "Requerido (eVisitor 9 NZD)",
            "duracion": "90 días",
            "nie": "Sí si trabajas",
            "documentacion": ["Pasaporte válido (6 meses)", "Fondos (1300€+)", "Billete de vuelta"],
            "tiempo_tramite": "Online 1-2 días",
            "costo_estimado": "9 NZD (≈5€)"
        },
        "China": {
            "visado": "Requerido",
            "duracion": "90 días",
            "nie": "Sí",
            "documentacion": ["Pasaporte", "Invitación o reserva hotel", "Comprobante económico", "Carta de empleo"],
            "tiempo_tramite": "15-20 días",
            "costo_estimado": "100-150€"
        },
        "India": {
            "visado": "Requerido",
            "duracion": "90 días",
            "nie": "Sí",
            "documentacion": ["Pasaporte (6 meses)", "Prueba de fondos", "Reserva hotel", "Certificado antecedentes"],
            "tiempo_tramite": "15-25 días",
            "costo_estimado": "80-120€"
        },
        "Otro": {
            "visado": "Consultar en embajada española de tu país",
            "duracion": "Varía según país",
            "nie": "Sí, una vez en España",
            "documentacion": ["Pasaporte válido", "Documentación específica por país", "Comprobante de fondos"],
            "tiempo_tramite": "15-60 días",
            "costo_estimado": "50-300€"
        }
    },
    "en": {
        "Argentina": {
            "visado": "Not required (EU-MERCOSUR)",
            "duracion": "90 days (then request residency)",
            "nie": "Yes, after 90 days",
            "documentacion": ["Valid passport", "Proof of economic solvency", "Health insurance"],
            "tiempo_tramite": "30-60 days",
            "costo_estimado": "100-300€"
        },
        "Colombia": {
            "visado": "Required (tourist or residence visa)",
            "duracion": "90 days (tourist visa)",
            "nie": "Yes, once in Spain",
            "documentacion": ["Valid passport", "Accommodation booking", "Proof of funds (800€/month)"],
            "tiempo_tramite": "15-30 days",
            "costo_estimado": "80-150€"
        },
        "Mexico": {
            "visado": "Not required (180 days as tourist)",
            "duracion": "180 days",
            "nie": "Yes, after establishing residency",
            "documentacion": ["Valid passport", "Return ticket", "Proof of funds"],
            "tiempo_tramite": "Automatic upon entry",
            "costo_estimado": "0€ (tourist visa)"
        },
        "Brazil": {
            "visado": "Required",
            "duracion": "90 days",
            "nie": "Yes",
            "documentacion": ["Valid passport (6 months min)", "Economic proof", "Background certificate"],
            "tiempo_tramite": "10-15 days",
            "costo_estimado": "90-120€"
        },
        "USA": {
            "visado": "Not required (90 days Schengen) ⚠️ ETIAS €80 from 2025",
            "duracion": "90 days",
            "nie": "Yes, for permanent residency",
            "documentacion": ["Valid passport (6 months)", "Return ticket", "Proof of funds (1000€+)"],
            "tiempo_tramite": "Automatic + ETIAS online",
            "costo_estimado": "€0 entry + €80 ETIAS"
        },
        "United Kingdom": {
            "visado": "Not required (post-Brexit) - 6 months",
            "duracion": "180 days",
            "nie": "Yes if stay > 6 months",
            "documentacion": ["Valid British passport", "Return ticket", "Funds (1500€+)"],
            "tiempo_tramite": "Automatic",
            "costo_estimado": "€0"
        },
        "Germany": {
            "visado": "Not required (EU/EEA)",
            "duracion": "Unlimited",
            "nie": "Yes when residing permanently",
            "documentacion": ["EU ID/Passport", "Monthly funds (800€+)", "Lease contract"],
            "tiempo_tramite": "Immediate",
            "costo_estimado": "€0"
        },
        "France": {
            "visado": "Not required (EU/EEA)",
            "duracion": "Unlimited",
            "nie": "Yes when residing permanently",
            "documentacion": ["EU ID/Passport", "Monthly funds (800€+)", "Lease contract"],
            "tiempo_tramite": "Immediate",
            "costo_estimado": "€0"
        },
        "Italy": {
            "visado": "Not required (EU/EEA)",
            "duracion": "Unlimited",
            "nie": "Yes when residing permanently",
            "documentacion": ["EU ID/Passport", "Monthly funds (800€+)", "Lease contract"],
            "tiempo_tramite": "Immediate",
            "costo_estimado": "€0"
        },
        "Netherlands": {
            "visado": "Not required (EU/EEA)",
            "duracion": "Unlimited",
            "nie": "Yes when residing permanently",
            "documentacion": ["EU ID/Passport", "Monthly funds (900€+)", "Lease contract"],
            "tiempo_tramite": "Immediate",
            "costo_estimado": "€0"
        },
        "Portugal": {
            "visado": "Not required (EU/EEA)",
            "duracion": "Unlimited",
            "nie": "Yes when residing permanently",
            "documentacion": ["EU ID/Passport", "Monthly funds (700€+)", "Lease contract"],
            "tiempo_tramite": "Immediate",
            "costo_estimado": "€0"
        },
        "Switzerland": {
            "visado": "Not required (Schengen)",
            "duracion": "90 days",
            "nie": "Yes for permanent residency",
            "documentacion": ["Valid passport", "Return ticket", "Funds", "Employment/lease contract"],
            "tiempo_tramite": "Automatic",
            "costo_estimado": "€0"
        },
        "Norway": {
            "visado": "Not required (Schengen/EEA)",
            "duracion": "90 days",
            "nie": "Yes for permanent residency",
            "documentacion": ["Valid passport", "Return ticket", "Funds"],
            "tiempo_tramite": "Automatic",
            "costo_estimado": "€0"
        },
        "Ireland": {
            "visado": "Not required (Common Travel Area)",
            "duracion": "6 months",
            "nie": "Yes if stay > 6 months",
            "documentacion": ["Valid passport", "Funds (1200€+)", "Return ticket"],
            "tiempo_tramite": "Automatic",
            "costo_estimado": "€0"
        },
        "Canada": {
            "visado": "Not required (90 days) - eVisitor €7",
            "duracion": "90 days",
            "nie": "Yes for residency",
            "documentacion": ["Valid passport", "eVisitor (online)", "Funds (1200€+)"],
            "tiempo_tramite": "Online 24-72 hours",
            "costo_estimado": "€7 (eVisitor)"
        },
        "Australia": {
            "visado": "Required (eVisitor 20 AUD)",
            "duracion": "90 days",
            "nie": "Yes if working",
            "documentacion": ["Valid passport (6 months)", "Funds (1500€+)", "Mandatory insurance"],
            "tiempo_tramite": "Online 1-2 days",
            "costo_estimado": "20 AUD (≈€13)"
        },
        "New Zealand": {
            "visado": "Required (eVisitor 9 NZD)",
            "duracion": "90 days",
            "nie": "Yes if working",
            "documentacion": ["Valid passport (6 months)", "Funds (1300€+)", "Return ticket"],
            "tiempo_tramite": "Online 1-2 days",
            "costo_estimado": "9 NZD (≈€5)"
        },
        "China": {
            "visado": "Required",
            "duracion": "90 days",
            "nie": "Yes",
            "documentacion": ["Passport", "Invitation or hotel booking", "Economic proof", "Employment letter"],
            "tiempo_tramite": "15-20 days",
            "costo_estimado": "100-150€"
        },
        "India": {
            "visado": "Required",
            "duracion": "90 days",
            "nie": "Yes",
            "documentacion": ["Passport (6 months)", "Proof of funds", "Hotel booking", "Background certificate"],
            "tiempo_tramite": "15-25 days",
            "costo_estimado": "80-120€"
        },
        "Other": {
            "visado": "Check with Spanish embassy in your country",
            "duracion": "Varies by country",
            "nie": "Yes, once in Spain",
            "documentacion": ["Valid passport", "Country-specific documentation", "Proof of funds"],
            "tiempo_tramite": "15-60 days",
            "costo_estimado": "50-300€"
        }
    }
}

# Checklist de primeros pasos
FIRST_STEPS_CHECKLIST = {
    "es": [
        "✈️ Preparar documentación (pasaporte, visado si aplica)",
        "🏠 Buscar alojamiento y hacer reserva",
        "💼 Demostrar solvencia económica (extracto bancario)",
        "📋 Obtener seguro de salud (si lo requiere tu visa)",
        "🛬 Llegar a España y registrarse en el ayuntamiento (empadronamiento)",
        "🆔 Solicitar NIE en la policía nacional",
        "🏥 Registrarse en centro de salud local",
        "📱 Abrir cuenta bancaria española",
        "🔑 Contratación de servicios (teléfono, internet, servicios)",
        "💡 Familiarizarse con sistema fiscal español"
    ],
    "en": [
        "✈️ Prepare documentation (passport, visa if applicable)",
        "🏠 Find accommodation and make reservation",
        "💼 Prove economic solvency (bank statement)",
        "📋 Obtain health insurance (if required by your visa)",
        "🛬 Arrive in Spain and register at town hall (empadronamiento)",
        "🆔 Apply for NIE at national police",
        "🏥 Register at local health center",
        "📱 Open Spanish bank account",
        "🔑 Contract services (phone, internet, utilities)",
        "💡 Familiarize yourself with Spanish tax system"
    ]
}

# Información sobre NIE
NIE_INFO = {
    "es": {
        "que_es": "Número de Identidad de Extranjero - Número único que te identifica ante administración española",
        "donde_solicitar": "Policía Nacional (Comisaría o cita previa)",
        "documentos_necesarios": [
            "Pasaporte original",
            "Formulario EX-15 (solicitud NIE)",
            "Comprobante de empadronamiento",
            "Comprobante de motivo (contrato trabajo, estudiante, etc.)"
        ],
        "tiempo": "5-10 días hábiles",
        "costo": "0€",
        "cita_previa": "Recomendado hacer cita previa en: https://www.cita-previa-ext.es"
    },
    "en": {
        "que_es": "Foreigner Identification Number - Unique ID for Spanish administration",
        "donde_solicitar": "National Police (Station or prior appointment)",
        "documentos_necesarios": [
            "Original passport",
            "Form EX-15 (NIE request)",
            "Proof of registration at town hall",
            "Proof of reason (employment contract, student, etc.)"
        ],
        "tiempo": "5-10 business days",
        "costo": "0€",
        "cita_previa": "Recommended to book appointment: https://www.cita-previa-ext.es"
    }
}

# Información sobre Empadronamiento
EMPADRONAMIENTO_INFO = {
    "es": {
        "que_es": "Registro oficial de residencia en un domicilio español",
        "donde": "Ayuntamiento de tu distrito o ciudad",
        "documentos": ["Pasaporte", "Contrato de alquiler o escritura propiedad", "Permiso del propietario"],
        "tiempo": "1 día (trámite rápido)",
        "costo": "0€",
        "importancia": "Requisito previo para NIE, acceso a sanidad, etc."
    },
    "en": {
        "que_es": "Official record of residence at a Spanish address",
        "donde": "Town hall of your district or city",
        "documentos": ["Passport", "Rental contract or property deed", "Property owner permission"],
        "tiempo": "1 day (quick process)",
        "costo": "0€",
        "importancia": "Required for NIE, health access, etc."
    }
}

# ============================================================================
# CLASE BOT
# ============================================================================

class ImmigrationBot:
    """Bot especializado en información de inmigración y primeros pasos."""

    # OPTIMIZACIÓN: Caché de clase para evitar recargar JSON en cada instancia
    _legal_ads_cache = None
    _cache_loaded = False

    def __init__(self, language: str = "es"):
        self.language = language.lower()
        if self.language not in ["es", "en"]:
            self.language = "es"
        self.legal_ads = self._load_legal_ads()

    def _legal_note(self) -> str:
        if self.legal_ads:
            if self.language == "es":
                header = "\n🤝 Recomendamos consultar con un profesional en leyes de extranjería. Prioridad a firmas anunciantes:"  # noqa: E501
                lines = [
                    f"🔹 {ad.get('nombre', 'Firma legal')} ({ad.get('contacto', ad.get('url', ''))}) — anuncio en la revista"
                    for ad in self.legal_ads
                ]
            else:
                header = "\n🤝 We recommend speaking with an immigration lawyer. Priority to advertiser firms:"  # noqa: E501
                lines = [
                    f"🔹 {ad.get('nombre', 'Law firm')} ({ad.get('contacto', ad.get('url', ''))}) — advertiser in the magazine"
                    for ad in self.legal_ads
                ]
            return header + "\n" + "\n".join(lines)

        # Fallback estático
        lines = LEGAL_RECOMMENDATIONS[self.language]
        if self.language == "es":
            header = "\n🤝 Recomendamos consultar con un profesional en leyes de extranjería. Prioridad a firmas anunciantes:"  # noqa: E501
        else:
            header = "\n🤝 We recommend speaking with an immigration lawyer. Priority to advertiser firms:"  # noqa: E501
        return header + "\n" + "\n".join(lines)

    def _load_legal_ads(self) -> List[Dict]:
        # OPTIMIZACIÓN: Usa caché de clase para evitar leer JSON en cada instancia (mejora 10-50ms)
        if ImmigrationBot._cache_loaded:
            return ImmigrationBot._legal_ads_cache or []

        data_path = Path(__file__).resolve().parent.parent / "data" / "anunciantes.json"
        try:
            with data_path.open(encoding="utf-8") as f:
                data = json.load(f)
            legal_list = [
                item for item in data.get("Legal and Financial", [])
                if item.get("es_anunciante")
            ]
            if not legal_list:
                legal_list = data.get("Legal and Financial", [])[:2]

            # Guardar en caché
            ImmigrationBot._legal_ads_cache = legal_list[:3]
            ImmigrationBot._cache_loaded = True
            return ImmigrationBot._legal_ads_cache
        except Exception:
            ImmigrationBot._cache_loaded = True  # Evitar reintentos
            ImmigrationBot._legal_ads_cache = []
            return []

    def get_greeting(self) -> str:
        """Saludo inicial."""
        if self.language == "es":
            return f"{EMOJI} ¡Hola! Soy tu asistente de inmigración. Te ayudaré con información sobre visados, NIE, documentación y primeros pasos para vivir en España. ¿De qué país vienes?"
        else:
            return f"{EMOJI} Hello! I'm your immigration assistant. I'll help you with information about visas, NIE, documentation and first steps to live in Spain. What country are you from?"

    def get_visa_info(self, country: str) -> Dict:
        """Obtener información de visado por país."""
        visa_data = VISA_INFO_BY_COUNTRY[self.language]

        # Buscar país (con aproximación)
        country_lower = country.lower()
        for key in visa_data.keys():
            if key.lower() in country_lower or country_lower in key.lower():
                info = visa_data[key]
                if self.language == "es":
                    response = f"📋 **Información de Visado para {key}**\n\n"
                    response += f"🎫 **Visado:** {info['visado']}\n"
                    response += f"⏱️ **Duración:** {info['duracion']}\n"
                    response += f"🆔 **NIE:** {info['nie']}\n"
                    response += f"📄 **Documentación:** {', '.join(info['documentacion'])}\n"
                    response += f"⏳ **Tiempo de trámite:** {info['tiempo_tramite']}\n"
                    response += f"💰 **Costo estimado:** {info['costo_estimado']}\n\n"
                    response += "¿Necesitas información sobre NIE, empadronamiento o primeros pasos?"
                    response += self._legal_note()
                else:
                    response = f"📋 **Visa Information for {key}**\n\n"
                    response += f"🎫 **Visa:** {info['visado']}\n"
                    response += f"⏱️ **Duration:** {info['duracion']}\n"
                    response += f"🆔 **NIE:** {info['nie']}\n"
                    response += f"📄 **Documentation:** {', '.join(info['documentacion'])}\n"
                    response += f"⏳ **Processing time:** {info['tiempo_tramite']}\n"
                    response += f"💰 **Estimated cost:** {info['costo_estimado']}\n\n"
                    response += "Need information about NIE, registration or first steps?"
                    response += self._legal_note()

                return {
                    "type": "visa_info",
                    "message": response,
                    "country": key,
                    "data": info
                }

        # Si no encuentra el país
        if self.language == "es":
            return {
                "type": "visa_info",
                "message": f"No tengo información específica de {country}. Por favor, consulta la embajada española de tu país o selecciona otro país de la lista." + self._legal_note(),
                "data": None
            }
        else:
            return {
                "type": "visa_info",
                "message": f"I don't have specific information for {country}. Please check the Spanish embassy in your country or select another country." + self._legal_note(),
                "data": None
            }

    def get_first_steps(self) -> str:
        """Obtener checklist de primeros pasos."""
        checklist = FIRST_STEPS_CHECKLIST[self.language]

        if self.language == "es":
            response = "📋 **Checklist: 10 Primeros Pasos**\n\n"
        else:
            response = "📋 **Checklist: First 10 Steps**\n\n"

        for i, step in enumerate(checklist, 1):
            response += f"{i}. {step}\n"
        response += self._legal_note()
        return response

    def get_nie_info(self) -> str:
        """Obtener información sobre NIE."""
        info = NIE_INFO[self.language]

        if self.language == "es":
            response = "🆔 **Información sobre el NIE (Número de Identidad de Extranjero)**\n\n"
            response += f"**¿Qué es?** {info['que_es']}\n\n"
            response += f"**¿Dónde solicitarlo?** {info['donde_solicitar']}\n\n"
            response += f"**Documentos necesarios:**\n"
            for doc in info['documentos_necesarios']:
                response += f"  • {doc}\n"
            response += f"\n**⏳ Tiempo:** {info['tiempo']}\n"
            response += f"**💰 Costo:** {info['costo']}\n\n"
            response += f"**Cita previa:** {info['cita_previa']}"
            response += self._legal_note()
        else:
            response = "🆔 **Information about NIE (Foreigner Identification Number)**\n\n"
            response += f"**What is it?** {info['que_es']}\n\n"
            response += f"**Where to apply?** {info['donde_solicitar']}\n\n"
            response += f"**Required documents:**\n"
            for doc in info['documentos_necesarios']:
                response += f"  • {doc}\n"
            response += f"\n**⏳ Time:** {info['tiempo']}\n"
            response += f"**💰 Cost:** {info['costo']}\n\n"
            response += f"**Prior appointment:** {info['cita_previa']}"
            response += self._legal_note()

        return response

    def get_empadronamiento_info(self) -> str:
        """Obtener información sobre empadronamiento."""
        info = EMPADRONAMIENTO_INFO[self.language]

        if self.language == "es":
            response = "🏠 **Información sobre Empadronamiento (Registro de Residencia)**\n\n"
            response += f"**¿Qué es?** {info['que_es']}\n\n"
            response += f"**¿Dónde?** {info['donde']}\n\n"
            response += f"**Documentos:** {', '.join(info['documentos'])}\n\n"
            response += f"**⏳ Tiempo:** {info['tiempo']}\n"
            response += f"**💰 Costo:** {info['costo']}\n"
            response += f"**❗ Importancia:** {info['importancia']}"
            response += self._legal_note()
        else:
            response = "🏠 **Information about Registration (Empadronamiento)**\n\n"
            response += f"**What is it?** {info['que_es']}\n\n"
            response += f"**Where?** {info['donde']}\n\n"
            response += f"**Documents:** {', '.join(info['documentos'])}\n\n"
            response += f"**⏳ Time:** {info['tiempo']}\n"
            response += f"**💰 Cost:** {info['costo']}\n"
            response += f"**❗ Importance:** {info['importancia']}"
            response += self._legal_note()

        return response

    def get_response(self, user_input: str) -> str:
        """Obtener respuesta según entrada del usuario."""
        user_lower = user_input.lower()

        # Detectar intención
        if any(word in user_lower for word in ['primero', 'paso', 'checklist', 'pasos', 'first', 'steps']):
            return self.get_first_steps()
        elif any(word in user_lower for word in ['nie', 'identidad', 'número']):
            return self.get_nie_info()
        elif any(word in user_lower for word in ['empadron', 'registro', 'registro residencia']):
            return self.get_empadronamiento_info()
        elif any(word in user_lower for word in ['visado', 'visa', 'requirement', 'documento']):
            # Extraer país si existe
            for country in VISA_INFO_BY_COUNTRY[self.language].keys():
                if country.lower() in user_lower:
                    info = self.get_visa_info(country)
                    return info['message']
            # Si no especifica país, pregunta
            if self.language == "es":
                return "¿De qué país vienes? Dime tu país para mostrarte los requisitos específicos de visado." + self._legal_note()
            else:
                return "What country are you from? Tell me your country to show you specific visa requirements." + self._legal_note()
        else:
            # Respuesta por defecto
            if self.language == "es":
                return f"Puedo ayudarte con:\n• 📋 Primeros pasos\n• 🎫 Información de visados\n• 🆔 NIE\n• 🏠 Empadronamiento\n\n¿Sobre qué tema quieres información?" + self._legal_note()
            else:
                return f"I can help you with:\n• 📋 First steps\n• 🎫 Visa information\n• 🆔 NIE\n• 🏠 Registration\n\nWhat topic would you like information about?" + self._legal_note()


if __name__ == "__main__":
    print("🌍 Immigration Bot - Test\n")

    # Test en español
    bot_es = ImmigrationBot("es")
    print("ESPAÑOL:")
    print(bot_es.get_greeting())
    print("\n" + "="*80 + "\n")
    print(bot_es.get_visa_info("Argentina")['message'])
    print("\n" + "="*80 + "\n")

    # Test en inglés
    bot_en = ImmigrationBot("en")
    print("ENGLISH:")
    print(bot_en.get_greeting())
