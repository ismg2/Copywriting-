"""
LLM Clients - Abstraction des différents fournisseurs de LLM.

Supporte :
- Ollama (local, sans clé API, sans dépendance externe)
- Anthropic (via SDK anthropic)
- OpenAI (via SDK openai)
"""

import json
import urllib.request
import urllib.error
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """Configuration commune pour tous les clients LLM."""

    provider: str  # "ollama", "anthropic", "openai"
    model: str
    base_url: str = ""
    api_key: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7


class OllamaClient:
    """
    Client Ollama utilisant uniquement urllib (zéro dépendance externe).

    Ollama expose une API REST sur http://localhost:11434.
    Aucune clé API requise.
    """

    def __init__(self, model: str = "llama3.1", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self._provider = "ollama"

    def generate(self, prompt: str, max_tokens: int = 4096, temperature: float = 0.7) -> str:
        """
        Génère du texte via l'API Ollama /api/chat.

        Args:
            prompt: Le prompt à envoyer.
            max_tokens: Nombre max de tokens en sortie.
            temperature: Température de génération.

        Returns:
            Le texte généré.
        """
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["message"]["content"]
        except urllib.error.URLError as e:
            raise ConnectionError(
                f"Impossible de se connecter à Ollama sur {self.base_url}. "
                f"Vérifiez qu'Ollama est lancé (ollama serve). Erreur: {e}"
            ) from e

    def list_models(self) -> list[dict]:
        """Liste les modèles disponibles dans Ollama."""
        url = f"{self.base_url}/api/tags"
        req = urllib.request.Request(url, method="GET")

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result.get("models", [])
        except urllib.error.URLError as e:
            raise ConnectionError(
                f"Impossible de se connecter à Ollama sur {self.base_url}. "
                f"Vérifiez qu'Ollama est lancé (ollama serve). Erreur: {e}"
            ) from e

    def is_available(self) -> bool:
        """Vérifie si Ollama est accessible."""
        try:
            url = f"{self.base_url}/api/tags"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200
        except (urllib.error.URLError, OSError):
            return False


class AnthropicClient:
    """Client wrapper pour le SDK Anthropic."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        try:
            import anthropic
        except ImportError:
            raise ImportError("pip install anthropic  — pour utiliser le provider Anthropic")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self._provider = "anthropic"

    def generate(self, prompt: str, max_tokens: int = 4096, temperature: float = 0.7) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text


class OpenAIClient:
    """Client wrapper pour le SDK OpenAI."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        try:
            import openai
        except ImportError:
            raise ImportError("pip install openai  — pour utiliser le provider OpenAI")
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self._provider = "openai"

    def generate(self, prompt: str, max_tokens: int = 4096, temperature: float = 0.7) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content


def create_llm_client(config: LLMConfig):
    """
    Factory : crée le bon client LLM selon la configuration.

    Args:
        config: Configuration LLM avec provider, model, etc.

    Returns:
        Un client LLM avec la méthode .generate(prompt) -> str
    """
    if config.provider == "ollama":
        base_url = config.base_url or "http://localhost:11434"
        return OllamaClient(model=config.model, base_url=base_url)

    elif config.provider == "anthropic":
        if not config.api_key:
            raise ValueError("ANTHROPIC_API_KEY requis pour le provider Anthropic")
        return AnthropicClient(api_key=config.api_key, model=config.model)

    elif config.provider == "openai":
        if not config.api_key:
            raise ValueError("OPENAI_API_KEY requis pour le provider OpenAI")
        return OpenAIClient(api_key=config.api_key, model=config.model)

    else:
        raise ValueError(
            f"Provider '{config.provider}' inconnu. "
            "Disponibles: ollama, anthropic, openai"
        )


def auto_detect_client() -> tuple:
    """
    Détecte automatiquement le meilleur client disponible.

    Ordre de priorité :
    1. Ollama (local, sans config)
    2. Anthropic (si ANTHROPIC_API_KEY défini)
    3. OpenAI (si OPENAI_API_KEY défini)

    Returns:
        Tuple (client, provider_name) ou (None, None)
    """
    import os

    # 1. Tenter Ollama (priorité au local)
    ollama = OllamaClient()
    if ollama.is_available():
        return ollama, "ollama"

    # 2. Anthropic
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        try:
            return AnthropicClient(api_key=api_key), "anthropic"
        except ImportError:
            pass

    # 3. OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        try:
            return OpenAIClient(api_key=api_key), "openai"
        except ImportError:
            pass

    return None, None
