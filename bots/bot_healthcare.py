def responder_consulta(pregunta, anunciantes):
    respuesta = "Opciones de salud y clínicas:\n"
    for anunciante in anunciantes:
        respuesta += f"- {anunciante['nombre']}: {anunciante['descripcion']}\n"
        if 'contacto' in anunciante:
            respuesta += f"  Contacto: {anunciante['contacto']}\n"
        if 'perfil' in anunciante:
            respuesta += f"  Perfil: {anunciante['perfil']}\n"
        respuesta += "\n"
    return respuesta
