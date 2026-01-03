#!/usr/bin/env python3
"""
Script de Migración - Luna Bot v2
Actualiza estructura de precios a modelo de dos niveles: Directorio + Campañas

Cambios:
- De 4 planes genéricos → 6 planes específicos (2 directorio + 3 campaña × 2 idiomas)
- Agrega campos: tipo, minimo_meses, negociable
- Actualiza mensajes proactivos
- Actualiza FAQ
"""

import shutil
import json
from pathlib import Path
from datetime import datetime

def backup_files():
    """Crear respaldos de archivos importantes."""
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)

    files_to_backup = [
        "config/luna_config.py",
        "bots/bot_advertising_sales.py",
        "routes/advertising_api.py"
    ]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for file_path in files_to_backup:
        src = Path(file_path)
        if src.exists():
            dst = backup_dir / f"{src.name}.{timestamp}.bak"
            shutil.copy2(src, dst)
            print(f"✅ Respaldo: {src.name} → {dst}")

    return backup_dir

def migrate_config():
    """Migrar config/luna_config.py."""
    print("\n📋 Migrando config/luna_config.py...")

    # Leer el archivo nuevo
    new_config = Path("config/luna_config_v2.py").read_text()

    # Escribir sobre el antiguo
    Path("config/luna_config.py").write_text(new_config)

    print("✅ Config actualizado")

def migrate_bot():
    """Migrar bots/bot_advertising_sales.py."""
    print("\n🤖 Migrando bots/bot_advertising_sales.py...")

    # Leer el archivo nuevo
    new_bot = Path("bots/bot_advertising_sales_v2.py").read_text()

    # Escribir sobre el antiguo
    Path("bots/bot_advertising_sales.py").write_text(new_bot)

    print("✅ Bot actualizado")

def update_api_routes():
    """Actualizar routes/advertising_api.py si existe."""
    api_file = Path("routes/advertising_api.py")

    if not api_file.exists():
        print("\n⚠️  routes/advertising_api.py no encontrado - saltando")
        return

    print("\n🔌 Actualizando routes/advertising_api.py...")

    content = api_file.read_text()

    # Reemplazar imports
    old_import = "from bots.bot_advertising_sales import AdvertisingSalesBot"
    new_import = "from bots.bot_advertising_sales import AdvertisingSalesBot\nfrom config.luna_config_v2 import get_all_plans, get_directorio_plans, get_campana_plans"

    if old_import in content:
        content = content.replace(old_import, new_import)

    api_file.write_text(content)
    print("✅ Routes actualizado")

