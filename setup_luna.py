#!/usr/bin/env python3
"""
Setup Script para Luna Advertising Bot
Verifica e instala todas las dependencias necesarias
"""

import os
import sys
import json
from pathlib import Path

# Colores para terminal
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

def check_directories(base_path):
    """Verifica y crea directorios necesarios."""
    print_info("Verificando estructura de directorios...")

    required_dirs = [
        'widget',
        'bots',
        'routes',
        'config',
        'docs',
        'data',
        'data/inquiries',
        'data/logs'
    ]

    for dir_name in required_dirs:
        dir_path = Path(base_path) / dir_name
        if dir_path.exists():
            print_success(f"Directorio {dir_name}/ existe")
        else:
            dir_path.mkdir(parents=True, exist_ok=True)
            print_warning(f"Directorio {dir_name}/ creado")

    return True

def check_files(base_path):
    """Verifica que todos los archivos necesarios existan."""
    print_info("Verificando archivos necesarios...")

    required_files = [
        'bots/bot_advertising_sales.py',
        'routes/advertising_api.py',
        'config/luna_config.py',
        'widget/luna-advertising.js',
        'widget/luna-advertising.css',
        'widget/luna-demo.html',
        'docs/LUNA_BOT_DOCUMENTATION.md'
    ]

    missing_files = []

    for file_name in required_files:
        file_path = Path(base_path) / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            print_success(f"{file_name} ({size:,} bytes)")
        else:
            print_error(f"{file_name} NO ENCONTRADO")
            missing_files.append(file_name)

    if missing_files:
        print_error(f"Faltan {len(missing_files)} archivos:")
        for f in missing_files:
            print(f"  - {f}")
        return False

    return True

def check_python_environment():
    """Verifica versión de Python."""
    print_info("Verificando Python...")

    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print_success(f"Python {python_version.major}.{python_version.minor}")
        return True
    else:
        print_error(f"Python {python_version.major}.{python_version.minor} - Se requiere 3.8+")
        return False

def check_dependencies():
    """Verifica dependencias de Python."""
    print_info("Verificando dependencias de Python...")

    required_packages = ['flask', 'pathlib']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package}")
        except ImportError:
            print_warning(f"{package} - No instalado")
            missing_packages.append(package)

    if missing_packages:
        print_warning(f"Faltan {len(missing_packages)} paquetes")
        print_info(f"Instala con: pip install {' '.join(missing_packages)}")
        return False

    return True

def validate_json_files(base_path):
    """Valida que archivos JSON sean válidos."""
    print_info("Validando archivos de configuración...")

    # No hay JSON en Luna, pero podemos chequear imports
    try:
        config_path = Path(base_path) / 'config' / 'luna_config.py'
        if config_path.exists():
            # Intentar importar la configuración
            import importlib.util
            spec = importlib.util.spec_from_file_location("luna_config", config_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Verificar que hay datos
            if hasattr(module, 'PLANS_CONFIG'):
                print_success("Configuración de planes cargada")
            if hasattr(module, 'MASCOT_CONFIG'):
                print_success("Configuración de mascota cargada")
            if hasattr(module, 'DYNAMIC_MESSAGES'):
                print_success("Mensajes dinámicos cargados")

            return True
    except Exception as e:
        print_error(f"Error al cargar configuración: {e}")
        return False

def check_flask_integration(base_path):
    """Verifica que la integración con Flask es posible."""
    print_info("Verificando integración con Flask...")

    api_path = Path(base_path) / 'routes' / 'advertising_api.py'

    if not api_path.exists():
        print_error("advertising_api.py no encontrado")
        return False

    with open(api_path) as f:
        content = f.read()
        if 'register_advertising_api' in content:
            print_success("Blueprint para registrar encontrado")
        if 'Flask' in content:
            print_success("Importaciones de Flask presentes")

    return True

def create_env_file(base_path):
    """Crea archivo de ejemplo .env"""
    print_info("Creando archivo de configuración de ejemplo...")

    env_content = """# Luna Advertising Bot - Configuración
# Copia este archivo a .env y personaliza

# Idioma por defecto
LUNA_DEFAULT_LANGUAGE=es

# Posición del widget
LUNA_WIDGET_POSITION=bottom-right

# Auto-abrir widget
LUNA_AUTO_OPEN=true

# Delay para auto-abrir (ms)
LUNA_AUTO_OPEN_DELAY=3000

# Email para leads
LUNA_ADMIN_EMAIL=admin@revistaexpatriados.es

# Webhook para leads (opcional)
# LUNA_WEBHOOK_URL=https://tu-api.com/webhooks/leads

# Base de datos (opcional)
# DATABASE_URL=sqlite:///luna_leads.db
"""

    env_path = Path(base_path) / '.env.example'
    try:
        env_path.write_text(env_content)
        print_success("Archivo .env.example creado")
        return True
    except Exception as e:
        print_error(f"Error creando .env.example: {e}")
        return False

def create_integration_guide(base_path):
    """Crea guía rápida de integración."""
    print_info("Creando guía de integración...")

    guide = """# 🦉 Guía de Integración Rápida - Luna Bot

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
"""

    guide_path = Path(base_path) / 'LUNA_INTEGRATION_GUIDE.md'
    try:
        guide_path.write_text(guide)
        print_success("Guía de integración creada")
        return True
    except Exception as e:
        print_error(f"Error creando guía: {e}")
        return False

def run_checks(base_path):
    """Ejecuta todos los chequeos."""
    print_header(f"🦉 Setup de Luna Advertising Bot")

    results = {
        'python': check_python_environment(),
        'dependencies': check_dependencies(),
        'directories': check_directories(base_path),
        'files': check_files(base_path),
        'config': validate_json_files(base_path),
        'flask': check_flask_integration(base_path)
    }

    print_header("Creando Archivos Adicionales")
    create_env_file(base_path)
    create_integration_guide(base_path)

    print_header("Resumen")

    all_good = all(results.values())

    for check, result in results.items():
        status = f"{GREEN}✅ OK{RESET}" if result else f"{RED}❌ FALLÓ{RESET}"
        print(f"{check.capitalize()}: {status}")

    if all_good:
        print_success("\n¡Todos los chequeos pasaron! 🎉")
        print("\nPróximos pasos:")
        print("1. Registra el blueprint en tu app Flask")
        print("2. Incluye luna-advertising.js y .css en tu HTML")
        print("3. Abre widget/luna-demo.html para ver la demo")
        print("4. Personaliza config/luna_config.py según tus planes")
        return 0
    else:
        print_error("\nAlgunos chequeos fallaron.")
        print("Por favor, revisa los errores arriba.")
        return 1

if __name__ == '__main__':
    # Obtener ruta base
    base_path = Path(__file__).parent.absolute()

    exit_code = run_checks(base_path)
    sys.exit(exit_code)
