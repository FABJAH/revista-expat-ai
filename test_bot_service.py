from bots.bot_service import responder_consulta


def test_bot_service_returns_all_defined_services():
    result = responder_consulta("quiero un bot")

    assert "json_data" in result
    assert "key_points" in result
    assert len(result["json_data"]) == 2
    assert len(result["key_points"]) == 2

    names = [item.get("nombre") for item in result["json_data"]]
    assert "Bot de Agendamiento de Citas" in names
    assert "Bot de Reservas para Restaurantes" in names
