"""
Pipeline de rédaction - Le coeur du processus d'écriture.

Le pipeline orchestre les 5 étapes de la rédaction :
1. Research  - Collecte et analyse des informations sur le sujet
2. Outline   - Construction du plan et de la structure
3. Draft     - Rédaction du premier brouillon
4. Edit      - Révision, amélioration et correction
5. Polish    - Finalisation, formatage et optimisation SEO
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from .personas import Persona


class PipelineStage(Enum):
    """Étapes du pipeline de rédaction."""

    RESEARCH = "research"
    OUTLINE = "outline"
    DRAFT = "draft"
    EDIT = "edit"
    POLISH = "polish"


@dataclass
class ContentBrief:
    """Brief de contenu - les instructions initiales pour la rédaction."""

    topic: str
    content_type: str  # "article", "blog", "usecase"
    persona: str  # nom de la persona à utiliser
    target_keywords: list[str] = field(default_factory=list)
    target_word_count: int = 1500
    language: str = "fr"
    additional_instructions: str = ""
    reference_urls: list[str] = field(default_factory=list)
    target_audience: str = ""


@dataclass
class PipelineState:
    """État courant du pipeline à travers les étapes."""

    brief: ContentBrief
    current_stage: PipelineStage = PipelineStage.RESEARCH
    research_notes: str = ""
    outline: str = ""
    draft: str = ""
    edited_content: str = ""
    final_content: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    seo_analysis: dict[str, Any] = field(default_factory=dict)
    revision_notes: list[str] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return self.current_stage == PipelineStage.POLISH and bool(self.final_content)


class WritingPipeline:
    """Pipeline de rédaction orchestrant les 5 étapes de création de contenu."""

    def __init__(self, llm_client: Any = None):
        """
        Args:
            llm_client: Client LLM (Anthropic, OpenAI, etc.) pour la génération.
        """
        self.llm_client = llm_client
        self.state: PipelineState | None = None

    def create_session(self, brief: ContentBrief) -> PipelineState:
        """Crée une nouvelle session de rédaction."""
        self.state = PipelineState(brief=brief)
        return self.state

    STAGE_NAMES = {
        PipelineStage.RESEARCH: "Recherche",
        PipelineStage.OUTLINE: "Plan",
        PipelineStage.DRAFT: "Rédaction",
        PipelineStage.EDIT: "Révision",
        PipelineStage.POLISH: "Finalisation",
    }

    async def run_full_pipeline(
        self,
        brief: ContentBrief,
        on_stage_complete: Callable[[dict], None] | None = None,
    ) -> PipelineState:
        """Exécute le pipeline complet de bout en bout."""
        self.create_session(brief)

        stages = [
            (PipelineStage.RESEARCH, self.research),
            (PipelineStage.OUTLINE, self.outline),
            (PipelineStage.DRAFT, self.draft),
            (PipelineStage.EDIT, self.edit),
            (PipelineStage.POLISH, self.polish),
        ]
        total = len(stages)
        pipeline_start = time.time()

        for i, (stage_enum, stage_fn) in enumerate(stages):
            stage_start = time.time()
            await stage_fn()
            stage_duration = time.time() - stage_start

            if on_stage_complete:
                on_stage_complete({
                    "stage": self.STAGE_NAMES[stage_enum],
                    "stage_index": i,
                    "total_stages": total,
                    "stage_duration": round(stage_duration, 1),
                    "elapsed": round(time.time() - pipeline_start, 1),
                })

        return self.state

    async def research(self) -> str:
        """Étape 1: Recherche et collecte d'informations."""
        self._ensure_state()
        self.state.current_stage = PipelineStage.RESEARCH

        prompt = self._build_research_prompt()
        result = await self._call_llm(prompt)

        self.state.research_notes = result
        return result

    async def outline(self) -> str:
        """Étape 2: Construction du plan structuré."""
        self._ensure_state()
        self.state.current_stage = PipelineStage.OUTLINE

        prompt = self._build_outline_prompt()
        result = await self._call_llm(prompt)

        self.state.outline = result
        return result

    async def draft(self) -> str:
        """Étape 3: Rédaction du premier brouillon."""
        self._ensure_state()
        self.state.current_stage = PipelineStage.DRAFT

        prompt = self._build_draft_prompt()
        result = await self._call_llm(prompt)

        self.state.draft = result
        return result

    async def edit(self) -> str:
        """Étape 4: Révision et amélioration."""
        self._ensure_state()
        self.state.current_stage = PipelineStage.EDIT

        prompt = self._build_edit_prompt()
        result = await self._call_llm(prompt)

        self.state.edited_content = result
        return result

    async def polish(self) -> str:
        """Étape 5: Finalisation et optimisation."""
        self._ensure_state()
        self.state.current_stage = PipelineStage.POLISH

        prompt = self._build_polish_prompt()
        result = await self._call_llm(prompt)

        self.state.final_content = result
        return result

    # --- Construction des prompts ---

    def _build_research_prompt(self) -> str:
        brief = self.state.brief
        keywords = ", ".join(brief.target_keywords) if brief.target_keywords else "à déterminer"

        return f"""Tu es un chercheur expert chargé de préparer un brief de recherche.

**Sujet:** {brief.topic}
**Type de contenu:** {brief.content_type}
**Langue:** {brief.language}
**Mots-clés cibles:** {keywords}
**Audience cible:** {brief.target_audience or "à définir selon le sujet"}

**Instructions supplémentaires:** {brief.additional_instructions}

Produis un résumé de recherche structuré contenant:
1. **Contexte** - Pourquoi ce sujet est pertinent maintenant
2. **Points clés** - Les 5-7 informations essentielles à couvrir
3. **Données et statistiques** - Chiffres importants à inclure
4. **Angle unique** - Quelle perspective originale adopter
5. **Questions fréquentes** - Ce que l'audience veut savoir
6. **Sources potentielles** - Types de sources à référencer"""

    def _build_outline_prompt(self) -> str:
        brief = self.state.brief

        return f"""Tu es un architecte de contenu expert.

**Sujet:** {brief.topic}
**Type de contenu:** {brief.content_type}
**Nombre de mots cible:** {brief.target_word_count}
**Recherche effectuée:**
{self.state.research_notes}

Crée un plan détaillé avec:
1. **Titre principal** (accrocheur, optimisé SEO)
2. **Meta description** (150-160 caractères)
3. **Introduction** - Accroche + problématique + promesse de valeur
4. **Corps** - Sections avec sous-titres H2/H3, points à couvrir par section
5. **Conclusion** - Résumé + appel à l'action
6. **Distribution de mots** - Nombre de mots estimé par section"""

    def _build_draft_prompt(self) -> str:
        brief = self.state.brief
        keywords = ", ".join(brief.target_keywords) if brief.target_keywords else "aucun spécifié"

        return f"""Tu es un rédacteur professionnel expert en {brief.content_type}.

**Plan à suivre:**
{self.state.outline}

**Recherche de référence:**
{self.state.research_notes}

**Mots-clés à intégrer naturellement:** {keywords}
**Nombre de mots cible:** {brief.target_word_count}
**Langue:** {brief.language}

Rédige le contenu complet en suivant strictement le plan.
Le texte doit être fluide, engageant et apporter une vraie valeur au lecteur.
Formate en Markdown avec les titres H1, H2, H3 appropriés."""

    def _build_edit_prompt(self) -> str:
        return f"""Tu es un éditeur professionnel exigeant.

**Brouillon à réviser:**
{self.state.draft}

Révise le contenu en vérifiant:
1. **Clarté** - Chaque phrase est-elle claire et nécessaire?
2. **Flow** - Les transitions entre sections sont-elles fluides?
3. **Engagement** - Le lecteur est-il captivé du début à la fin?
4. **Précision** - Les informations sont-elles exactes et sourcées?
5. **Ton** - Le ton est-il cohérent tout au long du texte?
6. **Grammaire** - Orthographe, grammaire, ponctuation impeccables?
7. **Longueur** - Le texte atteint-il le nombre de mots cible?

Produis la version révisée complète avec tes améliorations intégrées.
Ajoute en fin de document une section "## Notes de révision" listant les changements effectués."""

    def _build_polish_prompt(self) -> str:
        brief = self.state.brief
        keywords = ", ".join(brief.target_keywords) if brief.target_keywords else "aucun spécifié"

        return f"""Tu es un expert en finalisation de contenu et SEO.

**Contenu révisé:**
{self.state.edited_content}

**Mots-clés cibles:** {keywords}

Finalise le contenu en:
1. **Optimisant le SEO** - Titres, meta, densité de mots-clés, structure
2. **Ajoutant les éléments manquants** - Résumé TL;DR, CTA final
3. **Formatant proprement** - Markdown propre, listes, mise en forme
4. **Vérifiant la cohérence** - Ton, style, message global

Produis le contenu final prêt à publier en Markdown.
Ajoute en fin un bloc de métadonnées YAML avec:
- title, description, keywords, word_count, reading_time"""

    # --- Helpers ---

    def _ensure_state(self):
        if self.state is None:
            raise RuntimeError("Aucune session active. Appelez create_session() d'abord.")

    async def _call_llm(self, prompt: str) -> str:
        """Appelle le LLM via l'interface unifiée .generate()."""
        if self.llm_client is None:
            return f"[LLM non configuré - Prompt généré]\n\n{prompt}"

        # Interface unifiée : tous les clients exposent .generate(prompt)
        if hasattr(self.llm_client, "generate"):
            return self.llm_client.generate(prompt)

        raise ValueError(
            "Client LLM non supporté. Utilisez un client de src.agent.llm_clients "
            "(OllamaClient, AnthropicClient, OpenAIClient)."
        )
