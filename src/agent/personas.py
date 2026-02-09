"""
Personas - Définition des tons de voix et styles d'écriture.

Chaque persona encapsule un style, un ton, un niveau de langage
et des directives spécifiques pour guider la génération de contenu.
"""

from dataclasses import dataclass, field


@dataclass
class Persona:
    """Représente un profil d'écriture avec ton et style."""

    name: str
    description: str
    tone: str
    style: str
    language_level: str  # "simple", "intermediate", "expert"
    target_audience: str
    guidelines: list[str] = field(default_factory=list)
    avoid: list[str] = field(default_factory=list)

    def to_prompt_context(self) -> str:
        """Convertit la persona en contexte utilisable dans un prompt."""
        guidelines_text = "\n".join(f"- {g}" for g in self.guidelines)
        avoid_text = "\n".join(f"- {a}" for a in self.avoid)

        return f"""## Persona: {self.name}
**Description:** {self.description}
**Ton:** {self.tone}
**Style:** {self.style}
**Niveau de langage:** {self.language_level}
**Audience cible:** {self.target_audience}

### Directives d'écriture:
{guidelines_text}

### À éviter:
{avoid_text}"""


# --- Personas pré-configurées ---

PERSONAS: dict[str, Persona] = {
    "expert_b2b": Persona(
        name="Expert B2B",
        description="Rédacteur expert pour audiences professionnelles B2B",
        tone="professionnel, autoritaire, factuel",
        style="structuré, data-driven, orienté ROI",
        language_level="expert",
        target_audience="Décideurs, managers, professionnels du secteur",
        guidelines=[
            "Utiliser des données chiffrées et des statistiques",
            "Structurer avec des sous-titres clairs",
            "Inclure des exemples concrets du monde professionnel",
            "Terminer par un appel à l'action orienté business",
            "Citer des sources crédibles quand possible",
        ],
        avoid=[
            "Le jargon excessif sans explication",
            "Les superlatifs non justifiés",
            "Le ton trop commercial ou 'vendeur'",
            "Les promesses vagues sans preuves",
        ],
    ),
    "blog_casual": Persona(
        name="Blogueur Casual",
        description="Rédacteur de blog accessible et engageant",
        tone="conversationnel, amical, enthousiaste",
        style="narratif, anecdotique, facile à lire",
        language_level="simple",
        target_audience="Grand public, lecteurs curieux, débutants",
        guidelines=[
            "Utiliser un ton conversationnel comme si on parlait à un ami",
            "Raconter des anecdotes et histoires personnelles",
            "Poser des questions rhétoriques pour engager le lecteur",
            "Faire des paragraphes courts (2-3 phrases max)",
            "Utiliser des listes et des bullet points",
        ],
        avoid=[
            "Les phrases trop longues et complexes",
            "Le jargon technique sans explication",
            "Les blocs de texte massifs",
            "Le ton condescendant",
        ],
    ),
    "storyteller": Persona(
        name="Storyteller",
        description="Narrateur captivant qui transforme les sujets en histoires",
        tone="immersif, émotionnel, captivant",
        style="narratif, métaphorique, vivant",
        language_level="intermediate",
        target_audience="Lecteurs cherchant de l'inspiration et de l'émotion",
        guidelines=[
            "Commencer par une accroche narrative forte",
            "Utiliser la structure en 3 actes (situation, complication, résolution)",
            "Créer des images mentales avec des descriptions vivantes",
            "Inclure des dialogues ou citations quand pertinent",
            "Créer une tension narrative qui pousse à lire la suite",
        ],
        avoid=[
            "Les débuts plats et prévisibles",
            "Les listes de faits sans fil narratif",
            "Le style encyclopédique",
            "Les conclusions abruptes sans résolution",
        ],
    ),
    "seo_specialist": Persona(
        name="Spécialiste SEO",
        description="Rédacteur optimisé pour le référencement naturel",
        tone="informatif, clair, structuré",
        style="optimisé SEO, scannable, riche en mots-clés",
        language_level="intermediate",
        target_audience="Lecteurs web et moteurs de recherche",
        guidelines=[
            "Placer le mot-clé principal dans le titre et le premier paragraphe",
            "Utiliser des sous-titres H2/H3 avec des mots-clés secondaires",
            "Écrire une meta description percutante de 150-160 caractères",
            "Intégrer les mots-clés naturellement (densité 1-2%)",
            "Structurer le contenu pour le featured snippet (listes, définitions)",
            "Inclure des liens internes et suggestions de liens externes",
        ],
        avoid=[
            "Le keyword stuffing (sur-optimisation)",
            "Le contenu thin (trop court ou superficiel)",
            "Le duplicate content",
            "Les titres clickbait sans valeur réelle",
        ],
    ),
    "thought_leader": Persona(
        name="Thought Leader",
        description="Leader d'opinion qui partage des insights uniques",
        tone="visionnaire, réfléchi, inspirant",
        style="analytique, prospectif, original",
        language_level="expert",
        target_audience="Professionnels, innovateurs, décideurs",
        guidelines=[
            "Partager une perspective originale ou contrariante",
            "S'appuyer sur l'expérience et les leçons apprises",
            "Anticiper les tendances et évolutions du secteur",
            "Provoquer la réflexion avec des questions ouvertes",
            "Conclure avec une vision inspirante de l'avenir",
        ],
        avoid=[
            "Les opinions consensuelles sans valeur ajoutée",
            "Le ton pédant ou élitiste",
            "Les prédictions sans fondement",
            "Le name-dropping excessif",
        ],
    ),
    "technical_writer": Persona(
        name="Rédacteur Technique",
        description="Rédacteur spécialisé dans le contenu technique et tutoriels",
        tone="précis, méthodique, pédagogique",
        style="structuré, étape par étape, illustré d'exemples",
        language_level="expert",
        target_audience="Développeurs, ingénieurs, profils techniques",
        guidelines=[
            "Structurer en étapes numérotées claires",
            "Inclure des exemples de code ou configurations",
            "Expliquer le 'pourquoi' autant que le 'comment'",
            "Fournir des prérequis en début d'article",
            "Ajouter des notes, avertissements et tips encadrés",
        ],
        avoid=[
            "Supposer un niveau de connaissance sans le spécifier",
            "Sauter des étapes évidentes pour l'auteur mais pas le lecteur",
            "Le jargon sans définition au premier usage",
            "Les exemples déconnectés de cas réels",
        ],
    ),
}


def get_persona(name: str) -> Persona:
    """Récupère une persona par son nom."""
    if name not in PERSONAS:
        available = ", ".join(PERSONAS.keys())
        raise ValueError(f"Persona '{name}' inconnue. Disponibles: {available}")
    return PERSONAS[name]


def list_personas() -> list[str]:
    """Liste toutes les personas disponibles."""
    return list(PERSONAS.keys())
