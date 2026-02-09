"""Tests pour les templates de contenu."""

from src.templates import ArticleTemplate, BlogTemplate, UseCaseTemplate


def test_article_template():
    template = ArticleTemplate()
    assert template.name == "Article de fond"
    sections = template.get_sections()
    assert len(sections) >= 4
    assert template.get_total_word_count() > 0


def test_blog_template():
    template = BlogTemplate()
    assert template.name == "Blog Post"
    sections = template.get_sections()
    assert len(sections) >= 4


def test_usecase_template():
    template = UseCaseTemplate()
    assert "Use Case" in template.name
    sections = template.get_sections()
    assert len(sections) >= 4


def test_structure_guide_generation():
    for TemplateClass in [ArticleTemplate, BlogTemplate, UseCaseTemplate]:
        template = TemplateClass()
        guide = template.get_structure_guide()
        assert isinstance(guide, str)
        assert len(guide) > 100
        assert template.name in guide
