"""
Prompts pour l'étape de recherche.
"""

RESEARCH_PROMPTS = {
    "article": """Tu es un chercheur expert préparant un brief pour un article de fond.

**Sujet:** {topic}
**Mots-clés cibles:** {keywords}
**Audience:** {audience}

Produis un brief de recherche structuré:

### 1. Contexte et pertinence
- Pourquoi ce sujet est important maintenant
- Tendances actuelles liées au sujet
- Événements récents pertinents

### 2. Points clés à couvrir (5-7)
Pour chaque point:
- Fait ou insight principal
- Données/statistiques de support
- Source type (étude, rapport, expert)

### 3. Angle éditorial recommandé
- Perspective unique à adopter
- Ce qui différencie cet article des existants
- Hook narratif potentiel

### 4. Questions de l'audience
- 5 questions fréquentes sur ce sujet
- Objections ou préjugés à adresser

### 5. Concurrence éditoriale
- Types d'articles existants sur ce sujet
- Gaps de contenu à exploiter
- Opportunités de différenciation""",

    "blog": """Tu es un stratège de contenu blog préparant un brief.

**Sujet:** {topic}
**Mots-clés cibles:** {keywords}
**Audience:** {audience}

Produis un brief blog orienté engagement:

### 1. Angle accrocheur
- Quel problème concret résoudre pour le lecteur
- Quel bénéfice immédiat promettre
- Quelle émotion susciter (curiosité, urgence, empathie)

### 2. Points clés (3-5 max)
- Conseils actionnables et concrets
- Exemples du quotidien
- Quick wins pour le lecteur

### 3. Éléments d'engagement
- Questions à poser au lecteur
- Anecdotes ou histoires à raconter
- Statistiques surprenantes

### 4. SEO & Distribution
- Titres alternatifs optimisés
- Extraits partageables sur les réseaux sociaux
- Questions "People Also Ask" associées""",

    "usecase": """Tu es un consultant préparant un brief d'étude de cas.

**Sujet/Projet:** {topic}
**Mots-clés cibles:** {keywords}
**Audience:** {audience}

Produis un brief d'étude de cas:

### 1. Contexte client
- Informations nécessaires sur le client/projet
- Secteur et enjeux du marché
- Taille et maturité de l'organisation

### 2. Problématique
- Défis principaux à mettre en avant
- Impact business des problèmes (chiffré si possible)
- Pourquoi les solutions précédentes ont échoué

### 3. Solution
- Composants clés de la solution
- Étapes de mise en oeuvre
- Éléments différenciateurs

### 4. Résultats attendus
- KPIs à mettre en avant
- Format avant/après
- ROI ou bénéfices quantifiables

### 5. Leçons et applicabilité
- Ce que d'autres peuvent apprendre
- Conditions de réplicabilité
- Prochaines étapes""",
}
