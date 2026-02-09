"""
ArticleTemplate - Template pour articles de fond structurés.
"""

from .base import BaseTemplate, Section


class ArticleTemplate(BaseTemplate):
    """Template pour articles professionnels et éditoriaux."""

    @property
    def name(self) -> str:
        return "Article de fond"

    @property
    def description(self) -> str:
        return (
            "Structure complète pour articles approfondis : analyse, opinion, "
            "investigation ou guide expert."
        )

    def get_sections(self) -> list[Section]:
        return [
            Section(
                title="Titre et chapeau",
                description="Titre accrocheur (60-70 caractères) + chapeau résumant la valeur de l'article.",
                suggested_word_count=50,
                tips=[
                    "Le titre doit promettre un bénéfice clair",
                    "Le chapeau pose le problème et tease la solution",
                    "Inclure le mot-clé principal dans le titre",
                ],
            ),
            Section(
                title="Introduction",
                description="Accroche forte, contexte du sujet, annonce de la promesse de l'article.",
                suggested_word_count=150,
                subsections=[
                    Section(
                        title="Accroche",
                        description="Stat choc, question, anecdote ou déclaration audacieuse",
                        suggested_word_count=30,
                    ),
                    Section(
                        title="Contexte",
                        description="Pourquoi ce sujet est important maintenant",
                        suggested_word_count=60,
                    ),
                    Section(
                        title="Promesse",
                        description="Ce que le lecteur va apprendre/gagner",
                        suggested_word_count=60,
                    ),
                ],
                tips=["Ne pas dépasser 3 paragraphes pour l'intro"],
            ),
            Section(
                title="Corps principal - Section 1",
                description="Premier point majeur avec arguments, données et exemples.",
                suggested_word_count=400,
                tips=[
                    "Un argument principal par section",
                    "Soutenir avec des données chiffrées",
                    "Inclure au moins un exemple concret",
                ],
            ),
            Section(
                title="Corps principal - Section 2",
                description="Deuxième point majeur, approfondissement ou perspective différente.",
                suggested_word_count=400,
                tips=[
                    "Créer une transition fluide depuis la section précédente",
                    "Apporter une nouvelle perspective ou angle",
                ],
            ),
            Section(
                title="Corps principal - Section 3",
                description="Troisième point, implications pratiques ou cas d'usage.",
                suggested_word_count=350,
                tips=[
                    "Rendre actionnable pour le lecteur",
                    "Inclure des recommandations concrètes",
                ],
            ),
            Section(
                title="Conclusion",
                description="Synthèse des points clés, ouverture et appel à l'action.",
                suggested_word_count=150,
                subsections=[
                    Section(
                        title="Synthèse",
                        description="Résumé des 3 points principaux en 2-3 phrases",
                        suggested_word_count=60,
                    ),
                    Section(
                        title="Ouverture",
                        description="Perspective future ou question ouverte",
                        suggested_word_count=40,
                    ),
                    Section(
                        title="CTA",
                        description="Appel à l'action clair et pertinent",
                        suggested_word_count=50,
                    ),
                ],
            ),
        ]
