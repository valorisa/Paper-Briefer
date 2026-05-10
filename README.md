# paper-briefer

> Compresse des articles scientifiques en contexte optimisé pour les conversations avec des LLM (Claude, ChatGPT, etc.).

## Le problème

Vous venez de trouver un article technique de 40 pages que vous devez comprendre. Vous voulez en discuter avec Claude ou ChatGPT : poser des questions sur l'architecture, vérifier les résultats, comprendre les limites.

Mais coller le texte brut dans un LLM pose plusieurs problèmes :

- Le texte issu d'un OCR est plein de bruit : références d'images, formatage cassé, en-têtes répétés
- La majorité des tokens consommés n'apportent rien à la conversation
- Le LLM n'a aucune carte mentale de l'article : il ne distingue pas les claims originales du survol bibliographique
- Vous payez (en tokens ou en qualité de réponse) pour du contenu sans valeur sémantique

## La solution

`paper-briefer` extrait le **squelette sémantique** d'un article : les claims, les preuves visuelles, les spécifications, les limitations, la structure argumentaire. Il compresse le tout en un brief de ~3-4K tokens qui préserve la qualité de discussion.

Le brief n'est pas un résumé. C'est une **injection de contexte structurée**, conçue pour donner au LLM tout ce dont il a besoin pour mener une conversation informée sur l'article, sans le bruit.

## Le workflow complet

Voici le processus de bout en bout, du PDF brut à la conversation avec un LLM :

```text
┌─────────────────────────────────────────────────────────────────────┐
│  1. DOCUMENT SOURCE                                                 │
│     Un article scientifique au format PDF                           │
│     (ex: DeepSeek-V4, 46 pages)                                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  2. OCR PLAYGROUND (Mistral AI)                                     │
│     https://console.mistral.ai/build/document-ai/ocr-playground     │
│                                                                     │
│     Vous uploadez le PDF. Mistral AI le convertit en markdown       │
│     structuré (une page = un fichier). Vous téléchargez le ZIP.     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  3. PAPER-BRIEFER (cet outil)                                       │
│     $ paper-briefer export.zip                                      │
│                                                                     │
│     Extrait le squelette sémantique : claims, figures avec          │
│     légendes, spécifications, limitations, carte des preuves.       │
│     Produit un brief de ~3-4K tokens.                               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. CONVERSATION LLM                                                │
│     Collez le brief dans Claude, ChatGPT, ou tout autre LLM.       │
│     Posez vos questions. Le LLM répond comme s'il avait lu          │
│     l'article entier — parce qu'il a la structure, pas le bruit.   │
└─────────────────────────────────────────────────────────────────────┘
```

**Résultat** : un article de 20 000 mots devient un brief de ~4 000 tokens (compression 5x) qui permet de répondre correctement à 4/5 questions techniques, sans aucune hallucination.

## Prise en main rapide

### Installation

```bash
pip install paper-briefer
```

### Utilisation de base

```bash
paper-briefer article-export.zip
```

Cette commande produit deux fichiers :

- `article-export-brief.md` : le brief compressé (~3-4K tokens), prêt à coller dans n'importe quel LLM
- `article-export-metadata.json` : les métadonnées structurées complètes, pour un usage programmatique

### Exemple concret

L'exemple inclus dans ce repo a été généré à partir du rapport technique [DeepSeek-V4](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf), traité via [OCR Playground de Mistral AI](https://console.mistral.ai/build/document-ai/ocr-playground) puis passé dans `paper-briefer` :

```bash
$ paper-briefer deepseek-v4.zip -o output/

Extracting metadata from deepseek-v4.zip...
  -> output/deepseek-v4-metadata.json (46 pages, 22 figures)
  -> output/deepseek-v4-brief.md (~4155 tokens)
  Compression: 20270 words -> ~4155 tokens (20%)
Done.
```

## Que contient le brief ?

Le brief est organisé en couches sémantiques, chacune servant un objectif précis pour la compréhension par un LLM :

