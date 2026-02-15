#!/usr/bin/env python3
"""
Serveur web pour l'interface de copywriting.

Serveur léger basé sur http.server (stdlib Python, zéro dépendance).
Lance l'interface HTML et expose une API JSON pour la génération de contenu.

Usage:
    python web/server.py
    python web/server.py --port 8080
    python web/server.py --provider ollama --model mistral
"""

import argparse
import asyncio
import json
import os
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.agent.writer import CopywritingAgent
from src.agent.personas import PERSONAS
from src.agent.llm_clients import (
    OllamaClient,
    LLMConfig,
    create_llm_client,
    auto_detect_client,
)
from src.tools.seo import SEOAnalyzer
from src.tools.readability import ReadabilityAnalyzer
from src.tools.keywords import KeywordExtractor

# Client LLM global (configuré au démarrage)
LLM_CLIENT = None
PROVIDER_NAME = None


class CopywritingHandler(SimpleHTTPRequestHandler):
    """Handler HTTP pour l'interface web et l'API."""

    def __init__(self, *args, **kwargs):
        # Servir les fichiers depuis le répertoire web/
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

    def do_GET(self):
        """Gère les requêtes GET."""
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.path = "/index.html"
            return super().do_GET()

        if parsed.path == "/api/personas":
            return self._json_response(self._get_personas())

        if parsed.path == "/api/status":
            return self._json_response(self._get_status())

        if parsed.path == "/api/models":
            return self._json_response(self._get_models())

        return super().do_GET()

    def do_POST(self):
        """Gère les requêtes POST (API)."""
        parsed = urlparse(self.path)

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return self._json_response({"error": "JSON invalide"}, status=400)

        if parsed.path == "/api/write":
            return self._handle_write(data)

        if parsed.path == "/api/analyze":
            return self._handle_analyze(data)

        self._json_response({"error": "Endpoint inconnu"}, status=404)

    def _handle_write(self, data):
        """Génère du contenu via le pipeline."""
        topic = data.get("topic", "").strip()
        if not topic:
            return self._json_response({"error": "Le sujet est requis"}, status=400)

        content_type = data.get("content_type", "article")
        persona = data.get("persona", "expert_b2b")
        keywords = [k.strip() for k in data.get("keywords", "").split(",") if k.strip()]
        word_count = int(data.get("word_count", 1500))
        language = data.get("language", "fr")
        instructions = data.get("instructions", "")

        agent = CopywritingAgent(llm_client=LLM_CLIENT, output_dir=str(ROOT_DIR / "output"))

        try:
            result = asyncio.run(agent.write(
                topic=topic,
                content_type=content_type,
                persona=persona,
                keywords=keywords,
                word_count=word_count,
                language=language,
                instructions=instructions,
                save=True,
            ))
            return self._json_response(result)
        except Exception as e:
            return self._json_response({"error": str(e)}, status=500)

    def _handle_analyze(self, data):
        """Analyse un contenu."""
        content = data.get("content", "").strip()
        if not content:
            return self._json_response({"error": "Le contenu est requis"}, status=400)

        keywords = [k.strip() for k in data.get("keywords", "").split(",") if k.strip()]

        seo = SEOAnalyzer()
        readability = ReadabilityAnalyzer()
        kw_extractor = KeywordExtractor()

        seo_score = seo.analyze(content, keywords)
        seo_checks = seo.run_checks(content, keywords)
        read_report = readability.get_detailed_report(content)
        top_keywords = kw_extractor.extract_keywords(content, top_n=10)
        density = kw_extractor.analyze_density(content, keywords) if keywords else {}

        result = {
            "seo_score": seo_score,
            "seo_checks": seo_checks,
            "readability": read_report,
            "top_keywords": [{"word": w, "count": c} for w, c in top_keywords],
            "keyword_density": density,
        }
        return self._json_response(result)

    def _get_personas(self):
        """Retourne la liste des personas."""
        return {
            key: {
                "name": p.name,
                "description": p.description,
                "tone": p.tone,
                "style": p.style,
                "target_audience": p.target_audience,
                "language_level": p.language_level,
            }
            for key, p in PERSONAS.items()
        }

    def _get_status(self):
        """Retourne le statut du serveur."""
        model_name = getattr(LLM_CLIENT, "model", "none") if LLM_CLIENT else "none"
        return {
            "provider": PROVIDER_NAME or "none",
            "model": model_name,
            "llm_available": LLM_CLIENT is not None,
            "content_types": ["article", "blog", "usecase"],
            "personas": list(PERSONAS.keys()),
        }

    def _get_models(self):
        """Retourne les modèles Ollama disponibles."""
        try:
            client = OllamaClient()
            if client.is_available():
                models = client.list_models()
                return {
                    "available": True,
                    "models": [
                        {
                            "name": m.get("name", "?"),
                            "size_gb": round(m.get("size", 0) / (1024**3), 1),
                        }
                        for m in models
                    ],
                }
        except Exception:
            pass
        return {"available": False, "models": []}

    def _json_response(self, data, status=200):
        """Envoie une réponse JSON."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode("utf-8"))

    def do_OPTIONS(self):
        """CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """Log minimaliste."""
        if "/api/" in (args[0] if args else ""):
            print(f"  API: {args[0]}")


def main():
    parser = argparse.ArgumentParser(description="Interface web Copywriting Agent")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--provider", choices=["ollama", "anthropic", "openai", "auto"],
                        default="auto", help="Provider LLM")
    parser.add_argument("--model", default="", help="Modèle LLM")
    parser.add_argument("--ollama-url", default="http://localhost:11434", help="URL Ollama")
    args = parser.parse_args()

    # Configurer le client LLM
    global LLM_CLIENT, PROVIDER_NAME

    if args.provider == "auto":
        LLM_CLIENT, PROVIDER_NAME = auto_detect_client()
    else:
        default_models = {"ollama": "llama3.1", "anthropic": "claude-sonnet-4-20250514", "openai": "gpt-4"}
        model = args.model or default_models.get(args.provider, "")
        config = LLMConfig(
            provider=args.provider,
            model=model,
            base_url=args.ollama_url if args.provider == "ollama" else "",
            api_key=os.environ.get(
                "ANTHROPIC_API_KEY" if args.provider == "anthropic" else "OPENAI_API_KEY", ""
            ),
        )
        try:
            LLM_CLIENT = create_llm_client(config)
            PROVIDER_NAME = args.provider
        except (ValueError, ImportError) as e:
            print(f"Warning: {e}")

    model_name = getattr(LLM_CLIENT, "model", "none") if LLM_CLIENT else "none"

    server = HTTPServer(("0.0.0.0", args.port), CopywritingHandler)

    print(f"""
╔══════════════════════════════════════════════════╗
║         Copywriting Agent — Interface Web        ║
╠══════════════════════════════════════════════════╣
║  URL:      http://localhost:{str(args.port):<21s}  ║
║  Provider: {(PROVIDER_NAME or 'aucun'):<37s}  ║
║  Modèle:   {model_name:<37s}  ║
╚══════════════════════════════════════════════════╝
""")

    if LLM_CLIENT is None:
        print("  Aucun LLM détecté. Le mode dry-run sera utilisé.")
        print("  Pour activer Ollama : ollama serve && ollama pull mistral\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServeur arrêté.")
        server.server_close()


if __name__ == "__main__":
    main()
