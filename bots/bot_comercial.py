def responder_consulta(pregunta, paquetes):
    """
    Bot Comercial: ayuda a vender espacios publicitarios en la revista.
    - Explica beneficios
    - Muestra paquetes disponibles
    - Recoge datos de contacto
    """

    respuesta = "📢 Opciones para anunciarse en la revista:\n\n"
    for paquete in paquetes:
        respuesta += f"- {paquete['nombre']}: {paquete['descripcion']}\n"
        if 'precio' in paquete:
            respuesta += f"  Precio: {paquete['precio']}\n"
        if 'beneficios' in paquete:
            respuesta += f"  Beneficios: {', '.join(paquete['beneficios'])}\n"
        respuesta += "\n"

    respuesta += "👉 Si te interesa, podemos agendar una cita o enviarte una propuesta personalizada.\n"
    return respuesta
