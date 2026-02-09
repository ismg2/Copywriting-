"""
BaseTemplate - Classe de base pour tous les templates de contenu.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Section:
    """Représente une section du contenu."""

    title: str
    description: str
    suggested_word_count: int
    subsections: list["Section"] = field(default_factory=list)
    tips: list[str] = field(default_factory=list)


class BaseTemplate(ABC):
    """Template de base pour la structure de contenu."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nom du template."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Description du template."""
        ...

    @abstractmethod
    def get_sections(self) -> list[Section]:
        """Retourne la liste des sections du template."""
        ...

    def get_structure_guide(self) -> str:
        """Génère un guide de structure pour le prompt."""
        sections = self.get_sections()
        lines = [f"# Structure: {self.name}", f"_{self.description}_\n"]

        for i, section in enumerate(sections, 1):
            lines.append(f"## {i}. {section.title} (~{section.suggested_word_count} mots)")
            lines.append(f"   {section.description}")

            if section.subsections:
                for sub in section.subsections:
                    lines.append(f"   - **{sub.title}**: {sub.description}")

            if section.tips:
                lines.append("   **Tips:**")
                for tip in section.tips:
                    lines.append(f"   - {tip}")

            lines.append("")

        return "\n".join(lines)

    def get_total_word_count(self) -> int:
        """Calcule le nombre total de mots suggéré."""
        return sum(s.suggested_word_count for s in self.get_sections())
