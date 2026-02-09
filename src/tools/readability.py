"""
ReadabilityAnalyzer - Analyse de lisibilité du contenu.

Implémente des métriques de lisibilité adaptées au français.
"""

import re


class ReadabilityAnalyzer:
    """Analyse la lisibilité d'un texte."""

    def analyze(self, content: str) -> int:
        """
        Retourne un score de lisibilité sur 100.

        Critères:
        - Longueur moyenne des phrases
        - Longueur moyenne des mots
        - Diversité du vocabulaire
        - Structure (paragraphes, listes)
        """
        if not content.strip():
            return 0

        scores = {
            "sentence_length": self._score_sentence_length(content),
            "word_length": self._score_word_length(content),
            "vocabulary_diversity": self._score_vocabulary_diversity(content),
            "structure": self._score_structure(content),
        }

        # Moyenne pondérée
        weights = {
            "sentence_length": 0.30,
            "word_length": 0.20,
            "vocabulary_diversity": 0.20,
            "structure": 0.30,
        }

        total = sum(scores[k] * weights[k] for k in scores)
        return min(100, round(total))

    def get_detailed_report(self, content: str) -> dict:
        """Retourne un rapport détaillé de lisibilité."""
        sentences = self._split_sentences(content)
        words = self._extract_words(content)

        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        avg_word_length = sum(len(w) for w in words) / max(len(words), 1)
        unique_words = len(set(w.lower() for w in words))

        return {
            "score": self.analyze(content),
            "metrics": {
                "total_words": len(words),
                "total_sentences": len(sentences),
                "avg_sentence_length": round(avg_sentence_length, 1),
                "avg_word_length": round(avg_word_length, 1),
                "unique_words": unique_words,
                "vocabulary_richness": round(unique_words / max(len(words), 1) * 100, 1),
            },
            "recommendations": self._get_recommendations(content),
        }

    def _split_sentences(self, content: str) -> list[str]:
        """Découpe le texte en phrases."""
        # Retirer le markdown
        text = re.sub(r"^#+\s.*$", "", content, flags=re.MULTILINE)
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
        text = re.sub(r"\*([^*]+)\*", r"\1", text)

        sentences = re.split(r"[.!?]+", text)
        return [s.strip() for s in sentences if s.strip() and len(s.split()) > 2]

    def _extract_words(self, content: str) -> list[str]:
        """Extrait les mots du texte (sans markdown)."""
        text = re.sub(r"[#*_`\[\]()>-]", " ", content)
        words = re.findall(r"\b[a-zA-ZÀ-ÿ]{2,}\b", text)
        return words

    def _score_sentence_length(self, content: str) -> int:
        """Score basé sur la longueur des phrases (idéal: 15-20 mots)."""
        sentences = self._split_sentences(content)
        if not sentences:
            return 0

        avg = sum(len(s.split()) for s in sentences) / len(sentences)

        if 12 <= avg <= 20:
            return 100
        elif 10 <= avg <= 25:
            return 75
        elif 8 <= avg <= 30:
            return 50
        else:
            return 25

    def _score_word_length(self, content: str) -> int:
        """Score basé sur la longueur des mots (simplicité du vocabulaire)."""
        words = self._extract_words(content)
        if not words:
            return 0

        avg = sum(len(w) for w in words) / len(words)

        # En français, la moyenne est autour de 5-6 lettres
        if 4 <= avg <= 6:
            return 100
        elif 3 <= avg <= 7:
            return 75
        elif avg <= 8:
            return 50
        else:
            return 25

    def _score_vocabulary_diversity(self, content: str) -> int:
        """Score basé sur la diversité du vocabulaire."""
        words = self._extract_words(content)
        if not words:
            return 0

        unique_ratio = len(set(w.lower() for w in words)) / len(words)

        if unique_ratio >= 0.6:
            return 100
        elif unique_ratio >= 0.4:
            return 75
        elif unique_ratio >= 0.3:
            return 50
        else:
            return 25

    def _score_structure(self, content: str) -> int:
        """Score basé sur la structure du document."""
        score = 0

        # Présence de titres
        headings = len(re.findall(r"^#+\s", content, re.MULTILINE))
        if headings >= 4:
            score += 30
        elif headings >= 2:
            score += 15

        # Présence de listes
        lists = len(re.findall(r"^[-*]\s", content, re.MULTILINE))
        if lists >= 3:
            score += 25
        elif lists >= 1:
            score += 10

        # Paragraphes courts (bonne aération)
        paragraphs = [p for p in content.split("\n\n") if p.strip()]
        short_paras = sum(1 for p in paragraphs if len(p.split()) <= 60)
        if paragraphs:
            short_ratio = short_paras / len(paragraphs)
            if short_ratio >= 0.7:
                score += 25
            elif short_ratio >= 0.5:
                score += 15

        # Mise en forme (gras, italique)
        if re.search(r"\*\*[^*]+\*\*", content):
            score += 10
        if re.search(r"(?<!\*)\*(?!\*)[^*]+\*(?!\*)", content):
            score += 10

        return min(100, score)

    def _get_recommendations(self, content: str) -> list[str]:
        """Génère des recommandations d'amélioration."""
        recommendations = []
        sentences = self._split_sentences(content)
        words = self._extract_words(content)

        if sentences:
            avg_sentence = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_sentence > 25:
                recommendations.append(
                    f"Phrases trop longues (moyenne: {avg_sentence:.0f} mots). "
                    "Visez 15-20 mots par phrase."
                )

            long_sentences = [s for s in sentences if len(s.split()) > 30]
            if long_sentences:
                recommendations.append(
                    f"{len(long_sentences)} phrase(s) de plus de 30 mots à diviser."
                )

        if words:
            unique_ratio = len(set(w.lower() for w in words)) / len(words)
            if unique_ratio < 0.4:
                recommendations.append(
                    "Vocabulaire répétitif. Utilisez des synonymes pour varier."
                )

        headings = len(re.findall(r"^#+\s", content, re.MULTILINE))
        if headings < 3:
            recommendations.append("Ajoutez plus de sous-titres pour aérer le contenu.")

        if not re.search(r"^[-*]\s", content, re.MULTILINE):
            recommendations.append("Utilisez des listes à puces pour les énumérations.")

        return recommendations
