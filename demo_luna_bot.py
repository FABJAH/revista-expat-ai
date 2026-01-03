#!/usr/bin/env python3
"""
Demo Interactivo de Luna Bot v2.0
Muestra cómo funciona el bot de ventas con la nueva estructura de precios
"""

import sys
sys.path.insert(0, '/home/fleet/Escritorio/Revista-expats-ai')

from bots.bot_advertising_sales import AdvertisingSalesBot
from config.luna_config import get_all_plans, get_directorio_plans, get_campana_plans

def print_separator(title=""):
    """Imprimir separador visual."""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    else:
        print(f"{'='*70}\n")

def demo_saludo():
    """Demo de saludos."""
    print_separator("🦉 DEMO 1: SALUDOS CONTEXTUALES")

    bot = AdvertisingSalesBot("es")
    print("🤖 Bot en ESPAÑOL:")
    print(bot.get_greeting())

    print("\n" + "-"*70 + "\n")

    bot_en = AdvertisingSalesBot("en")
    print("🤖 Bot en INGLÉS:")
    print(bot_en.get_greeting())

def demo_comparacion_planes():
    """Demo de comparación de planes."""
    print_separator("📊 DEMO 2: COMPARACIÓN DIRECTORIO vs CAMPAÑA")

    bot = AdvertisingSalesBot("es")
    print(bot.get_plans_comparison())

def demo_preguntas():
    """Demo de preguntas y respuestas."""
    print_separator("💬 DEMO 3: PREGUNTAS Y RESPUESTAS")

    bot = AdvertisingSalesBot("es")

    preguntas = [
        "¿Cuál es el precio del directorio?",
        "Quiero hacer una campaña de marketing",
        "¿Hay descuento anual?",
        "¿Son negociables los precios?",
        "¿Cuál es la diferencia entre directorio y campaña?",
        "Hola, buenos días"
    ]

    for i, pregunta in enumerate(preguntas, 1):
        print(f"👤 Usuario: \"{pregunta}\"")
        print(f"🦉 Luna: {bot.get_response(pregunta)}")
        if i < len(preguntas):
            print("\n" + "-"*70 + "\n")

def demo_deteccion_idioma():
    """Demo de detección de idioma."""
    print_separator("🌍 DEMO 4: DETECCIÓN AUTOMÁTICA DE IDIOMA")

    bot = AdvertisingSalesBot("es")

    tests = [
        ("Hola, ¿cuánto cuesta?", "Español esperado"),
        ("Hello, how much does it cost?", "Inglés esperado"),
        ("Buenos días, necesito información", "Español esperado"),
        ("Good morning, I need information", "Inglés esperado"),
    ]

    for texto, esperado in tests:
        idioma_detectado = bot.detect_language(texto)
        print(f"📝 Texto: \"{texto}\"")
        print(f"🔍 Idioma detectado: {idioma_detectado.upper()} ({esperado})")
        print()

def demo_deteccion_intencion():
    """Demo de detección de intención."""
    print_separator("🎯 DEMO 5: DETECCIÓN DE INTENCIÓN")

    bot = AdvertisingSalesBot("es")

    tests = [
        "Hola buenos días",
        "¿Cuánto cuesta el plan?",
        "Quiero aparecer en el directorio",
        "Necesito una campaña de marketing",
        "¿Tienen descuento anual?",
        "¿Puedo negociar el precio?",
        "¿Cómo puedo contactarlos?",
    ]

    for texto in tests:
        intencion = bot.detect_intent(texto)
        print(f"📝 Usuario: \"{texto}\"")
        print(f"🎯 Intención detectada: {intencion.upper()}")
        print()

def demo_testimonios():
    """Demo de testimonios."""
    print_separator("⭐ DEMO 6: CASOS DE ÉXITO")

    bot = AdvertisingSalesBot("es")
    print(bot.get_testimonials())

