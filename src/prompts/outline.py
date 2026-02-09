"""
Prompts pour l'étape de structuration (outline).
"""

OUTLINE_PROMPTS = {
    "default": """Tu es un architecte de contenu expert en structure éditoriale.

**Sujet:** {topic}
**Type:** {content_type}
**Recherche:**
{research}
**Nombre de mots cible:** {word_count}

Crée un plan détaillé suivant ces règles:

### Structure requise:
1. **Titre H1** - Accrocheur, optimisé SEO, 50-70 caractères
2. **Meta description** - 150-160 caractères, incitative au clic
3. **Introduction** (10% du contenu)
   - Accroche (stat, question, anecdote)
   - Contexte et enjeu
   - Promesse de valeur / thèse
4. **Corps** (75% du contenu)
   - 3-5 sections H2
   - Sous-sections H3 si nécessaire
   - Points clés par section
   - Transitions entre sections
5. **Conclusion** (15% du contenu)
   - Synthèse
   - Ouverture / perspective
   - CTA

### Pour chaque section, précise:
- Titre H2 exact
- Points à couvrir (bullet points)
- Nombre de mots estimé
- Type de contenu (narratif, liste, analyse, exemple)
- Transition vers la section suivante""",
}
