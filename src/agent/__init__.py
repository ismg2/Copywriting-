from .writer import CopywritingAgent
from .pipeline import WritingPipeline
from .personas import Persona, PERSONAS
from .llm_clients import (
    OllamaClient,
    AnthropicClient,
    OpenAIClient,
    LLMConfig,
    create_llm_client,
    auto_detect_client,
)

__all__ = [
    "CopywritingAgent",
    "WritingPipeline",
    "Persona",
    "PERSONAS",
    "OllamaClient",
    "AnthropicClient",
    "OpenAIClient",
    "LLMConfig",
    "create_llm_client",
    "auto_detect_client",
]
