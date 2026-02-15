"""
CopywritingAgent - Agent principal de rédaction.

Point d'entrée central qui coordonne le pipeline, les personas,
les templates et les outils d'analyse pour produire du contenu de qualité.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .personas import Persona, get_persona, list_personas
from .pipeline import ContentBrief, PipelineStage, PipelineState, WritingPipeline
from ..templates import ArticleTemplate, BlogTemplate, UseCaseTemplate
from ..tools.seo import SEOAnalyzer
from ..tools.readability import ReadabilityAnalyzer
from ..tools.keywords import KeywordExtractor


class CopywritingAgent:
    """Agent de copywriting orchestrant la création de contenu."""

    CONTENT_TYPES = {
        "article": ArticleTemplate,
        "blog": BlogTemplate,
        "usecase": UseCaseTemplate,
    }

    def __init__(self, llm_client: Any = None, output_dir: str = "output"):
        """
        Args:
            llm_client: Client LLM (Anthropic, OpenAI, etc.)
            output_dir: Répertoire de sortie pour les contenus générés.
        """
        self.llm_client = llm_client
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.pipeline = WritingPipeline(llm_client=llm_client)
        self.seo = SEOAnalyzer()
        self.readability = ReadabilityAnalyzer()
        self.keywords = KeywordExtractor()

    async def write(
        self,
        topic: str,
        content_type: str = "article",
        persona: str = "expert_b2b",
        keywords: list[str] | None = None,
        word_count: int = 1500,
        language: str = "fr",
        instructions: str = "",
        save: bool = True,
        progress_callback=None,
    ) -> dict[str, Any]:
        """
        Génère un contenu complet via le pipeline.

        Args:
            topic: Sujet du contenu.
            content_type: Type de contenu ("article", "blog", "usecase").
            persona: Nom de la persona à utiliser.
            keywords: Mots-clés cibles pour le SEO.
            word_count: Nombre de mots cible.
            language: Langue du contenu.
            instructions: Instructions supplémentaires.
            save: Sauvegarder automatiquement le résultat.

        Returns:
            Dictionnaire avec le contenu final et les métadonnées.
        """
        # Validation
        if content_type not in self.CONTENT_TYPES:
            available = ", ".join(self.CONTENT_TYPES.keys())
            raise ValueError(f"Type '{content_type}' inconnu. Disponibles: {available}")

        selected_persona = get_persona(persona)

        # Créer le brief
        brief = ContentBrief(
            topic=topic,
            content_type=content_type,
            persona=persona,
            target_keywords=keywords or [],
            target_word_count=word_count,
            language=language,
            additional_instructions=self._enrich_instructions(
                instructions, selected_persona, content_type
            ),
        )

        # Exécuter le pipeline
        state = await self.pipeline.run_full_pipeline(
            brief, on_stage_complete=progress_callback
        )

        # Analyser le résultat
        analysis = self._analyze_content(state.final_content, keywords or [])

        # Construire le résultat
        result = {
            "content": state.final_content,
            "metadata": {
                "topic": topic,
                "content_type": content_type,
                "persona": persona,
                "language": language,
                "word_count": analysis.get("word_count", 0),
                "reading_time_minutes": analysis.get("reading_time", 0),
                "seo_score": analysis.get("seo_score", 0),
                "readability_score": analysis.get("readability_score", 0),
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
            "pipeline_state": {
                "research_notes": state.research_notes,
                "outline": state.outline,
                "draft_length": len(state.draft),
                "revision_notes": state.revision_notes,
            },
            "analysis": analysis,
        }

        if save:
            filepath = self._save_content(result)
            result["saved_to"] = str(filepath)

        return result

    def _enrich_instructions(
        self, base_instructions: str, persona: Persona, content_type: str
    ) -> str:
        """Enrichit les instructions avec le contexte de la persona et du template."""
        template_class = self.CONTENT_TYPES[content_type]
        template = template_class()
        template_context = template.get_structure_guide()

        parts = [
            persona.to_prompt_context(),
            f"\n## Structure du contenu ({content_type}):\n{template_context}",
        ]

        if base_instructions:
            parts.append(f"\n## Instructions spécifiques:\n{base_instructions}")

        return "\n\n".join(parts)

    def _analyze_content(self, content: str, keywords: list[str]) -> dict[str, Any]:
        """Analyse le contenu final avec tous les outils disponibles."""
        words = content.split()
        word_count = len(words)

        analysis = {
            "word_count": word_count,
            "reading_time": max(1, round(word_count / 250)),
            "seo_score": self.seo.analyze(content, keywords),
            "readability_score": self.readability.analyze(content),
            "keyword_density": self.keywords.analyze_density(content, keywords),
        }

        return analysis

    def _save_content(self, result: dict[str, Any]) -> Path:
        """Sauvegarde le contenu et les métadonnées."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        slug = result["metadata"]["topic"][:50].lower().replace(" ", "-")
        slug = "".join(c for c in slug if c.isalnum() or c == "-")

        # Sauvegarder le contenu Markdown
        content_path = self.output_dir / f"{timestamp}_{slug}.md"
        content_path.write_text(result["content"], encoding="utf-8")

        # Sauvegarder les métadonnées JSON
        meta_path = self.output_dir / f"{timestamp}_{slug}_meta.json"
        meta = {k: v for k, v in result.items() if k != "content"}
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

        return content_path

    @staticmethod
    def list_personas() -> list[str]:
        """Liste les personas disponibles."""
        return list_personas()

    @staticmethod
    def list_content_types() -> list[str]:
        """Liste les types de contenu supportés."""
        return ["article", "blog", "usecase"]

    def get_persona_details(self, name: str) -> dict:
        """Retourne les détails d'une persona."""
        persona = get_persona(name)
        return {
            "name": persona.name,
            "description": persona.description,
            "tone": persona.tone,
            "style": persona.style,
            "language_level": persona.language_level,
            "target_audience": persona.target_audience,
        }
