#!/usr/bin/env python3
"""
Exemples d'utilisation du Copywriting Agent.

Ces exemples montrent comment utiliser l'agent en tant que bibliothèque Python.
Pour l'utilisation CLI, voir: python main.py --help
"""

import asyncio
from src.agent.writer import CopywritingAgent
from src.agent.personas import get_persona, list_personas
from src.tools.seo import SEOAnalyzer
from src.tools.readability import ReadabilityAnalyzer
from src.tools.keywords import KeywordExtractor


# ============================================================
# Exemple 1: Générer un article de blog
# ============================================================
async def example_blog_post():
    """Génère un article de blog sur l'IA."""
    agent = CopywritingAgent(output_dir="output")

    result = await agent.write(
        topic="Comment l'IA transforme le marketing digital en 2025",
        content_type="blog",
        persona="blog_casual",
        keywords=["IA marketing", "intelligence artificielle", "marketing digital"],
        word_count=1200,
        language="fr",
    )

    print(f"Blog généré: {result['metadata']['word_count']} mots")
    print(f"Score SEO: {result['analysis']['seo_score']}/100")
    print(f"Lisibilité: {result['analysis']['readability_score']}/100")


# ============================================================
# Exemple 2: Créer une étude de cas
# ============================================================
async def example_use_case():
    """Génère une étude de cas B2B."""
    agent = CopywritingAgent(output_dir="output")

    result = await agent.write(
        topic="Comment TechCorp a réduit ses coûts IT de 40% grâce à la migration cloud",
        content_type="usecase",
        persona="expert_b2b",
        keywords=["migration cloud", "réduction coûts", "cloud computing"],
        word_count=1800,
        instructions="Focus sur le ROI et les métriques concrètes. Le client est une PME de 200 employés.",
    )

    print(f"Use case généré: {result['metadata']['word_count']} mots")
    if "saved_to" in result:
        print(f"Fichier: {result['saved_to']}")


# ============================================================
# Exemple 3: Analyser un contenu existant
# ============================================================
def example_analyze_content():
    """Analyse un contenu Markdown existant."""
    content = """
# Comment booster votre productivité avec l'IA

L'intelligence artificielle révolutionne notre façon de travailler.
Dans cet article, découvrez comment tirer parti de l'IA pour gagner du temps.

## 1. Automatiser les tâches répétitives

L'IA excelle dans l'automatisation des tâches répétitives. Les outils comme
ChatGPT ou Claude permettent de générer des emails, résumer des documents
et organiser vos données en quelques secondes.

## 2. Améliorer la prise de décision

Grâce à l'analyse de données, l'IA vous aide à prendre de meilleures décisions.
Les tableaux de bord intelligents identifient les tendances que l'oeil humain
pourrait manquer.

## 3. Personnaliser l'expérience client

L'IA permet de personnaliser chaque interaction client à grande échelle.
Les recommandations produits, les chatbots et les emails personnalisés
augmentent la satisfaction et la conversion.

## Conclusion

L'IA n'est plus un luxe mais une nécessité. Commencez petit, expérimentez,
et vous verrez rapidement des résultats concrets.
"""

    keywords = ["IA", "productivité", "intelligence artificielle"]

    # Analyse SEO
    seo = SEOAnalyzer()
    seo_score = seo.analyze(content, keywords)
    seo_details = seo.run_checks(content, keywords)

    print(f"Score SEO: {seo_score}/100")
    for check_name, check in seo_details.items():
        print(f"  [{check['status']}] {check_name}: {check['message']}")

    # Analyse lisibilité
    readability = ReadabilityAnalyzer()
    report = readability.get_detailed_report(content)
    print(f"\nLisibilité: {report['score']}/100")
    print(f"  Mots: {report['metrics']['total_words']}")
    print(f"  Phrases: {report['metrics']['total_sentences']}")

    # Extraction de mots-clés
    kw_extractor = KeywordExtractor()
    top_keywords = kw_extractor.extract_keywords(content, top_n=5)
    print(f"\nTop mots-clés:")
    for word, count in top_keywords:
        print(f"  {word} ({count}x)")

    # Densité
    density = kw_extractor.analyze_density(content, keywords)
    print(f"\nDensité mots-clés cibles:")
    for kw, data in density.items():
        print(f"  '{kw}': {data['density_percent']}% - {data['status']}")


# ============================================================
# Exemple 4: Explorer les personas
# ============================================================
def example_personas():
    """Affiche les détails de chaque persona."""
    print("=== Personas disponibles ===\n")
    for name in list_personas():
        persona = get_persona(name)
        print(f"--- {persona.name} ---")
        print(f"Ton: {persona.tone}")
        print(f"Style: {persona.style}")
        print(f"Audience: {persona.target_audience}")
        print()


# ============================================================
# Point d'entrée
# ============================================================
if __name__ == "__main__":
    print("=== Exemple: Analyse de contenu ===\n")
    example_analyze_content()

    print("\n=== Exemple: Personas ===\n")
    example_personas()

    # Pour les exemples async (nécessitent un client LLM configuré):
    # asyncio.run(example_blog_post())
    # asyncio.run(example_use_case())
