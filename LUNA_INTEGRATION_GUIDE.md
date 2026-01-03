# 🦉 Guía de Integración Rápida - Luna Bot

## 1. Registrar el Blueprint en Flask

En tu archivo principal (app.py, main.py, etc):

```python
from flask import Flask
from routes.advertising_api import register_advertising_api

app = Flask(__name__)

# Registrar Luna API
register_advertising_api(app)

# Otros blueprints...

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## 2. Incluir el Widget en tu HTML

En la página donde quieras que aparezca Luna:

```html
<!DOCTYPE html>
<html>
<head>
    <!-- Importar CSS del widget -->
    <link rel="stylesheet" href="/static/widget/luna-advertising.css">
</head>
<body>
    <!-- Tu contenido aquí -->
    <h1>Bienvenido a nuestra revista</h1>

    <!-- Importar JS del widget (al final del body) -->
    <script src="/static/widget/luna-advertising.js"></script>

    <!-- Opcional: Configurar idioma -->
    <script>
        window.lunaLanguage = 'es'; // 'es' o 'en'
    </script>
</body>
</html>
```

## 3. Configurar Rutas Estáticas (Flask)

En tu app Flask:

```python
app.static_folder = 'widget'  # O donde tengas los archivos
```

O mejor, servir desde el directorio widget:

```python
@app.route('/widget/<path:filename>')
def widget(filename):
    from flask import send_from_directory
    return send_from_directory('widget', filename)
```

## 4. Probar

1. Inicia tu servidor Flask
2. Abre tu página en navegador
3. Deberías ver el widget en la esquina inferior derecha (🦉)
4. Abre la demo en `widget/luna-demo.html` para ver todas las features

## 5. Personalización

Edita los archivos:
- `config/luna_config.py` - Planes, mensajes, configuración
- `bots/bot_advertising_sales.py` - Lógica del bot
- `widget/luna-advertising.css` - Estilos
- `widget/luna-advertising.js` - Comportamiento del widget

## ⚠️ Consideraciones Importantes

- Los leads se guardan en `data/inquiries/` (crear carpeta si no existe)
- Los logs van a `data/logs/` (crear carpeta si no existe)
- Asegúrate que las carpetas `data/` tienen permisos de escritura

## 🆘 Troubleshooting

### Widget no aparece
- Verifica que las rutas a los archivos JS/CSS son correctas
- Revisa la consola del navegador (F12) para errores

### API no responde
- Verifica que Flask está corriendo
- Revisa que `/api/bot/advertising` está registrado
- Mira los logs de Flask

### Leads no se guardan
- Verifica que `data/inquiries/` existe y tiene permisos de escritura
- Revisa los logs en `data/logs/advertising_conversations.jsonl`

---

¡Listo! Luna debería estar funcionando. 🎉
