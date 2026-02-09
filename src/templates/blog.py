"""
BlogTemplate - Template pour articles de blog engageants.
"""

from .base import BaseTemplate, Section


class BlogTemplate(BaseTemplate):
    """Template pour posts de blog conversationnels et engageants."""

    @property
    def name(self) -> str:
        return "Blog Post"

    @property
    def description(self) -> str:
        return (
            "Structure pour articles de blog : ton conversationnel, "
            "format scannable, engagement maximal."
        )

    def get_sections(self) -> list[Section]:
        return [
            Section(
                title="Titre et meta",
                description="Titre engageant format blog + meta description pour le SEO.",
                suggested_word_count=30,
                tips=[
                    "Formats qui marchent : 'Comment...', 'X raisons de...', 'Le guide complet de...'",
                    "Utiliser des chiffres dans le titre quand possible",
                    "Créer un sentiment d'urgence ou de curiosité",
                ],
            ),
            Section(
                title="Accroche",
                description="Premier paragraphe qui capte immédiatement l'attention.",
                suggested_word_count=80,
                tips=[
                    "Commencer par un problème que le lecteur reconnaît",
                    "Ou une question qui fait réfléchir",
                    "Maximum 2-3 phrases courtes et percutantes",
                ],
            ),
            Section(
                title="Le problème / Le contexte",
                description="Exposition du problème ou de la situation que le lecteur rencontre.",
                suggested_word_count=200,
                tips=[
                    "Montrer au lecteur que vous comprenez sa douleur",
                    "Utiliser le 'vous' pour impliquer directement",
                    "Raconter une mini-histoire si possible",
                ],
            ),
            Section(
                title="La solution / Les points clés",
                description="Coeur de l'article avec les conseils, astuces ou informations.",
                suggested_word_count=600,
                subsections=[
                    Section(
                        title="Point 1",
                        description="Premier conseil ou information clé",
                        suggested_word_count=200,
                    ),
                    Section(
                        title="Point 2",
                        description="Deuxième conseil ou information clé",
                        suggested_word_count=200,
                    ),
                    Section(
                        title="Point 3",
                        description="Troisième conseil ou information clé",
                        suggested_word_count=200,
                    ),
                ],
                tips=[
                    "Utiliser des sous-titres descriptifs pour chaque point",
                    "Alterner texte, listes et exemples",
                    "Chaque point doit être actionnable",
                ],
            ),
            Section(
                title="Exemple concret / Cas pratique",
                description="Illustration concrète avec un exemple réel ou fictif.",
                suggested_word_count=200,
                tips=[
                    "Un avant/après fonctionne très bien",
                    "Utiliser des screenshots ou schémas si possible",
                ],
            ),
            Section(
                title="Conclusion et CTA",
                description="Résumé rapide et appel à l'action engageant.",
                suggested_word_count=100,
                tips=[
                    "Résumer en 2-3 bullet points",
                    "Poser une question ouverte pour les commentaires",
                    "CTA clair : partager, commenter, s'inscrire, télécharger",
                ],
            ),
        ]
