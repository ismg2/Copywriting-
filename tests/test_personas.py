"""Tests pour le système de personas."""

from src.agent.personas import Persona, get_persona, list_personas, PERSONAS


def test_list_personas():
    personas = list_personas()
    assert len(personas) >= 5
    assert "expert_b2b" in personas
    assert "blog_casual" in personas


def test_get_persona():
    persona = get_persona("expert_b2b")
    assert isinstance(persona, Persona)
    assert persona.name == "Expert B2B"


def test_get_unknown_persona():
    try:
        get_persona("inexistant")
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_persona_to_prompt_context():
    persona = get_persona("storyteller")
    context = persona.to_prompt_context()
    assert "Storyteller" in context
    assert "Ton:" in context
    assert "À éviter:" in context


def test_all_personas_have_required_fields():
    for name, persona in PERSONAS.items():
        assert persona.name, f"{name} missing name"
        assert persona.tone, f"{name} missing tone"
        assert persona.style, f"{name} missing style"
        assert persona.guidelines, f"{name} missing guidelines"
        assert persona.avoid, f"{name} missing avoid"
