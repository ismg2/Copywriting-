"""
Prompts pour l'étape d'édition et de polish.
"""

EDITING_PROMPTS = {
    "edit": """Tu es un éditeur senior exigeant et bienveillant.

**Brouillon à réviser:**
{draft}

### Grille de révision:

**1. Structure (20 points)**
- [ ] Le titre est accrocheur et optimisé SEO
- [ ] L'intro capte l'attention en 3 secondes
- [ ] La structure est logique et progressive
- [ ] Les transitions entre sections sont fluides
- [ ] La conclusion apporte une vraie valeur

**2. Contenu (30 points)**
- [ ] Chaque section apporte de la valeur
- [ ] Les arguments sont étayés par des données
- [ ] Les exemples sont concrets et pertinents
- [ ] Pas de redondances ni de remplissage
- [ ] Le niveau de détail est adapté à l'audience

**3. Style (25 points)**
- [ ] Le ton est cohérent tout au long
- [ ] Les phrases sont claires et concises
- [ ] Le vocabulaire est riche mais accessible
- [ ] Les paragraphes sont aérés (max 3-4 phrases)
- [ ] L'écriture est active (pas passive)

**4. SEO & Format (15 points)**
- [ ] Mots-clés intégrés naturellement
- [ ] Sous-titres descriptifs et optimisés
- [ ] Listes et mise en forme utilisées à bon escient
- [ ] Meta description présente et optimisée
- [ ] Longueur appropriée

**5. Correction (10 points)**
- [ ] Orthographe impeccable
- [ ] Grammaire correcte
- [ ] Ponctuation appropriée
- [ ] Cohérence typographique

Produis:
1. La version révisée complète
2. Un résumé des modifications effectuées
3. Un score sur 100 basé sur la grille ci-dessus""",

    "polish": """Tu es un expert en finalisation de contenu éditorial.

**Contenu révisé:**
{content}

**Mots-clés cibles:** {keywords}

### Checklist de finalisation:

1. **SEO final**
   - Mot-clé principal dans les 100 premiers mots
   - Densité de mots-clés entre 1% et 2.5%
   - Titres H2/H3 contenant des mots-clés secondaires
   - Meta description de 150-160 caractères

2. **Éléments manquants**
   - TL;DR en début d'article (2-3 phrases)
   - CTA final clair et engageant
   - Suggestions de contenu associé

3. **Formatage**
   - Markdown propre et consistant
   - Espacement cohérent
   - Listes bien formatées

4. **Métadonnées**
   Ajoute en fin de document:
   ```yaml
   ---
   title: "..."
   description: "..."
   keywords: [...]
   word_count: X
   reading_time: "X min"
   content_type: "..."
   ---
   ```

Produis le contenu final prêt à publier.""",
}
