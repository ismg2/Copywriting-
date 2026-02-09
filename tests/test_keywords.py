"""Tests pour l'extracteur de mots-clés."""

from src.tools.keywords import KeywordExtractor


def test_extract_keywords():
    extractor = KeywordExtractor()
    content = "Le marketing digital transforme les entreprises. Le marketing est essentiel pour la croissance."
    keywords = extractor.extract_keywords(content, top_n=5)
    assert len(keywords) > 0
    assert any("marketing" in kw[0] for kw in keywords)


def test_extract_bigrams():
    extractor = KeywordExtractor()
    content = "Le marketing digital est important. Le marketing digital transforme tout."
    bigrams = extractor.extract_bigrams(content, top_n=5)
    assert len(bigrams) > 0


def test_analyze_density():
    extractor = KeywordExtractor()
    content = "marketing " * 10 + "autre mot " * 90
    density = extractor.analyze_density(content, ["marketing"])
    assert "marketing" in density
    assert density["marketing"]["count"] == 10
    assert density["marketing"]["density_percent"] > 0


def test_density_empty_keywords():
    extractor = KeywordExtractor()
    result = extractor.analyze_density("Du contenu quelconque.", [])
    assert result == {}


def test_suggest_related():
    extractor = KeywordExtractor()
    content = "Le marketing digital utilise des outils comme l'analyse marketing et l'automatisation marketing pour optimiser les campagnes."
    related = extractor.suggest_related_keywords(content, "marketing")
    assert isinstance(related, list)
