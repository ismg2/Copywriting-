"""
SEOAnalyzer - Analyse SEO du contenu généré.
"""

import re


class SEOAnalyzer:
    """Analyse et score SEO d'un contenu."""

    def analyze(self, content: str, keywords: list[str]) -> int:
        """
        Analyse le contenu et retourne un score SEO sur 100.

        Critères évalués:
        - Présence du mot-clé dans le titre (H1)
        - Structure de titres (H1, H2, H3)
        - Densité de mots-clés
        - Longueur du contenu
        - Présence de meta description
        - Liens et médias
        - Lisibilité des paragraphes
        """
        score = 0
        checks = self.run_checks(content, keywords)

        for check in checks.values():
            score += check["score"]

        return min(100, score)

    def run_checks(self, content: str, keywords: list[str]) -> dict:
        """Exécute tous les checks SEO et retourne le détail."""
        return {
            "title": self._check_title(content, keywords),
            "headings": self._check_headings(content),
            "keyword_density": self._check_keyword_density(content, keywords),
            "content_length": self._check_content_length(content),
            "meta_description": self._check_meta_description(content),
            "paragraphs": self._check_paragraphs(content),
            "internal_structure": self._check_internal_structure(content),
        }

    def _check_title(self, content: str, keywords: list[str]) -> dict:
        """Vérifie le titre H1."""
        h1_match = re.search(r"^# (.+)$", content, re.MULTILINE)
        if not h1_match:
            return {"score": 0, "message": "Pas de titre H1 trouvé", "status": "fail"}

        title = h1_match.group(1).lower()
        title_length = len(title)

        score = 5  # H1 présent
        messages = []

        # Longueur optimale du titre (50-70 chars)
        if 50 <= title_length <= 70:
            score += 5
        elif title_length < 50:
            messages.append(f"Titre trop court ({title_length} chars, idéal: 50-70)")
        else:
            messages.append(f"Titre trop long ({title_length} chars, idéal: 50-70)")

        # Mot-clé dans le titre
        if keywords:
            primary = keywords[0].lower()
            if primary in title:
                score += 5
            else:
                messages.append(f"Mot-clé principal '{keywords[0]}' absent du titre")

        message = "; ".join(messages) if messages else "Titre optimisé"
        return {"score": score, "message": message, "status": "pass" if score >= 10 else "warn"}

    def _check_headings(self, content: str) -> dict:
        """Vérifie la structure des titres."""
        h2_count = len(re.findall(r"^## ", content, re.MULTILINE))
        h3_count = len(re.findall(r"^### ", content, re.MULTILINE))

        score = 0
        messages = []

        if h2_count >= 3:
            score += 10
        elif h2_count >= 2:
            score += 5
            messages.append("Ajoutez plus de sous-titres H2 (minimum 3 recommandé)")
        else:
            messages.append("Structure de titres insuffisante")

        if h3_count >= 2:
            score += 5

        message = "; ".join(messages) if messages else f"{h2_count} H2, {h3_count} H3 - bonne structure"
        return {"score": score, "message": message, "status": "pass" if score >= 10 else "warn"}

    def _check_keyword_density(self, content: str, keywords: list[str]) -> dict:
        """Vérifie la densité des mots-clés."""
        if not keywords:
            return {"score": 10, "message": "Pas de mots-clés cibles définis", "status": "info"}

        words = content.lower().split()
        total_words = len(words)
        if total_words == 0:
            return {"score": 0, "message": "Contenu vide", "status": "fail"}

        content_lower = content.lower()
        primary = keywords[0].lower()
        count = content_lower.count(primary)
        density = (count / total_words) * 100

        score = 0
        if 1.0 <= density <= 2.5:
            score = 15
            message = f"Densité optimale: {density:.1f}% pour '{keywords[0]}'"
        elif 0.5 <= density < 1.0:
            score = 8
            message = f"Densité faible: {density:.1f}% (idéal: 1-2.5%)"
        elif 2.5 < density <= 4.0:
            score = 5
            message = f"Densité élevée: {density:.1f}% - risque de keyword stuffing"
        elif density > 4.0:
            score = 0
            message = f"Keyword stuffing détecté: {density:.1f}%"
        else:
            score = 3
            message = f"Mot-clé sous-utilisé: {density:.1f}%"

        return {"score": score, "message": message, "status": "pass" if score >= 10 else "warn"}

    def _check_content_length(self, content: str) -> dict:
        """Vérifie la longueur du contenu."""
        word_count = len(content.split())

        if word_count >= 1500:
            return {"score": 15, "message": f"{word_count} mots - longueur optimale", "status": "pass"}
        elif word_count >= 1000:
            return {"score": 10, "message": f"{word_count} mots - acceptable", "status": "warn"}
        elif word_count >= 500:
            return {"score": 5, "message": f"{word_count} mots - contenu court", "status": "warn"}
        else:
            return {"score": 0, "message": f"{word_count} mots - contenu trop court", "status": "fail"}

    def _check_meta_description(self, content: str) -> dict:
        """Vérifie la présence d'une meta description."""
        # Cherche un pattern de meta description dans le contenu
        meta_patterns = [
            r"description:\s*(.+)",
            r"\*\*Meta description[:\s]*\*\*\s*(.+)",
            r"meta_description:\s*(.+)",
        ]

        for pattern in meta_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                desc = match.group(1).strip()
                length = len(desc)
                if 140 <= length <= 160:
                    return {"score": 10, "message": f"Meta description optimale ({length} chars)", "status": "pass"}
                else:
                    return {"score": 5, "message": f"Meta description: {length} chars (idéal: 140-160)", "status": "warn"}

        return {"score": 0, "message": "Pas de meta description trouvée", "status": "fail"}

    def _check_paragraphs(self, content: str) -> dict:
        """Vérifie la longueur des paragraphes."""
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip() and not p.strip().startswith("#")]

        if not paragraphs:
            return {"score": 0, "message": "Pas de paragraphes détectés", "status": "fail"}

        long_paragraphs = [p for p in paragraphs if len(p.split()) > 100]
        ratio = len(long_paragraphs) / len(paragraphs)

        if ratio == 0:
            return {"score": 10, "message": "Paragraphes bien dimensionnés", "status": "pass"}
        elif ratio < 0.3:
            return {"score": 5, "message": f"{len(long_paragraphs)} paragraphe(s) trop long(s)", "status": "warn"}
        else:
            return {"score": 0, "message": "Trop de paragraphes longs - divisez-les", "status": "fail"}

    def _check_internal_structure(self, content: str) -> dict:
        """Vérifie la structure interne (listes, emphase, etc.)."""
        score = 0
        features = []

        # Listes
        if re.search(r"^[-*] ", content, re.MULTILINE):
            score += 5
            features.append("listes")

        # Texte en gras
        if re.search(r"\*\*[^*]+\*\*", content):
            score += 3
            features.append("mise en gras")

        # Texte en italique
        if re.search(r"(?<!\*)\*(?!\*)[^*]+\*(?!\*)", content):
            score += 2
            features.append("italique")

        if features:
            return {"score": score, "message": f"Éléments trouvés: {', '.join(features)}", "status": "pass"}
        else:
            return {"score": 0, "message": "Ajoutez des listes, du gras, etc.", "status": "warn"}