| Section | Rôle | Exemple |
| ------- | ---- | ------- |
| Titre + périmètre | Identité et échelle de l'article | "46 pages, 22 figures, 20K mots" |
| Résumé | Claims principales, dans les mots des auteurs | Abstract complet préservé |
| Contributions clés | Ce qui est réellement nouveau | "attention hybride combinant CSA et HCA" |
| Spécifications | Les chiffres qui définissent le système | "1.6T params, 49B activés, 1M contexte" |
| Figures et tableaux | Preuves visuelles avec légendes + phrases d'ancrage | Ce que chaque figure démontre, en contexte |
| Structure | Table des matières navigable | Hiérarchie des sections avec pages |
| Limitations et perspectives | Ce que les auteurs reconnaissent comme faiblesses | Extrait de la conclusion |
| Densité de preuves | Quelles pages sont riches en références vs. contenu original | Guide pour repérer l'innovation |
| Références croisées | Comment les sections dépendent les unes des autres | "Section 3.2 référence Figure 5" |
| Mots-clés | Vocabulaire technique | Permet des questions de suivi précises |

### Pourquoi ces couches ?

Cette structure a été conçue et validée via un processus de revue contradictoire (documenté dans `docs/design-decisions/`). Insight clé : **les figures et tableaux portent la preuve**. Les claims d'un article vivent dans le texte, mais les preuves vivent dans les visuels. Extraire les légendes de figures avec leurs phrases d'ancrage ("La Figure 3 montre que...") transforme le brief d'un simple index en une carte des preuves.

## Comment utiliser le brief

### Avec Claude ou ChatGPT

Collez le brief comme contexte, puis posez vos questions naturellement :

```text
Voici le brief structuré de l'article dont je veux discuter :

[collez ici le contenu du fichier brief.md]

Questions :
- Comment l'architecture d'attention diffère-t-elle de la version précédente ?
- Quels sont les gains d'efficacité concrets pour les contextes longs ?
- Quelles limitations dois-je garder en tête avant de m'appuyer sur ce travail ?
```

### Avec Claude Code ou Cursor

Placez le brief dans votre projet et référencez-le :

```bash
paper-briefer article.zip -o docs/
# Ensuite dans Claude Code : "Lis docs/article-brief.md et explique-moi l'architecture"
```

### Comme pipeline de recherche (API Python)

```python
from paper_briefer.extract import extract
from paper_briefer.brief import generate_brief

metadata = extract("article.zip")

# Accès programmatique aux données structurées
for fig in metadata.figures_and_tables:
    print(f"{fig.id}: {fig.caption}")
    for anchor in fig.anchor_sentences:
        print(f"  Preuve: {anchor}")

# Générer le brief
brief = generate_brief(metadata)
print(brief)
```

## Qualité de compression

### Protocole de validation

