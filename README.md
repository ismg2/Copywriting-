# Copywriting Agent

Agent de copywriting IA pour générer des articles, blogs et études de cas de qualité professionnelle.

## Architecture

```
src/
├── agent/                 # Moteur principal
│   ├── writer.py          # CopywritingAgent - orchestrateur central
│   ├── pipeline.py        # Pipeline 5 étapes: Research → Outline → Draft → Edit → Polish
│   └── personas.py        # 6 personas pré-configurées (ton, style, audience)
├── templates/             # Structures par type de contenu
│   ├── article.py         # Articles de fond
│   ├── blog.py            # Blog posts
│   └── usecase.py         # Études de cas (Problème → Solution → Résultat)
├── tools/                 # Outils d'analyse
│   ├── seo.py             # Score SEO (titres, densité, structure, meta)
│   ├── readability.py     # Score lisibilité (phrases, vocabulaire, aération)
│   └── keywords.py        # Extraction et densité de mots-clés
├── prompts/               # System prompts par étape du pipeline
│   ├── research.py
│   ├── outline.py
│   ├── drafting.py
│   └── editing.py
config/settings.yaml       # Configuration globale
main.py                    # CLI
```

## Installation

```bash
# Cloner le repo
git clone <repo-url>
cd Copywriting-

# Installer les dépendances
pip install -e ".[all]"

# Configurer la clé API (au choix)
export ANTHROPIC_API_KEY="sk-ant-..."
# ou
export OPENAI_API_KEY="sk-..."
```

## Utilisation CLI

```bash
# Générer un article
python main.py write --topic "L'IA dans le marketing" --type article --persona expert_b2b

# Générer un blog post
python main.py write -t "10 astuces SEO" -T blog -p seo_specialist -k "SEO,référencement"

# Générer une étude de cas
python main.py write -t "Migration cloud chez TechCorp" -T usecase -w 2000

# Lister les personas
python main.py list-personas

# Analyser un contenu existant
python main.py analyze --file output/article.md --keywords "IA,marketing"
```

## Utilisation Python

```python
import asyncio
from src.agent.writer import CopywritingAgent

agent = CopywritingAgent()

result = asyncio.run(agent.write(
    topic="Comment l'IA transforme le marketing",
    content_type="blog",
    persona="blog_casual",
    keywords=["IA", "marketing"],
    word_count=1200,
))

print(result["content"])
print(f"SEO: {result['analysis']['seo_score']}/100")
```

## Pipeline de rédaction

Chaque contenu passe par 5 étapes :

| Étape | Description |
|-------|-------------|
| **Research** | Collecte d'informations, identification des angles et données clés |
| **Outline** | Construction du plan structuré avec distribution des mots |
| **Draft** | Rédaction du premier brouillon complet |
| **Edit** | Révision : clarté, flow, engagement, précision, ton |
| **Polish** | Finalisation SEO, formatage, métadonnées |

## Personas disponibles

| Persona | Ton | Audience |
|---------|-----|----------|
| `expert_b2b` | Professionnel, factuel | Décideurs, managers |
| `blog_casual` | Conversationnel, amical | Grand public |
| `storyteller` | Immersif, captivant | Lecteurs en quête d'inspiration |
| `seo_specialist` | Informatif, structuré | Lecteurs web + moteurs de recherche |
| `thought_leader` | Visionnaire, inspirant | Professionnels, innovateurs |
| `technical_writer` | Précis, pédagogique | Développeurs, ingénieurs |

## Outils d'analyse intégrés

- **SEO Analyzer** : Score sur 100 (titre, structure H2/H3, densité mots-clés, meta description, longueur)
- **Readability Analyzer** : Score de lisibilité (longueur des phrases, vocabulaire, structure)
- **Keyword Extractor** : Extraction automatique, bigrammes, analyse de densité

## Tests

```bash
pip install -e ".[dev]"
pytest
```

## Configuration

Éditer `config/settings.yaml` pour personnaliser les paramètres par défaut (modèle LLM, langue, seuils SEO, etc.).
