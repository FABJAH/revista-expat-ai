# bots/content_manager.py
"""
Gestor de contenido editorial de la revista.
Carga y busca artículos, guías y contenido interno.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional

class ContentManager:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.guides_dir = self.base_dir / "data" / "guides"
        self.articles_dir = self.base_dir / "data" / "articles"
        self.guides = self._load_guides()
        print(f"✅ Contenido editorial cargado: {len(self.guides)} guías disponibles")

    def _load_guides(self) -> List[Dict]:
        """Carga todas las guías disponibles"""
        guides = []
        if self.guides_dir.exists():
            for guide_file in self.guides_dir.glob("*.json"):
                try:
                    with open(guide_file, 'r', encoding='utf-8') as f:
                        guide = json.load(f)
                        guide['tipo'] = 'guia'
                        guides.append(guide)
                except Exception as e:
                    print(f"⚠️  Error cargando {guide_file}: {e}")
        return guides

    def search_guides(self, keywords: List[str], categoria: str = None) -> List[Dict]:
        """
        Busca guías relevantes basándose en keywords y categoría.

        Args:
            keywords: Lista de palabras clave para buscar
            categoria: Categoría específica (Healthcare, Legal, etc.)

        Returns:
            Lista de guías relevantes ordenadas por relevancia
        """
        relevant_guides = []

        for guide in self.guides:
            score = 0

            # Coincidencia de categoría (peso 3)
            if categoria and guide.get('categoria') == categoria:
                score += 3

            # Coincidencia en keywords de la guía (peso 2)
            guide_keywords = [k.lower() for k in guide.get('keywords', [])]
            for keyword in keywords:
                if any(keyword.lower() in gk for gk in guide_keywords):
                    score += 2

            # Coincidencia en título (peso 1)
            titulo = guide.get('titulo', '').lower()
            for keyword in keywords:
                if keyword.lower() in titulo:
                    score += 1

            if score > 0:
                guide_copy = guide.copy()
                guide_copy['relevancia'] = score
                relevant_guides.append(guide_copy)

        # Ordenar por relevancia
        relevant_guides.sort(key=lambda x: x['relevancia'], reverse=True)
        return relevant_guides

    def get_guide_summary(self, guide: Dict) -> Dict:
        """
        Devuelve un resumen corto de la guía para mostrar en el chat.
        """
        return {
            "tipo": "guia_revista",
            "titulo": guide.get('titulo'),
            "resumen": guide.get('resumen'),
            "slug": guide.get('slug'),
            "url": f"/revista/guias/{guide.get('slug')}",
            "categoria": guide.get('categoria')
        }

    def get_guide_highlights(self, guide: Dict, max_items: int = 3) -> List[str]:
        """
        Extrae los puntos más importantes de una guía.
        """
        highlights = []

        for seccion in guide.get('contenido', [])[:max_items]:
            if 'texto' in seccion:
                highlights.append(f"• {seccion['seccion']}: {seccion['texto'][:150]}...")
            elif 'lista' in seccion and seccion['lista']:
                highlights.append(f"• {seccion['seccion']}: {seccion['lista'][0]}")
            elif 'tips' in seccion and seccion['tips']:
                highlights.append(f"• {seccion['tips'][0]}")

        return highlights
