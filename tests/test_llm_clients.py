"""Tests pour les clients LLM."""

from src.agent.llm_clients import (
    OllamaClient,
    LLMConfig,
    create_llm_client,
)


def test_ollama_client_init():
    client = OllamaClient(model="mistral", base_url="http://localhost:11434")
    assert client.model == "mistral"
    assert client.base_url == "http://localhost:11434"
    assert client._provider == "ollama"


def test_ollama_client_strips_trailing_slash():
    client = OllamaClient(base_url="http://localhost:11434/")
    assert client.base_url == "http://localhost:11434"


def test_ollama_unavailable():
    client = OllamaClient(base_url="http://localhost:99999")
    assert client.is_available() is False


def test_create_llm_client_ollama():
    config = LLMConfig(provider="ollama", model="mistral")
    client = create_llm_client(config)
    assert client._provider == "ollama"
    assert client.model == "mistral"


def test_create_llm_client_ollama_custom_url():
    config = LLMConfig(provider="ollama", model="llama3.1", base_url="http://myserver:11434")
    client = create_llm_client(config)
    assert client.base_url == "http://myserver:11434"


def test_create_llm_client_unknown_provider():
    config = LLMConfig(provider="unknown", model="test")
    try:
        create_llm_client(config)
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "unknown" in str(e).lower()


def test_create_llm_client_anthropic_no_key():
    config = LLMConfig(provider="anthropic", model="claude-sonnet-4-20250514", api_key="")
    try:
        create_llm_client(config)
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_create_llm_client_openai_no_key():
    config = LLMConfig(provider="openai", model="gpt-4", api_key="")
    try:
        create_llm_client(config)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
