import json
import re
import unicodedata
from pathlib import Path

# Los bots se importarán cuando los creemos
# from . import bot_accommodation, bot_arts_culture, etc.

def _normalize(s):
    """Normalizar texto para búsquedas"""
    if not s:
        return ""
    s = str(s).strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()

class Orchestrator:
    def __init__(self):
        # Cargar base de datos de anunciantes con ruta robusta
        try:
            # Determinar ruta a la carpeta data (dos niveles arriba si es necesario)
            base_dir = Path(__file__).resolve().parent.parent
            data_path = base_dir / 'data' / 'anunciantes.json'

            # Fallback: si no existe, intentar ruta relativa simple
            if not data_path.exists():
                data_path = Path(__file__).resolve().parent / 'data' / 'anunciantes.json'

            with open(str(data_path), 'r', encoding='utf-8') as f:
                self.advertisers = json.load(f)
            print("✅ Base de datos cargada correctamente")
        except FileNotFoundError:
            print(f"❌ ERROR: No se encuentra {data_path}")
            self.advertisers = {}
        except Exception as e:
            print(f"❌ ERROR cargando base de datos: {e}")
            self.advertisers = {}

        # Mapeo de bots (inicialmente vacío, se llenará después)
        self.bots_map = {}
        print("✅ Orchestrator iniciado - listo para conectar bots")

    def classify_intent(self, question):
        """Sistema de clasificación MEJORADO para 12 categorías con patrones mejorados"""
        question_norm = _normalize(question)

        print(f"🔍 Analizando pregunta: '{question}'")

        # PRIMERO: Clasificar por categorías con patrones MEJORADOS
        category_patterns = {
            "Accommodation": [
                "hotel", "apartamento", "alojamiento", "vivienda", "alquiler",
                "piso", "habitacion", "residencia", "donde vivir", "busco casa",
                "necesito techo", "alquilar", "airbnb", "hostal", "apartment",
                "rent", "housing", "accommodation", "where to live"
            ],
            "Arts and Culture": [
                "museo", "galeria", "exposicion", "arte", "cultural", "teatro",
                "concierto", "espectaculo", "obra", "pintura", "escultura",
                "actividad cultural", "que ver", "turismo cultural", "visita guiada",
                "museum", "gallery", "exhibition", "art", "theater", "concert"
            ],
            "Bars and Clubs": [
                "bar", "discoteca", "pub", "copas", "noche", "fiesta", "club",
                "musica en vivo", "karaoke", "terraza", "cerveza", "cocktail",
                "donde salir", "vida nocturna", "plan noche", "afterwork",
                "nightlife", "party", "drinks", "pub"
            ],
            "Beauty and Well-Being": [
                "spa", "masaje", "estetica", "belleza", "bienestar", "relajacion",
                "cuidado personal", "peluqueria", "manicura", "facial", "wellness",
                "masajista", "esteticista", "centro belleza", "beauty", "spa",
                "massage", "wellbeing", "salon"
            ],
            "Business Services": [
                "negocio", "empresa", "servicios", "corporativo", "oficina",
                "emprendedor", "consultoria", "asesoria", "professional",
                "business", "co-working", "coworking", "junta", "reunion",
                "services", "corporate", "office", "consulting"
            ],
            "Education": [
                "escuela", "colegio", "universidad", "curso", "idiomas", "academia",
                "educacion", "aprender", "estudiar", "clase", "taller", "formacion",
                "language", "school", "university", "course", "education", "learn"
            ],
            "Healthcare": [
                "medico", "hospital", "clinica", "dentista", "seguro", "salud",
                "doctor", "pediatra", "ginecologo", "psicologo", "fisioterapia",
                "health", "healthcare", "medical", "insurance", "doctor", "clinic"
            ],
            "Home Services": [
                "casa", "hogar", "reparacion", "limpieza", "fontanero", "electricista",
                "carpintero", "mudanza", "pintor", "jardineria", "domestico",
                "home", "services", "cleaning", "plumber", "repair", "moving"
            ],
            "Legal and Financial": [
                "abogado", "legal", "financiero", "ley", "impuestos", "banco",
                "asesor", "contrato", "visado", "nie", "residencia", "permiso",
                "ayuda legal", "consulta", "documentos", "tramites", "derechos",
                "solicitud", "nomina", "contabilidad",
                "lawyer", "legal", "financial", "tax", "bank", "visa", "immigration"
            ],
            "Recreation and Leisure": [
                "ocio", "recreacion", "deporte", "gimnasio", "parque", "diversion",
                "actividad", "entretenimiento", "juego", "deporte", "ejercicio",
                "recreation", "leisure", "sports", "gym", "fun", "park"
            ],
            "Restaurants": [
                "restaurante", "comida", "cenar", "comer", "cena", "almuerzo",
                "gastronomia", "cocina", "menu", "reserva", "terraza", "bar",
                "restaurant", "food", "dinner", "lunch", "cuisine", "reservation"
            ],
            "Retail": [
                "tienda", "compras", "retail", "producto", "ropa", "moda",
                "shopping", "comercio", "venta", "local", "boutique", "centro comercial",
                "store", "shop", "buy", "purchase", "mall", "clothing"
            ],
            "Comercial": [
                "anunciar", "publicidad", "paquete", "campana", "promocion",
                "revista", "media kit", "ads", "advertising", "campaign",
                "advertise", "marketing", "sponsor", "promote"
            ]
        }

        # Buscar coincidencias mejoradas por patrón
        best_match = None
        best_score = 0

        for category, patterns in category_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in question_norm:
                    score += 1

            if score > best_score:
                best_score = score
                best_match = category

        # Si un patrón de categoría coincidió, usar ese (prioridad a patrones)
        if best_match and best_score >= 1:
            confidence = min(0.1 * best_score + 0.5, 0.95)
            print(f"🎯 Categoría detectada por patrón: {best_match} (puntaje: {best_score})")
            return best_match, confidence, None

        # SEGUNDO: Buscar coincidencias exactas con negocios
        for category, businesses in self.advertisers.items():
            for business in businesses:
                business_name = _normalize(business.get('nombre', ''))
                if business_name and business_name in question_norm:
                    print(f"✅ Encontrado negocio: {business['nombre']}")
                    return category, 0.95, business

                # Buscar en descripción con coincidencia de tokens
                desc_norm = _normalize(business.get('descripcion', ''))
                desc_tokens = set(re.findall(r"\w+", desc_norm))
                q_tokens = set(re.findall(r"\w+", question_norm))
                common_tokens = desc_tokens & q_tokens
                
                if len(common_tokens) >= 2:  # Al menos 2 tokens en común
                    print(f"✅ Encontrado por coincidencia semántica: {business['nombre']} (comunes: {common_tokens})")
                    return category, 0.85, business

        # Por defecto, usar Desconocida
        print(f"🎯 Categoría detectada: Desconocida (puntaje: 0)")
        return "Desconocida", 0.3, None

    def process_query(self, question, language="es"):
        """Procesar consulta y generar respuesta"""
        categoria, confidence, advertiser = self.classify_intent(question)

        # Obtener resultados de la categoría
        resultados = self.advertisers.get(categoria, [])

        # Si hay un advertiser específico, agregarlo a resultados
        if advertiser and advertiser not in resultados:
            resultados.insert(0, advertiser)

        # Por ahora, respuesta básica hasta que tengamos los bots
        respuesta = self._generate_basic_response(categoria, resultados, question, language)

        return {
            "respuesta": respuesta.get("text", ""),
            "agente": categoria,
            "confidence": confidence,
            "json": respuesta.get("json", {})
        }

    def _generate_basic_response(self, categoria, resultados, pregunta, language):
        """Generar respuesta básica con estructura estándar"""

        if language == "es":
            if resultados:
                response_text = f"ES:\nCategoría detectada: {categoria}\nResultados principales:\n"
                for resultado in resultados[:3]:
                    response_text += f"- {resultado['nombre']}: {resultado.get('descripcion', 'N/A')}\n"
                    response_text += f"  Contacto: {resultado.get('contacto', 'N/A')}\n"
                
                response_text += f"\n{self._get_tips_es(categoria)}"
            else:
                response_text = f"ES:\nServicio de {categoria} - Próximamente más información detallada."

            response_text += f"\n\nEN:\n"
            
            if resultados:
                response_text += f"Category detected: {categoria}\nTop results:\n"
                for resultado in resultados[:3]:
                    response_text += f"- {resultado['nombre']}: {resultado.get('descripcion', 'N/A')}\n"
                    response_text += f"  Contact: {resultado.get('contacto', 'N/A')}\n"
                
                response_text += f"\n{self._get_tips_en(categoria)}"
            else:
                response_text += f"{categoria} service - More detailed information coming soon."

            return {
                "text": response_text,
                "json": {
                    "categoria": categoria,
                    "opciones": resultados,
                    "pregunta_original": pregunta
                }
            }

        else:  # English
            response_text = f"EN:\n"
            
            if resultados:
                response_text += f"Category detected: {categoria}\nTop results:\n"
                for resultado in resultados[:3]:
                    response_text += f"- {resultado['nombre']}: {resultado.get('descripcion', 'N/A')}\n"
                    response_text += f"  Contact: {resultado.get('contacto', 'N/A')}\n"
                
                response_text += f"\n{self._get_tips_en(categoria)}"
            else:
                response_text += f"{categoria} service - More detailed information coming soon."

            response_text += f"\n\nES:\n"
            
            if resultados:
                response_text += f"Categoría detectada: {categoria}\nResultados principales:\n"
                for resultado in resultados[:3]:
                    response_text += f"- {resultado['nombre']}: {resultado.get('descripcion', 'N/A')}\n"
                    response_text += f"  Contacto: {resultado.get('contacto', 'N/A')}\n"
                
                response_text += f"\n{self._get_tips_es(categoria)}"
            else:
                response_text += f"Servicio de {categoria} - Próximamente más información detallada."

            return {
                "text": response_text,
                "json": {
                    "categoria": categoria,
                    "opciones": resultados,
                    "pregunta_original": pregunta
                }
            }

    def _get_tips_es(self, categoria):
        """Consejos en español para cada categoría"""
        tips = {
            "Accommodation": "• Precios: Hoteles €80-200/noche, Apartamentos €700-1500/mes\n• Zonas recomendadas: Eixample, Gràcia, Barceloneta\n• Webs útiles: Idealista, Fotocasa, Airbnb",
            "Arts and Culture": "• Museos principales: Picasso (€12), MACBA (€11), MNAC (€12)\n• Domingos: Entradas reducidas después de las 15:00\n• Eventos gratis: Primer domingo de cada mes",
            "Bars and Clubs": "• Zonas de fiesta: El Born, Port Olímpic, Gràcia\n• Horario: Bares hasta 2-3 AM, Clubs hasta 6 AM\n• Precio medio: Copa €8-12",
            "Restaurants": "• Horarios: Almuerzo 13:00-16:00, Cena 20:00-23:00\n• Precio medio: Menú del día €12-18, Cena €25-40\n• Reservas recomendadas en fin de semana",
            "Legal and Financial": "• NIE: Cita previa en comisaría\n• Bancos: Cuentas para expats disponibles\n• Impuestos: IRPF progresivo 19%-47%",
        }
        return tips.get(categoria, "• Próximamente más información específica")

    def _get_tips_en(self, categoria):
        """Tips in English for each category"""
        tips = {
            "Accommodation": "• Prices: Hotels €80-200/night, Apartments €700-1500/month\n• Recommended areas: Eixample, Gràcia, Barceloneta\n• Useful websites: Idealista, Fotocasa, Airbnb",
            "Arts and Culture": "• Main museums: Picasso (€12), MACBA (€11), MNAC (€12)\n• Sundays: Discount tickets after 3:00 PM\n• Free events: First Sunday of each month",
            "Bars and Clubs": "• Nightlife areas: El Born, Port Olímpic, Gràcia\n• Hours: Bars until 2-3 AM, Clubs until 6 AM\n• Average price: Drink €8-12",
            "Restaurants": "• Hours: Lunch 1:00-4:00 PM, Dinner 8:00-11:00 PM\n• Average price: Daily menu €12-18, Dinner €25-40\n• Weekend reservations recommended",
            "Legal and Financial": "• NIE: Appointment at police station\n• Banks: Expat accounts available\n• Taxes: Progressive income tax 19%-47%",
        }
        return tips.get(categoria, "• More specific information coming soon")

    def _get_general_info_es(self, categoria):
        """Información general en español"""
        info = {
            "Accommodation": "Encuentra hoteles, apartamentos y viviendas en Barcelona. Zonas recomendadas: Eixample (céntrico), Gràcia (bohemio), Barceloneta (playa).",
            "Arts and Culture": "Descubre museos, galerías y eventos culturales. Barcelona es rica en cultura modernista y contemporánea.",
            "Bars and Clubs": "Vida nocturna vibrante con bares, pubs y discotecas para todos los gustos.",
            "Restaurants": "Gastronomía diversa desde tapas tradicionales hasta cocina de vanguardia.",
            "Legal and Financial": "Asesoría para trámites legales, impuestos, bancos y documentación para expatriados.",
        }
        return info.get(categoria, f"Servicio de {categoria} - Próximamente más información detallada.")

    def _get_general_info_en(self, categoria):
        """General information in English"""
        info = {
            "Accommodation": "Find hotels, apartments and housing in Barcelona. Recommended areas: Eixample (central), Gràcia (bohemian), Barceloneta (beach).",
            "Arts and Culture": "Discover museums, galleries and cultural events. Barcelona is rich in modernist and contemporary culture.",
            "Bars and Clubs": "Vibrant nightlife with bars, pubs and clubs for all tastes.",
            "Restaurants": "Diverse gastronomy from traditional tapas to avant-garde cuisine.",
            "Legal and Financial": "Advice for legal procedures, taxes, banks and documentation for expats.",
        }
        return info.get(categoria, f"{categoria} service - More detailed information coming soon.")
