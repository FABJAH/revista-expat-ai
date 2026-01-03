"""
Seed initial articles into cache for demo purposes.
Use this if RSS feeds are not accessible during development.
"""

import json
from pathlib import Path
from datetime import datetime

def seed_cache():
    """Cargar artículos de demostración en el caché"""

    demo_articles = [
        {
            "url": "https://www.barcelona-metropolitan.com/article/nie-residency-explained",
            "title": "NIE Residency Explained: Your Complete Guide",
            "description": "Understanding the NIE (Número de Identidad de Extranjero) is crucial for anyone planning to stay in Spain. Learn what you need to know about residency applications.",
            "published": "2024-01-15T10:30:00Z",
            "categories": ["legal", "immigration", "residency"],
            "source": "Barcelona Metropolitan",
            "synced_at": datetime.utcnow().isoformat()
        },
        {
            "url": "https://www.barcelona-metropolitan.com/article/finding-apartment-barcelona",
            "title": "Finding Your Perfect Apartment in Barcelona",
            "description": "A practical guide to navigating the Barcelona rental market. Learn about neighborhoods, contracts, and what to expect when looking for accommodation.",
            "published": "2024-01-12T14:20:00Z",
            "categories": ["accommodation", "housing", "rental"],
            "source": "Barcelona Metropolitan",
            "synced_at": datetime.utcnow().isoformat()
        },
        {
            "url": "https://www.barcelona-metropolitan.com/article/healthcare-barcelona",
            "title": "Understanding Barcelona's Healthcare System",
            "description": "Guide to accessing healthcare services in Barcelona. Information about insurance, clinics, and public health services for expatriates.",
            "published": "2024-01-10T09:15:00Z",
            "categories": ["healthcare", "medical", "insurance"],
            "source": "Barcelona Metropolitan",
            "synced_at": datetime.utcnow().isoformat()
        },
        {
            "url": "https://www.barcelona-metropolitan.com/article/spanish-courses-barcelona",
            "title": "Best Spanish Language Schools in Barcelona",
            "description": "Discover the top Spanish language courses in Barcelona. Compare intensive programs, conversation classes, and academic options for all levels.",
            "published": "2024-01-08T11:45:00Z",
            "categories": ["education", "language", "course"],
            "source": "Barcelona Metropolitan",
            "synced_at": datetime.utcnow().isoformat()
        },
        {
            "url": "https://www.barcelona-metropolitan.com/article/jobs-barcelona",
            "title": "Job Hunting in Barcelona: Where to Find Work",
            "description": "Strategies for finding employment in Barcelona as an expatriate. Explore job boards, networking opportunities, and visa requirements for work.",
            "published": "2024-01-05T16:00:00Z",
            "categories": ["work", "employment", "job"],
            "source": "Barcelona Metropolitan",
            "synced_at": datetime.utcnow().isoformat()
        },
        {
            "url": "https://www.barcelona-metropolitan.com/article/restaurants-guide",
            "title": "Dining Out in Barcelona: Restaurant Guide",
            "description": "Explore the best restaurants in Barcelona across different cuisines and neighborhoods. From Michelin-starred to local favorites.",
            "published": "2024-01-03T12:30:00Z",
            "categories": ["restaurants", "dining", "food"],
            "source": "Barcelona Metropolitan",
            "synced_at": datetime.utcnow().isoformat()
        },
        {
            "url": "https://www.barcelona-metropolitan.com/article/taxes-barcelona",
            "title": "Tax Obligations for Expats in Barcelona",
            "description": "Understand your tax responsibilities as a resident of Barcelona. Guide to income tax, property tax, and filing requirements.",
            "published": "2024-01-01T08:00:00Z",
            "categories": ["legal", "financial", "taxes"],
            "source": "Barcelona Metropolitan",
            "synced_at": datetime.utcnow().isoformat()
        },
        {
            "url": "https://www.barcelona-metropolitan.com/article/sports-recreation",
            "title": "Recreation & Sports Activities in Barcelona",
            "description": "Active lifestyle guide for Barcelona. Find gyms, sports clubs, outdoor activities, and recreation centers throughout the city.",
            "published": "2023-12-30T13:20:00Z",
            "categories": ["recreation", "sports", "leisure"],
            "source": "Barcelona Metropolitan",
            "synced_at": datetime.utcnow().isoformat()
        }
    ]

    cache_dir = Path(__file__).resolve().parent.parent / "data" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    cache_file = cache_dir / "articles.json"

    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(demo_articles, f, ensure_ascii=False, indent=2)
        print(f"✅ Demo articles seeded to {cache_file}")
        print(f"   Total articles: {len(demo_articles)}")
        return True
    except Exception as e:
        print(f"❌ Error seeding cache: {e}")
        return False

if __name__ == "__main__":
    seed_cache()
