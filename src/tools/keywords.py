"""
KeywordExtractor - Extraction et analyse de mots-clés.
"""

import re
from collections import Counter


# Mots vides français (stop words)
FRENCH_STOP_WORDS = {
    "le", "la", "les", "de", "du", "des", "un", "une", "et", "en", "est",
    "que", "qui", "dans", "pour", "au", "aux", "ce", "cette", "ces",
    "son", "sa", "ses", "sur", "par", "pas", "plus", "avec", "mais",
    "ou", "ne", "se", "si", "il", "elle", "on", "nous", "vous", "ils",
    "elles", "leur", "leurs", "mon", "ma", "mes", "ton", "ta", "tes",
    "tout", "tous", "toute", "toutes", "autre", "autres", "même",
    "aussi", "bien", "très", "trop", "peu", "assez", "encore",
    "alors", "donc", "car", "comme", "quand", "comment", "où",
    "peut", "être", "avoir", "fait", "faire", "dit", "sont", "été",
    "entre", "après", "avant", "chez", "sans", "sous", "vers",
    "dont", "nos", "vos", "cette", "été", "cela", "votre", "notre",
}


class KeywordExtractor:
    """Extraction et analyse de mots-clés dans le contenu."""

    def extract_keywords(self, content: str, top_n: int = 20) -> list[tuple[str, int]]:
        """
        Extrait les mots-clés les plus fréquents du contenu.

        Args:
            content: Texte à analyser.
            top_n: Nombre de mots-clés à retourner.

        Returns:
            Liste de tuples (mot-clé, fréquence) triés par fréquence.
        """
        words = self._tokenize(content)
        filtered = [w for w in words if w not in FRENCH_STOP_WORDS and len(w) > 3]
        return Counter(filtered).most_common(top_n)

    def extract_bigrams(self, content: str, top_n: int = 10) -> list[tuple[str, int]]:
        """Extrait les bigrammes (paires de mots) les plus fréquents."""
        words = self._tokenize(content)
        filtered = [w for w in words if w not in FRENCH_STOP_WORDS and len(w) > 2]

        bigrams = [f"{filtered[i]} {filtered[i+1]}" for i in range(len(filtered) - 1)]
        return Counter(bigrams).most_common(top_n)

    def analyze_density(self, content: str, target_keywords: list[str]) -> dict[str, dict]:
        """
        Analyse la densité des mots-clés cibles dans le contenu.

        Args:
            content: Texte à analyser.
            target_keywords: Liste de mots-clés à vérifier.

        Returns:
            Dict avec la densité et le status pour chaque mot-clé.
        """
        if not target_keywords:
            return {}

        content_lower = content.lower()
        total_words = len(content_lower.split())

        if total_words == 0:
            return {}

        results = {}
        for keyword in target_keywords:
            kw_lower = keyword.lower()
            count = content_lower.count(kw_lower)
            # Ajuster le comptage pour les expressions multi-mots
            kw_words = len(kw_lower.split())
            density = (count * kw_words / total_words) * 100

            if 1.0 <= density <= 2.5:
                status = "optimal"
            elif 0.5 <= density < 1.0:
                status = "low"
            elif 2.5 < density <= 4.0:
                status = "high"
            elif density > 4.0:
                status = "stuffing"
            else:
                status = "very_low"

            results[keyword] = {
                "count": count,
                "density_percent": round(density, 2),
                "status": status,
                "recommendation": self._density_recommendation(density, keyword),
            }

        return results

    def suggest_related_keywords(self, content: str, primary_keyword: str) -> list[str]:
        """
        Suggère des mots-clés associés basés sur le contenu existant.

        Identifie les mots fréquemment proches du mot-clé principal.
        """
        content_lower = content.lower()
        primary_lower = primary_keyword.lower()

        # Trouver les phrases contenant le mot-clé principal
        sentences = re.split(r"[.!?]", content_lower)
        relevant_sentences = [s for s in sentences if primary_lower in s]

        # Extraire les mots de ces phrases
        related_words = []
        for sentence in relevant_sentences:
            words = re.findall(r"\b[a-zA-ZÀ-ÿ]{4,}\b", sentence)
            related_words.extend(
                w for w in words
                if w not in FRENCH_STOP_WORDS and w != primary_lower
            )

        # Retourner les plus fréquents
        counter = Counter(related_words)
        return [word for word, _ in counter.most_common(10)]

    def _tokenize(self, content: str) -> list[str]:
        """Tokenize le contenu en mots normalisés."""
        # Retirer le markdown
        text = re.sub(r"[#*_`\[\]()>]", " ", content)
        # Extraire les mots
        words = re.findall(r"\b[a-zA-ZÀ-ÿ]+\b", text.lower())
        return words

    def _density_recommendation(self, density: float, keyword: str) -> str:
        """Génère une recommandation basée sur la densité."""
        if density < 0.5:
            return f"Augmentez l'utilisation de '{keyword}'. Ajoutez-le dans les titres et premiers paragraphes."
        elif density < 1.0:
            return f"Densité légèrement faible pour '{keyword}'. Intégrez-le 2-3 fois de plus naturellement."
        elif density <= 2.5:
            return f"Densité optimale pour '{keyword}'. Maintenez ce niveau."
        elif density <= 4.0:
            return f"Attention: '{keyword}' est trop utilisé. Remplacez certaines occurrences par des synonymes."
        else:
            return f"Keyword stuffing pour '{keyword}'. Réduisez drastiquement et utilisez des variations."
