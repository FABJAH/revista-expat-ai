import json
import bots.bot_legal as bot_legal
import bots.bot_accommodation as bot_accommodation
import bots.bot_healthcare as bot_healthcare
import bots.bot_education as bot_education
import bots.bot_work as bot_work
import bots.bot_social as bot_social
import bots.bot_comercial as bot_comercial

# 👉 Aquí cargas el JSON
with open("data/anunciantes.json", "r", encoding="utf-8") as archivo:
    base_datos = json.load(archivo)

# Función para detectar categoría
def detectar_categoria(pregunta):
    pregunta = pregunta.lower().strip()
    categorias = {
        "Accommodation": ["hotel", "apartamento", "alojamiento", "vivienda", "alquiler", "piso"],
        "Legal and Financial": ["abogado", "nie", "residencia", "legal", "documento", "permiso", "impuestos", "banco"],
        "Healthcare": ["médico", "salud", "clínica", "dentista", "seguro", "hospital"],
        "Education": ["escuela", "colegio", "universidad", "curso", "idiomas", "academia"],
        "Work and Networking": ["trabajo", "empleo", "oferta", "coworking", "networking"],
        "Social and Cultural": ["expats", "asociación", "evento", "restaurante", "actividad", "ocio"],
        "Comercial": ["anunciar", "publicidad", "paquete", "campaña", "promoción", "revista"]

    }
    for categoria, palabras in categorias.items():
        if any(palabra in pregunta for palabra in palabras):
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

    print(f"\nCategoría detectada: {categoria}")s
    if categoria == "Legal and Financial":
        print(bot_legal.responder_consulta(pregunta, resultados))
    elif categoria == "Accommodation":
        print(bot_accommodation.responder_consulta(pregunta, resultados))
    elif categoria == "Healthcare":
        print(bot_healthcare.responder_consulta(pregunta, resultados))
    elif categoria == "Education":
        print(bot_education.responder_consulta(pregunta, resultados))
    elif categoria == "Work and Networking":
        print(bot_work.responder_consulta(pregunta, resultados))
    elif categoria == "Social and Cultural":
        print(bot_social.responder_consulta(pregunta, resultados))
    elif categoria == "Comercial":   # 👉 aquí añadimos el nuevo caso
        print(bot_comercial.responder_consulta(pregunta, resultados))
    else:
        print("No se encontraron coincidencias en la base de datos.")