Nous avons testé le brief sur le rapport technique DeepSeek-V4 (46 pages, 20 270 mots, 22 figures) en donnant le brief à une instance LLM fraîche (sans accès à l'article original) et en posant 5 questions techniques couvrant : architecture, claims quantitatives, limitations, évaluation de la nouveauté et implications pratiques.

### Résultats

| Métrique | Valeur |
| -------- | ------ |
| Taille d'entrée | 20 270 mots (~27K tokens) |
| Taille du brief | ~4 155 tokens |
| Ratio de compression | ~5x |
| Questions correctement répondues | 4/5 |
| Hallucinations | 0 |
| Identification correcte des lacunes | Oui (dit "je ne sais pas" quand l'info manque) |

### Ce qui a fonctionné

- **Questions d'architecture** : explication correcte du mécanisme CSA/HCA à partir des descriptions de figures
- **Claims quantitatives** : tous les chiffres de benchmarks reproduits exactement (taux de réussite, ratios de FLOPs)
- **Évaluation de la nouveauté** : distinction correcte entre composants hérités et nouveaux
- **Implications déploiement** : avantages pratiques déduits des spécifications

### Ce qui a échoué (et comment c'est corrigé)

- **Question sur les limitations** : le brief initial n'extrayait pas la section "Limitations & Future Work". Le LLM a correctement dit "cette information n'est pas dans le brief" plutôt que d'halluciner. Corrigé en v0.1 par l'ajout de l'extraction des limitations.

## Format d'entrée

### Actuellement supporté

**Exports ZIP d'OCR Playground** : le format structuré produit par [OCR Playground de Mistral AI](https://console.mistral.ai/build/document-ai/ocr-playground) lors de l'export de documents traités. Le ZIP contient :

```text
document.pdf/
  markdown.md              <- document complet en markdown
  pages/
    page-1/
      markdown.md          <- contenu par page
      img-0.jpeg           <- images extraites
      img-0.jpeg-annotation.json
      hyperlinks.md        <- URLs extraites
    page-2/
      ...
```

### Prévu pour les prochaines versions

- Entrée PDF directe (via OCR intégré ou outils externes)
- Sources LaTeX arXiv
- Fichiers markdown simples

## Référence CLI

```bash
# Basique : produit le brief ET les métadonnées
paper-briefer input.zip

# Spécifier un répertoire de sortie
paper-briefer input.zip -o ./analyse/

# Seulement le brief markdown (pour coller dans un LLM)
paper-briefer input.zip --brief-only

# Seulement le JSON structuré (pour usage programmatique)
paper-briefer input.zip --json-only
```

## Structure du projet

```text
paper-briefer/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md        <- template pour signaler un bug
│   │   └── feature_request.md   <- template pour proposer une fonctionnalité
│   ├── pull_request_template.md <- template pour les PR
│   └── workflows/
│       └── ci.yml               <- CI GitHub Actions (Python 3.10-3.13)
├── docs/
│   ├── design-decisions/
│   │   ├── 001-positioning.md   <- pourquoi "paper-briefer" (Option C)
│   │   ├── 002-extraction-priorities.md <- priorités d'extraction
│   │   └── 003-compression-validation.md <- protocole de validation
│   └── validation-test.md      <- résultats détaillés du test 5 questions
├── examples/
│   ├── README.md               <- source et contexte de l'exemple
│   ├── *-brief.md              <- brief généré (~4K tokens)
│   └── *-metadata.json         <- métadonnées structurées complètes
├── paper_briefer/
│   ├── __init__.py             <- version du package
│   ├── extract.py              <- moteur d'extraction (ZIP -> DocumentMetadata)
│   ├── brief.py                <- générateur de brief (DocumentMetadata -> markdown)
│   └── cli.py                  <- interface en ligne de commande
├── tests/
│   ├── test_extract.py         <- tests du moteur d'extraction
│   └── test_brief.py           <- tests du générateur de brief
├── .gitignore
├── .markdownlint.json          <- config du linter markdown
├── CHANGELOG.md                <- historique des versions
├── CLAUDE.md                   <- instructions pour assistants IA
├── CODE_OF_CONDUCT.md          <- code de conduite
├── CONTRIBUTING.md             <- guide de contribution
├── LICENSE                     <- licence MIT
├── pyproject.toml              <- configuration du package Python
├── README.md                   <- ce fichier
└── SECURITY.md                 <- politique de sécurité
```

### Couches d'extraction

Le moteur d'extraction opère en trois passes :

1. **Passe structurelle** (regex) : titres, table des matières, limites de pages, comptage de mots
2. **Passe sémantique** (regex + heuristiques) : légendes de figures, phrases d'ancrage, références croisées, densité de citations, limitations
3. **Passe intelligence** (prévue, optionnelle) : résumés de claims augmentés par LLM, typage des preuves

Les couches 1 et 2 ne nécessitent aucune clé API ni dépendance externe. La couche 3 sera optionnelle et utilisera l'API Claude pour une analyse sémantique plus profonde.

## Décisions de conception

Le positionnement et les fonctionnalités de cet outil ont été validés via deux sessions de LLM Council (5 conseillers indépendants + revue par les pairs + synthèse du chairman). Décisions clés documentées dans `docs/design-decisions/` :

- **Pourquoi "brief" plutôt que "résumé"** : un résumé perd la structure. Un brief préserve les relations interrogeables.
- **Pourquoi les figures en priorité** : les figures et tableaux concentrent la preuve d'un article. L'extraction caption + ancre donne 10x plus de ROI en compréhension que la détection de limites de sections.
- **Pourquoi les limitations comptent** : la seule question qui a échoué en validation portait sur les limitations. Les articles qui reconnaissent leurs faiblesses sont plus fiables, et les LLM ont besoin de ce signal.
- **Pourquoi pas l'analyse sémantique complète en v1** : l'extraction par regex à coût ~0 couvre 80% de la valeur. L'inférence LLM pour les graphes de claims représente les 20% restants à ~5$/article, réservé pour la v2.

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour la configuration de développement et les conventions.

## Licence

MIT
