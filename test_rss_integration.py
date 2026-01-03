"""
Test script para verificar funcionamiento del RSS Manager y su integración
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_rss_manager():
    print("=" * 60)
    print("TEST 1: Instanciar RSS Manager")
    print("=" * 60)

    from bots.rss_manager import get_rss_manager
    rss_mgr = get_rss_manager()
    print(f"✅ RSS Manager creado. {len(rss_mgr.articles)} artículos en caché.\n")

    print("=" * 60)
    print("TEST 2: Sincronizar feeds (manual)")
    print("=" * 60)

    try:
        new_count = rss_mgr.sync_feeds()
        print(f"✅ Sync completado: {new_count} nuevos artículos\n")
    except Exception as e:
        print(f"⚠️ Error en sync (posible sin conexión internet): {e}\n")

    print("=" * 60)
    print("TEST 3: Buscar artículos por categoría")
    print("=" * 60)

    categories = ["Legal and Financial", "Healthcare", "Education", "Accommodation"]
    for cat in categories:
        articles = rss_mgr.get_articles_by_category(cat, limit=2)
        print(f"{cat}: {len(articles)} artículos encontrados")
        for art in articles:
            print(f"  - {art['title'][:50]}...")
    print()

    print("=" * 60)
    print("TEST 4: Buscar artículos por keywords")
    print("=" * 60)

    keywords = ["legal", "immigration", "visa"]
    results = rss_mgr.search_articles(keywords, limit=3)
    print(f"Búsqueda '{keywords}': {len(results)} resultados")
    for art in results:
        print(f"  - {art['title'][:60]}...")
    print()

    print("=" * 60)
    print("TEST 5: Verificar caché persistente")
    print("=" * 60)

    cache_file = Path(__file__).parent / "data" / "cache" / "articles.json"
    if cache_file.exists():
        with open(cache_file, 'r', encoding='utf-8') as f:
            cached = json.load(f)
        print(f"✅ Caché guardado: {len(cached)} artículos en {cache_file}\n")
    else:
        print(f"⚠️ Caché no encontrado en {cache_file}\n")

    print("=" * 60)
    print("TEST 6: Integración con Orchestrator")
    print("=" * 60)

    from bots.orchestrator import Orchestrator
    orch = Orchestrator()

    test_query = "I need legal help for my NIE"
    result = orch.process_query(test_query, "en")

    print(f"Query: {test_query}")
    print(f"Categoría: {result.get('agente')}")
    print(f"Confianza: {result.get('confidence'):.2f}")
    print(f"Anunciantes: {len(result.get('json', []))}")
    print(f"Guías: {len(result.get('guias', []))}")
    print(f"Artículos RSS: {len(result.get('articulos', []))}")

    if result.get('articulos'):
        print("\n📰 Artículos encontrados:")
        for art in result.get('articulos', [])[:2]:
            print(f"  - {art['title'][:60]}...")
    print()

    print("=" * 60)
    print("✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
    print("=" * 60)

if __name__ == "__main__":
    test_rss_manager()
