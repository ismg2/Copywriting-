"""Tests pour l'analyseur de lisibilité."""

from src.tools.readability import ReadabilityAnalyzer


def test_analyze_returns_score():
    analyzer = ReadabilityAnalyzer()
    content = "# Titre\n\nUne phrase simple. Une autre phrase."
    score = analyzer.analyze(content)
    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_empty_content():
    analyzer = ReadabilityAnalyzer()
    assert analyzer.analyze("") == 0


def test_detailed_report():
    analyzer = ReadabilityAnalyzer()
    content = "# Titre\n\n## Section\n\nPremière phrase courte. Deuxième phrase aussi courte."
    report = analyzer.get_detailed_report(content)
    assert "score" in report
    assert "metrics" in report
    assert "recommendations" in report
    assert report["metrics"]["total_words"] > 0


def test_well_structured_content_scores_higher():
    analyzer = ReadabilityAnalyzer()
    good = "# Titre\n\n## Section 1\n\nPhrase courte. Autre phrase.\n\n- Point un\n- Point deux\n\n## Section 2\n\n**Important**: texte en gras."
    bad = "Un très long bloc de texte sans aucune structure ni titre ni liste ni mise en forme qui continue encore et encore sans jamais s'arrêter ce qui rend la lecture très difficile et fatigante pour le lecteur qui doit parcourir tout ce pavé."
    assert analyzer.analyze(good) > analyzer.analyze(bad)
