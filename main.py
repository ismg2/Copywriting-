#!/usr/bin/env python3
"""
Copywriting Agent - Point d'entrée CLI.

Usage:
    python main.py write --topic "Sujet" --type article --persona expert_b2b
    python main.py write --topic "Sujet" --provider ollama --model mistral
    python main.py list-personas
    python main.py list-types
    python main.py list-models
    python main.py analyze --file output/mon-article.md --keywords "mot1,mot2"
"""

import argparse
import asyncio
import json
import os
import sys

from src.agent.writer import CopywritingAgent
from src.agent.personas import PERSONAS
from src.agent.llm_clients import (
    LLMConfig,
    OllamaClient,
    create_llm_client,
    auto_detect_client,
)
from src.tools.seo import SEOAnalyzer
from src.tools.readability import ReadabilityAnalyzer
from src.tools.keywords import KeywordExtractor


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Agent de Copywriting IA - Générez des articles, blogs et use cases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Avec Ollama (local, sans clé API)
  %(prog)s write --topic "L'IA dans le marketing" --provider ollama --model mistral
  %(prog)s write --topic "Guide SEO" -T blog --provider ollama --model llama3.1

  # Avec Anthropic / OpenAI
  %(prog)s write --topic "Migration cloud" --provider anthropic --model claude-sonnet-4-20250514
  %(prog)s write --topic "Migration cloud" --provider openai --model gpt-4

  # Auto-détection (Ollama > Anthropic > OpenAI)
  %(prog)s write --topic "L'IA dans le marketing" --type blog --persona blog_casual

  # Autres commandes
  %(prog)s list-models                          # Voir les modèles Ollama disponibles
  %(prog)s list-models --ollama-url http://server:11434
  %(prog)s list-personas
  %(prog)s analyze --file output/article.md --keywords "IA,marketing"
        """,
    )

    # Options globales LLM
    llm_group = parser.add_argument_group("LLM Provider")
    llm_group.add_argument(
        "--provider",
        choices=["ollama", "anthropic", "openai", "auto"],
        default="auto",
        help="Provider LLM (default: auto — détecte Ollama, puis Anthropic, puis OpenAI)",
    )
    llm_group.add_argument(
        "--model", "-m",
        default="",
        help="Modèle à utiliser (ex: mistral, llama3.1, claude-sonnet-4-20250514, gpt-4)",
    )
    llm_group.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="URL du serveur Ollama (default: http://localhost:11434)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commande à exécuter")

    # --- Commande: write ---
    write_parser = subparsers.add_parser("write", help="Générer un nouveau contenu")
    write_parser.add_argument("--topic", "-t", required=True, help="Sujet du contenu")
    write_parser.add_argument(
        "--type",
        "-T",
        choices=["article", "blog", "usecase"],
        default="article",
        help="Type de contenu (default: article)",
    )
    write_parser.add_argument(
        "--persona",
        "-p",
        choices=list(PERSONAS.keys()),
        default="expert_b2b",
        help="Persona/ton à utiliser (default: expert_b2b)",
    )
    write_parser.add_argument(
        "--keywords",
        "-k",
        default="",
        help="Mots-clés SEO séparés par des virgules",
    )
    write_parser.add_argument(
        "--words",
        "-w",
        type=int,
        default=1500,
        help="Nombre de mots cible (default: 1500)",
    )
    write_parser.add_argument(
        "--language",
        "-l",
        default="fr",
        help="Langue du contenu (default: fr)",
    )
    write_parser.add_argument(
        "--instructions",
        "-i",
        default="",
        help="Instructions supplémentaires",
    )
    write_parser.add_argument(
        "--no-save",
        action="store_true",
        help="Ne pas sauvegarder automatiquement",
    )
    write_parser.add_argument(
        "--output-dir",
        "-o",
        default="output",
        help="Répertoire de sortie (default: output)",
    )

    # --- Commande: list-personas ---
    subparsers.add_parser("list-personas", help="Lister les personas disponibles")

    # --- Commande: list-types ---
    subparsers.add_parser("list-types", help="Lister les types de contenu")

    # --- Commande: list-models ---
    subparsers.add_parser("list-models", help="Lister les modèles Ollama disponibles")

    # --- Commande: analyze ---
    analyze_parser = subparsers.add_parser("analyze", help="Analyser un contenu existant")
    analyze_parser.add_argument("--file", "-f", required=True, help="Fichier Markdown à analyser")
    analyze_parser.add_argument(
        "--keywords",
        "-k",
        default="",
        help="Mots-clés à vérifier (séparés par des virgules)",
    )

    return parser


def cmd_list_personas():
    """Affiche les personas disponibles."""
    print("\n=== Personas disponibles ===\n")
    for key, persona in PERSONAS.items():
        print(f"  {key:20s} | {persona.name}")
        print(f"  {'':20s} | Ton: {persona.tone}")
        print(f"  {'':20s} | Audience: {persona.target_audience}")
        print()


def cmd_list_types():
    """Affiche les types de contenu disponibles."""
    print("\n=== Types de contenu ===\n")
    types = {
        "article": "Article de fond - Analyse approfondie, opinion, guide expert",
        "blog": "Blog Post - Contenu conversationnel et engageant",
        "usecase": "Use Case - Étude de cas format Problème → Solution → Résultat",
    }
    for key, desc in types.items():
        print(f"  {key:10s} | {desc}")
    print()


def cmd_list_models(args):
    """Liste les modèles disponibles dans Ollama."""
    client = OllamaClient(base_url=args.ollama_url)

    print(f"\n=== Modèles Ollama ({args.ollama_url}) ===\n")

    if not client.is_available():
        print("  Ollama n'est pas accessible.")
        print(f"  Vérifiez qu'Ollama est lancé : ollama serve")
        print(f"  URL testée : {args.ollama_url}")
        print()
        sys.exit(1)

    try:
        models = client.list_models()
    except ConnectionError as e:
        print(f"  Erreur: {e}")
        sys.exit(1)

    if not models:
        print("  Aucun modèle installé.")
        print("  Installez un modèle : ollama pull llama3.1")
        print()
        return

    for model in models:
        name = model.get("name", "?")
        size = model.get("size", 0)
        size_gb = size / (1024 ** 3) if size else 0
        modified = model.get("modified_at", "")[:10]
        print(f"  {name:30s}  {size_gb:5.1f} GB  {modified}")

    print(f"\n  Total: {len(models)} modèle(s)")
    print(f"\n  Usage: python main.py --provider ollama --model <nom> write -t \"Sujet\"")
    print()


def cmd_analyze(args):
    """Analyse un contenu existant."""
    try:
        with open(args.file, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur: fichier '{args.file}' non trouvé.")
        sys.exit(1)

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    seo = SEOAnalyzer()
    readability = ReadabilityAnalyzer()
    kw_extractor = KeywordExtractor()

    print(f"\n=== Analyse de {args.file} ===\n")

    # SEO
    seo_score = seo.analyze(content, keywords)
    seo_checks = seo.run_checks(content, keywords)
    print(f"Score SEO: {seo_score}/100")
    for name, check in seo_checks.items():
        status_icon = {"pass": "+", "warn": "~", "fail": "!", "info": "i"}.get(check["status"], "?")
        print(f"  [{status_icon}] {name}: {check['message']}")

    # Lisibilité
    read_report = readability.get_detailed_report(content)
    print(f"\nScore Lisibilité: {read_report['score']}/100")
    metrics = read_report["metrics"]
    print(f"  Mots: {metrics['total_words']} | Phrases: {metrics['total_sentences']}")
    print(f"  Moy. mots/phrase: {metrics['avg_sentence_length']} | Moy. lettres/mot: {metrics['avg_word_length']}")
    print(f"  Richesse vocabulaire: {metrics['vocabulary_richness']}%")

    if read_report["recommendations"]:
        print("\n  Recommandations:")
        for rec in read_report["recommendations"]:
            print(f"    - {rec}")

    # Mots-clés
    if keywords:
        print(f"\nDensité des mots-clés cibles:")
        density = kw_extractor.analyze_density(content, keywords)
        for kw, data in density.items():
            print(f"  '{kw}': {data['density_percent']}% ({data['count']}x) - {data['status']}")

    # Top mots-clés extraits
    top_kw = kw_extractor.extract_keywords(content, top_n=10)
    print(f"\nTop 10 mots-clés du contenu:")
    for word, count in top_kw:
        print(f"  {word:20s} ({count}x)")

    print()


def _resolve_llm_client(args):
    """Résout le client LLM selon les arguments CLI."""
    provider = args.provider

    # Mode auto-détection
    if provider == "auto":
        client, detected = auto_detect_client()
        return client, detected

    # Déterminer le modèle par défaut selon le provider
    default_models = {
        "ollama": "llama3.1",
        "anthropic": "claude-sonnet-4-20250514",
        "openai": "gpt-4",
    }
    model = args.model or default_models.get(provider, "")

    config = LLMConfig(
        provider=provider,
        model=model,
        base_url=args.ollama_url if provider == "ollama" else "",
        api_key=os.environ.get(
            "ANTHROPIC_API_KEY" if provider == "anthropic" else "OPENAI_API_KEY", ""
        ),
    )

    try:
        client = create_llm_client(config)
        return client, provider
    except (ValueError, ImportError) as e:
        print(f"Erreur: {e}")
        return None, None


async def cmd_write(args):
    """Génère un nouveau contenu."""
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    # Résoudre le client LLM
    llm_client, provider_name = _resolve_llm_client(args)

    agent = CopywritingAgent(llm_client=llm_client, output_dir=args.output_dir)

    model_name = getattr(llm_client, "model", "?") if llm_client else "none"

    print(f"\n=== Génération de contenu ===")
    print(f"  Sujet: {args.topic}")
    print(f"  Type: {args.type}")
    print(f"  Persona: {args.persona}")
    print(f"  Mots-clés: {keywords or 'aucun'}")
    print(f"  Mots cible: {args.words}")
    print(f"  Langue: {args.language}")
    print(f"  Provider: {provider_name or 'aucun'}")
    print(f"  Modèle: {model_name}")
    print()

    if llm_client is None:
        print("Aucun LLM détecté. Options :")
        print("  1. Lancez Ollama : ollama serve  (puis ollama pull llama3.1)")
        print("  2. Ou : export ANTHROPIC_API_KEY=sk-ant-...")
        print("  3. Ou : export OPENAI_API_KEY=sk-...")
        print("Le pipeline sera exécuté en mode 'dry run'.\n")

    result = await agent.write(
        topic=args.topic,
        content_type=args.type,
        persona=args.persona,
        keywords=keywords,
        word_count=args.words,
        language=args.language,
        instructions=args.instructions,
        save=not args.no_save,
    )

    # Afficher le résultat
    print("--- Contenu généré ---\n")
    print(result["content"][:2000])
    if len(result["content"]) > 2000:
        print(f"\n... [{len(result['content']) - 2000} caractères supplémentaires]")

    print("\n--- Métadonnées ---")
    print(json.dumps(result["metadata"], indent=2, ensure_ascii=False))

    if "saved_to" in result:
        print(f"\nSauvegardé dans: {result['saved_to']}")


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "list-personas":
        cmd_list_personas()
    elif args.command == "list-types":
        cmd_list_types()
    elif args.command == "list-models":
        cmd_list_models(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "write":
        asyncio.run(cmd_write(args))


if __name__ == "__main__":
    main()
