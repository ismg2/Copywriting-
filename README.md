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
git clone <repo-url>
cd Copywriting-
pip install -e ".[all]"
```

## Configuration LLM

3 options de provider, par ordre de priorité en mode auto :

### Option 1 : Ollama (local, gratuit, sans clé API)
```bash
ollama serve                    # Démarrer le serveur
ollama pull mistral             # Télécharger un modèle
python main.py list-models      # Vérifier les modèles disponibles
```

### Option 2 : Anthropic
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Option 3 : OpenAI
```bash
export OPENAI_API_KEY="sk-..."
```

## Utilisation CLI

```bash
# Avec Ollama (local, sans clé API)
python main.py --provider ollama --model mistral write -t "L'IA dans le marketing"
python main.py --provider ollama --model llama3.1 write -t "Guide SEO" -T blog

# Auto-détection (Ollama > Anthropic > OpenAI)
python main.py write -t "L'IA dans le marketing" -T blog -p blog_casual

# Lister les modèles Ollama
python main.py list-models

# Autres commandes
python main.py list-personas
python main.py analyze --file output/article.md --keywords "IA,marketing"
```

## Utilisation Python

```python
from src.agent.writer import CopywritingAgent
from src.agent.llm_clients import OllamaClient

client = OllamaClient(model="mistral")
agent = CopywritingAgent(llm_client=client)

import asyncio
result = asyncio.run(agent.write(
    topic="Comment l'IA transforme le marketing",
    content_type="blog",
    persona="blog_casual",
    keywords=["IA", "marketing"],
))

print(result["content"])
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
