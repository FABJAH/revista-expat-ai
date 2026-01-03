#!/usr/bin/env python3
"""
Scraper para extraer anunciantes del directorio real de Barcelona Metropolitan
Extrae: nombre, categoría, descripción, ubicación, teléfono, email, web
"""

import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from typing import Dict, List, Optional
import time

# Categorías del directorio
CATEGORIES = {
    "accommodation": "Accommodation",
    "arts-culture": "Arts and Culture",
    "bars-and-clubs": "Bars and Clubs",
    "beauty-and-well-being": "Beauty and Well-Being",
    "business-services": "Business Services",
    "education": "Education",
    "medical": "Healthcare",
    "home-services-1": "Home Services",
    "legal-and-financial": "Legal and Financial",
    "recreation-and-leisure": "Recreation and Leisure",
    "restaurant": "Restaurants",
    "retail": "Retail"
}

BASE_URL = "https://www.barcelona-metropolitan.com/search/location"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
}

class DirectoryScraper:
    def __init__(self):
        self.advertisers = []
        self.session = requests.Session()

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch una página y retorna el contenido parseado"""
        try:
            response = self.session.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            return None

    def extract_advertisers_from_page(self, html: BeautifulSoup, category: str) -> List[Dict]:
        """Extrae anunciantes de una página HTML"""
        advertisers = []

        # Buscar todos los anuncios en la página
        entries = html.find_all('h4')

        for entry in entries:
            try:
                # Obtener nombre del negocio (del enlace h4)
                link = entry.find('a')
                if not link:
                    continue

                name = link.get_text(strip=True)
                url = link.get('href', '').strip()

                # Obtener el contenedor principal
                container = entry.find_parent('div', class_='card')
                if not container:
                    continue

                # Obtener ubicación
                location_text = ""
                location_elem = container.find('p')
                if location_elem and location_elem.find('a'):
                    location_text = location_elem.find('a').get_text(strip=True)

                # Obtener descripción
                description = ""
                desc_elem = container.find('p', class_='description')
                if desc_elem:
                    description = desc_elem.get_text(strip=True)
                else:
                    # Intentar obtener texto que sigue al nombre
                    text_parts = container.find_all('p')
                    for p in text_parts:
                        text = p.get_text(strip=True)
                        if text and text != location_text:
                            description = text
                            break

                advertiser = {
                    "nombre": name,
                    "categoria": category,
                    "descripcion": description,
                    "ubicacion": location_text,
                    "url": url,
                    "tipo_plan": "Directorio",  # Asumido por defecto
                    "precio_mes": 34,  # Directorio base
                    "paquete": "directorio"
                }

                advertisers.append(advertiser)

            except Exception as e:
                print(f"⚠️  Error parsing entry: {e}")
                continue

        return advertisers

    def scrape_category(self, category_slug: str, category_name: str) -> List[Dict]:
        """Scrape todos los anunciantes de una categoría"""
        print(f"\n📍 Scraping {category_name}...")

        all_advertisers = []
        page = 1

        while True:
            url = f"{BASE_URL}/{category_slug}/?page={page}"
            print(f"  → Página {page}...")

            html = self.fetch_page(url)
            if not html:
                break

            # Extraer anunciantes de esta página
            advertisers = self.extract_advertisers_from_page(html, category_name)

            if not advertisers:
                print(f"  → Fin de categoría (página {page} sin resultados)")
                break

            all_advertisers.extend(advertisers)
            print(f"    ✅ {len(advertisers)} anunciantes encontrados")

            page += 1
            time.sleep(1)  # Respetar al servidor

        return all_advertisers

    def scrape_all(self) -> List[Dict]:
        """Scrape todas las categorías"""
        print("🚀 Iniciando scrape del directorio Barcelona Metropolitan...")
        print(f"📊 Total de categorías: {len(CATEGORIES)}\n")

        for slug, name in CATEGORIES.items():
            advertisers = self.scrape_category(slug, name)
            self.advertisers.extend(advertisers)

        return self.advertisers

    def save_to_json(self, filepath: str):
        """Guardar anunciantes en JSON"""
        output = {
            "total": len(self.advertisers),
            "timestamp": str(time.strftime('%Y-%m-%d %H:%M:%S')),
            "source": "barcelona-metropolitan.com/directory",
            "advertisers": self.advertisers
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Guardado: {len(self.advertisers)} anunciantes en {filepath}")


def main():
    scraper = DirectoryScraper()

    # Scrape all categories
    scraper.scrape_all()

    # Save to JSON
    output_path = Path(__file__).parent / 'data' / 'anunciantes_metropolitan.json'
    scraper.save_to_json(str(output_path))

    # Mostrar resumen
    print("\n" + "="*50)
    print("📊 RESUMEN DEL SCRAPE")
    print("="*50)
    print(f"Total anunciantes: {len(scraper.advertisers)}")

    # Agrupar por categoría
    by_category = {}
    for adv in scraper.advertisers:
        cat = adv['categoria']
        by_category[cat] = by_category.get(cat, 0) + 1

    for cat, count in sorted(by_category.items()):
        print(f"  • {cat}: {count}")


if __name__ == "__main__":
    main()
