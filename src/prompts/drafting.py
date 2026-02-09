"""
Prompts pour l'étape de rédaction (drafting).
"""

DRAFTING_PROMPTS = {
    "default": """Tu es un rédacteur professionnel expert.

**Plan à suivre:**
{outline}

**Notes de recherche:**
{research}

**Consignes:**
- Type: {content_type}
- Mots-clés à intégrer: {keywords}
- Nombre de mots cible: {word_count}
- Langue: {language}

{persona_context}

### Règles de rédaction:
1. **Suivre le plan exactement** - Ne pas dévier de la structure
2. **Fluidité** - Chaque phrase doit couler naturellement vers la suivante
3. **Valeur** - Chaque paragraphe doit apporter quelque chose au lecteur
4. **Concret** - Exemples, données, illustrations à chaque point clé
5. **Format** - Markdown propre avec H1, H2, H3, listes, gras

### Mots-clés SEO:
Intègre les mots-clés suivants naturellement (densité 1-2%):
{keywords}

Rédige maintenant le contenu complet.""",
}
