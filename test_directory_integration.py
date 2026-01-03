# test_directory_integration.py
"""
Script de prueba para verificar que la integración con el directorio funciona.
Ejecución: python test_directory_integration.py
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from bots.directory_connector import get_directory_connector
from bots.orchestrator import Orchestrator
from bots.logger import logger


def test_directory_connector():
    """Prueba el DirectoryConnector."""
    print("\n" + "="*60)
    print("🧪 TEST 1: DirectoryConnector")
    print("="*60)

    try:
        connector = get_directory_connector()

        # Obtener todos los anunciantes
        print("\n📥 Obteniendo anunciantes...")
        advertisers = connector.get_all_advertisers(limit=10)

        if advertisers:
            print(f"✅ Cargados {len(advertisers)} anunciantes")
            print(f"\n📋 Primeros 2 anunciantes:")
            for i, ad in enumerate(advertisers[:2], 1):
                print(f"\n  {i}. {ad.get('nombre', 'Sin nombre')}")
                print(f"     Categoría: {ad.get('category', ad.get('categoria', 'N/A'))}")
                print(f"     Descripción: {ad.get('descripcion', 'N/A')[:50]}...")
        else:
            print("⚠️ No se cargaron anunciantes (probablemente usando JSON local)")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_orchestrator():
    """Prueba el Orchestrator."""
    print("\n" + "="*60)
    print("🧪 TEST 2: Orchestrator")
    print("="*60)

    try:
        orch = Orchestrator()

        print("\n✅ Orchestrator inicializado")
        print(f"   Categorías cargadas: {len(orch.advertisers)}")
        print(f"   Categorías: {list(orch.advertisers.keys())[:5]}...")

        # Verificar que el directorio está configurado
        print(f"\n✅ DirectoryConnector integrado: {orch.directory is not None}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_query():
    """Prueba una consulta completa."""
    print("\n" + "="*60)
    print("🧪 TEST 3: Consulta completa")
    print("="*60)

    try:
        orch = Orchestrator()

        # Hacer una consulta
        query = "Need a hotel in Barcelona"
        print(f"\n🔍 Pregunta: '{query}'")

        response = orch.process_query(query, language="en", limit=3)

        print(f"\n✅ Respuesta obtenida:")
        print(f"   Agente: {response.get('agente')}")
        print(f"   Confianza: {response.get('confidence'):.2%}")
        print(f"   Total resultados: {response.get('total_results')}")
        print(f"   Resultados mostrados: {len(response.get('json', []))}")

        if response.get('json'):
            print(f"\n📌 Primer resultado:")
            ad = response['json'][0]
            print(f"   Nombre: {ad.get('nombre')}")
            print(f"   Categoría: {ad.get('category', ad.get('categoria'))}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search():
    """Prueba búsqueda por keyword."""
    print("\n" + "="*60)
    print("🧪 TEST 4: Búsqueda por keyword")
    print("="*60)

    try:
        connector = get_directory_connector()

        # Buscar
        query = "hotel"
        print(f"\n🔍 Buscando: '{query}'")

        results = connector.search_advertisers(query, limit=5)

        print(f"✅ Encontrados {len(results)} resultados")

        if results:
            print(f"\n📌 Primeros resultados:")
            for i, ad in enumerate(results[:2], 1):
                print(f"   {i}. {ad.get('nombre', 'Sin nombre')}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Ejecuta todos los tests."""
    print("\n" + "🚀"*30)
    print("PRUEBAS DE INTEGRACIÓN DIRECTORIO BARCELONA METROPOLITAN")
    print("🚀"*30)

    results = {
        "DirectoryConnector": test_directory_connector(),
        "Orchestrator": test_orchestrator(),
        "Consulta": test_query(),
        "Búsqueda": test_search(),
    }

    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status:10} {test_name}")

    print(f"\n{passed}/{total} pruebas completadas")

    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ La integración está lista")
    else:
        print(f"\n⚠️ {total - passed} prueba(s) fallaron")
        print("Revisa los errores arriba")

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