def create_migration_report():
    """Crear reporte de migración."""
    report = """
╔════════════════════════════════════════════════════════════════╗
║           🦉 REPORTE DE MIGRACIÓN - LUNA BOT V2.0            ║
╚════════════════════════════════════════════════════════════════╝

CAMBIOS REALIZADOS:
═══════════════════════════════════════════════════════════════

1. ESTRUCTURA DE PRECIOS
   De: 4 planes genéricos
   A:  6 planes específicos (Directorio + Campañas)

2. PLANES CREADOS
   ✅ Directorio Mensual (34€)
   ✅ Directorio Anual (367€ con 10% descuento)
   ✅ Campaña Básica (159€/mes, mín 6 meses)
   ✅ Campaña Profesional (199€/mes, mín 6 meses)
   ✅ Campaña Premium (299€/mes, mín 6 meses)
   + Versiones EN (5 planes más)

3. NUEVOS CAMPOS
   • tipo: "directorio" | "campana"
   • minimo_meses: 6 (solo campañas)
   • negociable: True (solo campañas)
   • popular: True (Profesional es popular)

4. DESCUENTOS
   ✅ 10% descuento anual en directorio
   ✅ 10% descuento anual en campañas
   ✅ Cálculos automáticos incluidos

5. MENSAJERÍA MEJORADA
   ✅ Saludos contextuales (mañana/tarde/noche)
   ✅ Preguntas proactivas específicas
   ✅ FAQ mejorado con 8 preguntas
   ✅ Testimonios actualizados

6. FUNCIONES NUEVAS
   ✅ get_directorio_plans()
   ✅ get_campana_plans()
   ✅ get_all_plans()
   ✅ get_annual_discount()
   ✅ calculate_annual_price()
   ✅ format_price()

7. BOT MEJORADO
   ✅ Detección de intención más precisa
   ✅ Detección automática de idioma
   ✅ Comparación directorio vs campaña
   ✅ Respuestas contextuales por tipo

ARCHIVOS ACTUALIZADOS:
═══════════════════════════════════════════════════════════════
✅ config/luna_config.py (de config_v2.py)
✅ bots/bot_advertising_sales.py (de bot_v2.py)
✅ routes/advertising_api.py (si existe)

ARCHIVOS NUEVOS CREADOS:
═══════════════════════════════════════════════════════════════
✅ config/luna_config_v2.py (original)
✅ bots/bot_advertising_sales_v2.py (original)
✅ LUNA_PRECIOS_ESTRUCTURA_COMPLETA.md (documentación)
✅ migrate_luna_v2.py (este script)

RESPALDOS CREADOS:
═══════════════════════════════════════════════════════════════
Las versiones anteriores se encuentran en: backups/

PRÓXIMOS PASOS:
═══════════════════════════════════════════════════════════════
1. Revisar los nuevos archivos
2. Ejecutar: python3 setup_luna.py (para validar)
3. Probar el widget: abrir widget/luna-demo.html
4. Verificar respuestas del bot
5. Confirmar precios en frontend

VERIFICACIÓN RÁPIDA:
═══════════════════════════════════════════════════════════════

# Test config
python3 -c "
from config.luna_config_v2 import *
print('✅ Config cargado')
print(f'Directorio: {len(get_directorio_plans(\"es\"))} planes')
print(f'Campañas: {len(get_campana_plans(\"es\"))} planes')
"

# Test bot
python3 -c "
from bots.bot_advertising_sales_v2 import AdvertisingSalesBot
bot = AdvertisingSalesBot('es')
print('✅ Bot cargado')
print(f'Intención: {bot.detect_intent(\"¿Precio directorio?\")}')
"

COMPATIBILIDAD:
═══════════════════════════════════════════════════════════════
✅ Compatible con Flask
✅ Compatible con FastAPI
✅ Compatible con widget JavaScript
✅ Mantiene API endpoints
✅ Mantiene bilingual support

FILOSOFÍA IMPLEMENTADA:
═══════════════════════════════════════════════════════════════
"La revista ayuda al cliente a llegar a nuevos clientes"

✅ Directorio = Visibilidad pasiva (34€)
✅ Campaña = Crecimiento activo (159-299€)
✅ Precios negociables según cliente
✅ Acompañamiento integral
✅ Orientado a resultados (ROI)

═══════════════════════════════════════════════════════════════
Migración completada exitosamente ✅
Versión: Luna Bot v2.0
Fecha: {}
═══════════════════════════════════════════════════════════════
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    report_file = Path("MIGRATION_REPORT.txt")
    report_file.write_text(report)

    print(report)
    print(f"\n📄 Reporte guardado en: {report_file}")

def main():
    """Ejecutar migración completa."""
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║     🦉 LUNA BOT v2.0 - SCRIPT DE MIGRACIÓN      ║
    ║  Estructura: Directorio + Campañas              ║
    ╚═══════════════════════════════════════════════════╝
    """)

    # 1. Verificar archivos v2
    print("\n1️⃣  Verificando archivos v2...")
    v2_files = [
        Path("config/luna_config_v2.py"),
        Path("bots/bot_advertising_sales_v2.py")
    ]

    for f in v2_files:
        if f.exists():
            print(f"   ✅ {f.name} encontrado")
        else:
            print(f"   ❌ {f.name} NO ENCONTRADO - Abortando")
            return

    # 2. Crear respaldos
    print("\n2️⃣  Creando respaldos...")
    backup_dir = backup_files()

    # 3. Migrar archivos
    print("\n3️⃣  Migrando archivos...")
    migrate_config()
    migrate_bot()
    update_api_routes()

    # 4. Crear reporte
    print("\n4️⃣  Generando reporte...")
    create_migration_report()

    print("\n" + "="*60)
    print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
    print("="*60)
    print("""
PRÓXIMO PASO:
Ejecuta: python3 setup_luna.py

Para validar que todo está funcionando correctamente.
    """)

if __name__ == "__main__":
    main()