def demo_planes_config():
    """Demo de configuración de planes."""
    print_separator("📋 DEMO 7: ESTRUCTURA DE PLANES EN CONFIG")

    # Planes de directorio
    print("📍 PLANES DE DIRECTORIO (Español):")
    directorio_planes = get_directorio_plans("es")
    for plan in directorio_planes:
        print(f"\n  {plan['emoji']} {plan['nombre']}")
        print(f"     Precio: {plan['precio']}€/{plan['periodo']}")
        print(f"     Tipo: {plan['tipo']}")
        print(f"     Beneficios: {len(plan['beneficios'])} incluidos")

    print("\n" + "-"*70)

    # Planes de campaña
    print("\n📢 PLANES DE CAMPAÑA (Español):")
    campana_planes = get_campana_plans("es")
    for plan in campana_planes:
        print(f"\n  {plan['emoji']} {plan['nombre']}")
        print(f"     Precio: {plan['precio']}€/{plan['periodo']}")
        print(f"     Tipo: {plan['tipo']}")
        print(f"     Mínimo: {plan['minimo_meses']} meses")
        print(f"     Negociable: {'Sí' if plan['negociable'] else 'No'}")
        print(f"     Popular: {'⭐ SÍ' if plan.get('popular', False) else 'No'}")

def demo_conversacion_completa():
    """Demo de conversación completa."""
    print_separator("💬 DEMO 8: CONVERSACIÓN COMPLETA")

    bot = AdvertisingSalesBot("es")

    conversacion = [
        "Hola",
        "Quiero saber sobre sus servicios",
        "¿Cuál es la diferencia entre directorio y campaña?",
        "Me interesa la campaña profesional",
        "¿Puedo negociar el precio?",
        "Perfecto, gracias"
    ]

    for mensaje in conversacion:
        print(f"👤 Usuario: {mensaje}")
        respuesta = bot.get_response(mensaje)
        print(f"🦉 Luna: {respuesta}")
        print("\n" + "-"*70 + "\n")

def menu_interactivo():
    """Menú interactivo para probar el bot."""
    print_separator("🎮 MODO INTERACTIVO")

    bot = AdvertisingSalesBot("es")

    print("Escribe tus preguntas y Luna responderá.")
    print("Escribe 'salir' para terminar.\n")

    while True:
        try:
            pregunta = input("👤 Tú: ").strip()

            if not pregunta:
                continue

            if pregunta.lower() in ['salir', 'exit', 'quit']:
                print("\n🦉 Luna: ¡Hasta luego! Espero haberte ayudado.\n")
                break

            respuesta = bot.get_response(pregunta)
            print(f"🦉 Luna: {respuesta}\n")

        except KeyboardInterrupt:
            print("\n\n🦉 Luna: ¡Hasta luego!\n")
            break

def main():
    """Menú principal."""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    🦉 LUNA BOT v2.0 - DEMOSTRACIÓN                      ║
║                  Bot de Ventas - Estructura de Precios                   ║
║              Directorio (34€) + Campañas (159€/199€/299€)               ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

    while True:
        print("\n¿Qué demo quieres ver?")
        print("\n  1. Saludos contextuales")
        print("  2. Comparación Directorio vs Campaña")
        print("  3. Preguntas y Respuestas")
        print("  4. Detección de idioma")
        print("  5. Detección de intención")
        print("  6. Casos de éxito (testimonios)")
        print("  7. Estructura de planes (config)")
        print("  8. Conversación completa")
        print("  9. Modo interactivo (prueba tú mismo)")
        print("  0. Mostrar TODOS los demos")
        print("  q. Salir")

        opcion = input("\n🎯 Opción: ").strip().lower()

        if opcion == 'q':
            print("\n👋 ¡Hasta luego!\n")
            break
        elif opcion == '1':
            demo_saludo()
        elif opcion == '2':
            demo_comparacion_planes()
        elif opcion == '3':
            demo_preguntas()
        elif opcion == '4':
            demo_deteccion_idioma()
        elif opcion == '5':
            demo_deteccion_intencion()
        elif opcion == '6':
            demo_testimonios()
        elif opcion == '7':
            demo_planes_config()
        elif opcion == '8':
            demo_conversacion_completa()
        elif opcion == '9':
            menu_interactivo()
        elif opcion == '0':
            demo_saludo()
            demo_comparacion_planes()
            demo_preguntas()
            demo_deteccion_idioma()
            demo_deteccion_intencion()
            demo_testimonios()
            demo_planes_config()
            demo_conversacion_completa()
            print("\n✅ TODOS LOS DEMOS COMPLETADOS\n")
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!\n")
