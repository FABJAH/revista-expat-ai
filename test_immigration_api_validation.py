from flask import Flask

from routes.immigration_api import immigration_api


def build_test_app():
    app = Flask(__name__)
    app.register_blueprint(immigration_api)
    return app


def test_immigration_requires_json_content_type():
    app = build_test_app()
    client = app.test_client()

    resp = client.post(
        "/api/immigration",
        data="message=hola",
        content_type="text/plain",
    )

    assert resp.status_code == 415
    data = resp.get_json()
    assert "Content-Type" in data["error"]


def test_immigration_rejects_too_long_message():
    app = build_test_app()
    client = app.test_client()

    payload = {"message": "a" * 1001, "language": "es"}
    resp = client.post("/api/immigration", json=payload)

    assert resp.status_code == 400
    data = resp.get_json()
    assert "1000" in data["error"]
