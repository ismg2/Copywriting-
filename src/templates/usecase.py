"""
UseCaseTemplate - Template pour études de cas et use cases.
"""

from .base import BaseTemplate, Section


class UseCaseTemplate(BaseTemplate):
    """Template pour études de cas client et use cases produit/service."""

    @property
    def name(self) -> str:
        return "Use Case / Étude de Cas"

    @property
    def description(self) -> str:
        return (
            "Structure pour études de cas : démontrer la valeur via un "
            "exemple concret avec le format Problème → Solution → Résultat."
        )

    def get_sections(self) -> list[Section]:
        return [
            Section(
                title="Titre et résumé exécutif",
                description="Titre orienté résultat + résumé en 3-4 phrases des points clés.",
                suggested_word_count=80,
                tips=[
                    "Format titre : '[Client/Secteur] : Comment [solution] a permis [résultat chiffré]'",
                    "Le résumé doit donner envie de lire mais aussi fonctionner seul",
                    "Inclure le chiffre clé du résultat dans le titre",
                ],
            ),
            Section(
                title="Fiche d'identité",
                description="Présentation rapide du client/projet : secteur, taille, contexte.",
                suggested_word_count=100,
                subsections=[
                    Section(
                        title="Le client",
                        description="Qui est le client, son secteur, sa taille",
                        suggested_word_count=40,
                    ),
                    Section(
                        title="Le contexte",
                        description="Situation de départ, marché, enjeux",
                        suggested_word_count=60,
                    ),
                ],
                tips=["Utiliser un format fiche / tableau pour la lisibilité"],
            ),
            Section(
                title="Le défi / Le problème",
                description="Description détaillée du problème ou défi rencontré.",
                suggested_word_count=250,
                subsections=[
                    Section(
                        title="Situation initiale",
                        description="Comment les choses fonctionnaient avant",
                        suggested_word_count=80,
                    ),
                    Section(
                        title="Points de douleur",
                        description="Les problèmes concrets et leur impact",
                        suggested_word_count=100,
                    ),
                    Section(
                        title="Enjeux",
                        description="Ce qui était en jeu (coûts, compétitivité, croissance)",
                        suggested_word_count=70,
                    ),
                ],
                tips=[
                    "Quantifier les problèmes quand possible (perte de X%, Y heures/semaine)",
                    "Rendre les défis universels pour que d'autres entreprises s'identifient",
                ],
            ),
            Section(
                title="La solution",
                description="Présentation de la solution mise en place, étape par étape.",
                suggested_word_count=350,
                subsections=[
                    Section(
                        title="Choix de la solution",
                        description="Pourquoi cette approche a été choisie",
                        suggested_word_count=80,
                    ),
                    Section(
                        title="Mise en oeuvre",
                        description="Comment la solution a été déployée, les étapes clés",
                        suggested_word_count=150,
                    ),
                    Section(
                        title="Spécificités techniques",
                        description="Détails techniques pertinents sans jargon excessif",
                        suggested_word_count=120,
                    ),
                ],
                tips=[
                    "Montrer le processus, pas juste le résultat final",
                    "Mentionner les obstacles rencontrés et comment ils ont été surmontés",
                ],
            ),
            Section(
                title="Les résultats",
                description="Résultats concrets, chiffrés et vérifiables.",
                suggested_word_count=250,
                subsections=[
                    Section(
                        title="Métriques clés",
                        description="KPIs avant/après avec pourcentages d'amélioration",
                        suggested_word_count=100,
                    ),
                    Section(
                        title="Bénéfices qualitatifs",
                        description="Améliorations non chiffrables mais significatives",
                        suggested_word_count=80,
                    ),
                    Section(
                        title="Témoignage",
                        description="Citation directe du client ou de l'équipe",
                        suggested_word_count=70,
                    ),
                ],
                tips=[
                    "Utiliser des visuels : graphiques avant/après, tableaux comparatifs",
                    "Les chiffres sont le coeur de la crédibilité du use case",
                    "Un bon témoignage vaut mille arguments",
                ],
            ),
            Section(
                title="Enseignements et prochaines étapes",
                description="Leçons apprises et perspectives futures.",
                suggested_word_count=150,
                tips=[
                    "Quelles leçons peuvent être appliquées par le lecteur",
                    "Mentionner les évolutions prévues",
                    "CTA : 'Vous avez un défi similaire? Parlons-en.'",
                ],
            ),
        ]
