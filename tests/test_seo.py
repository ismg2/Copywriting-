"""Tests pour l'analyseur SEO."""

from src.tools.seo import SEOAnalyzer


def test_analyze_returns_score():
    seo = SEOAnalyzer()
    content = "# Mon titre\n\nDu contenu ici."
    score = seo.analyze(content, [])
    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_h1_detection():
    seo = SEOAnalyzer()
    checks = seo.run_checks("# Titre avec mot-clé\n\nContenu.", ["mot-clé"])
    assert checks["title"]["score"] > 0


def test_no_h1():
    seo = SEOAnalyzer()
    checks = seo.run_checks("Contenu sans titre.", [])
    assert checks["title"]["score"] == 0


def test_heading_structure():
    seo = SEOAnalyzer()
    content = "# H1\n## H2 a\n## H2 b\n## H2 c\n### H3"
    checks = seo.run_checks(content, [])
    assert checks["headings"]["score"] >= 10


def test_keyword_density_optimal():
    seo = SEOAnalyzer()
    # ~100 mots avec "marketing" apparaissant 2 fois = ~2% densité
    content = "Le marketing digital est un domaine en pleine évolution. " + "Chaque entreprise doit investir dans sa stratégie numérique. " * 8 + "Le marketing reste un levier essentiel pour la croissance."
    checks = seo.run_checks(content, ["marketing"])
    assert checks["keyword_density"]["score"] > 0


def test_content_length_scoring():
    seo = SEOAnalyzer()
    short = "Court. " * 10
    long = "Mot " * 1600
    assert seo.run_checks(short, [])["content_length"]["score"] < seo.run_checks(long, [])["content_length"]["score"]
