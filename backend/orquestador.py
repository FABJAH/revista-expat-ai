import json
import unicodedata
import bots.bot_legal as bot_legal
import bots.bot_accommodation as bot_accommodation
import bots.bot_healthcare as bot_healthcare
import bots.bot_education as bot_education
import bots.bot_work as bot_work
import bots.bot_social as bot_social
import bots.bot_comercial as bot_comercial

# 👉 Aquí cargas el JSON
with open("../data/anunciantes.json", "r", encoding="utf-8") as archivo:
base_datos = json.load(archivo)


def _normalize(s):
    if not s:
        return ""
    s = str(s)
    s = s.strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()


# Función para detectar categoría (normaliza acentos y mayúsculas y añade sinónimos)
def detectar_categoria(pregunta):
    pregunta_norm = _normalize(pregunta)

    categorias = {
        "Accommodation": ["hotel", "apartamento", "alojamiento", "vivienda", "alquiler", "piso", "room", "rent", "housing"],
        "Legal and Financial": ["abogado", "nie", "residencia", "legal", "documento", "permiso", "impuesto", "impuestos", "banco", "lawyer", "tax"],
        "Healthcare": ["medico", "medico", "salud", "clinica", "dentista", "seguro", "hospital", "doctor", "health"],
        "Education": ["escuela", "colegio", "universidad", "curso", "idiomas", "academia", "curso", "language", "school"],
        "Work and Networking": ["trabajo", "empleo", "oferta", "coworking", "networking", "job", "trabajar"],
        "Social and Cultural": ["expats", "asociacion", "asociacion", "evento", "restaurante", "actividad", "ocio", "community"],
        "Comercial": ["anunciar", "publicidad", "paquete", "campana", "promocion", "revista", "advertising", "ads"]
    }

    for categoria, palabras in categorias.items():
        for palabra in palabras:
            if palabra in pregunta_norm:
                return categoria
    return "Desconocida"


# Procesar la pregunta y devolver resultados
def procesar_pregunta(pregunta):
    categoria = detectar_categoria(pregunta)
    resultados = base_datos.get(categoria, [])
    return categoria, resultados


# Programa principal
if __name__ == "__main__":
    pregunta = input("¿Qué necesitas saber?\n")
    categoria, resultados = procesar_pregunta(pregunta)

    print(f"\nCategoría detectada: {categoria}")

    # Llamar al subbot correspondiente y esperar estructura estándar
    bot_result = None
    if categoria == "Legal and Financial":
        bot_result = bot_legal.responder_consulta(pregunta, resultados)
    elif categoria == "Accommodation":
        bot_result = bot_accommodation.responder_consulta(pregunta, resultados)
    elif categoria == "Healthcare":
        bot_result = bot_healthcare.responder_consulta(pregunta, resultados)
    elif categoria == "Education":
        bot_result = bot_education.responder_consulta(pregunta, resultados)
    elif categoria == "Work and Networking":
        bot_result = bot_work.responder_consulta(pregunta, resultados)
    elif categoria == "Social and Cultural":
        bot_result = bot_social.responder_consulta(pregunta, resultados)
    elif categoria == "Comercial":
        bot_result = bot_comercial.responder_consulta(pregunta, resultados)
    else:
        bot_result = {"json": {"categoria": categoria, "opciones": []}, "text": "ES: No se encontraron coincidencias.\nEN: No matches found."}

    # Imprimir texto amigable bilingüe y JSON estructurado
    if isinstance(bot_result, dict):
        text = bot_result.get("text")
        json_part = bot_result.get("json")
        if text:
            print("\n" + text)
        if json_part is not None:
            print("\nJSON estructurado:")
            print(json.dumps(json_part, ensure_ascii=False, indent=2))
    else:
        # Compatibilidad con posibles respuestas antiguas
        print(bot_result)
