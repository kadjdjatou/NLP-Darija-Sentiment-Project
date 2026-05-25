# DATASET REPORT
## Darija YouTube Comments — Sentiment Analysis Dataset

**Version :** 1.0  
**Date :** 2025–2026  
**Groupes :** Groupe 1 & Groupe 2  

---

# 4. Contenu du Dataset

---

## 4.1 🌍 Sources des Données

### Plateforme utilisée

- **Plateforme :** YouTube
- **Méthode de collecte :** YouTube Data API v3 (scraping via API officielle)
- **Période de collecte :** Janvier 2025 — Février 2026
- **Langue cible :** Darija marocaine (arabe dialectal)

---

### Chaînes YouTube scrapées

| # | Chaîne | Thématique | Type de contenu |
|---|--------|-----------|----------------|
| 1 | Simo Sedraty | Divertissement / Humour | Vidéos comiques, challenges |
| 2 | i3lamtv | Politique / Actualités | Débats, interviews politiques |
| 3 | Kawalis | Critique / Société | Contenu critique, polémiques |
| 4 | Marouane53 | Humour / Lifestyle | Sketchs, vlogs |
| 5 | Raw Soueelt | Podcasts / Interviews | Discussions libres |
| 6 | Bladna 24 | Actualités | Informations quotidiennes |
| 7 | Rimal TV | Actualités / Société | Reportages, news |
| 8 | SAFAA | Divertissement | Contenu varié |
| 9 | Swinga | Musique / Culture | Clips, contenu musical |
| 10 | PILOTA | Humour / Divertissement | Vidéos courtes |
| 11 | BOTATO | Humour / Réseaux sociaux | Contenu viral |

---

### Pourquoi ces sources ?

Ces chaînes ont été sélectionnées pour les raisons suivantes :

**1. Diversité thématique :**
Les chaînes couvrent des thématiques variées
(humour, politique, actualités, musique, société)
afin d'obtenir un vocabulaire Darija riche et représentatif.
Un dataset provenant d'une seule thématique 
serait biaisé vers un type de sentiment.

**2. Richesse en sentiments négatifs :**
Les chaînes comme **SAFAA** et **Kawalis** 
sont connues pour générer des commentaires 
très engagés et souvent négatifs (critiques politiques, 
mécontentement social). 
Ce choix délibéré compense le déséquilibre naturel 
(les commentaires positifs étant plus fréquents sur YouTube).

**3. Authenticité de la Darija :**
Ces chaînes s'adressent à un public marocain 
qui commente naturellement en Darija pure, 
sans filtre ni formalisme. 
On y trouve les 3 formes d'écriture :
- Darija en **alphabet arabe** : "واعر بزاف"
- Darija en **Arabizi** (latin + chiffres) : "wa3r bzzaf"
- **Mixte** (arabe + latin) : "هاد الفيديو is top"

**4. Volume suffisant :**
Chaque chaîne génère des milliers de commentaires 
par vidéo, permettant d'atteindre l'objectif 
de 40 000+ commentaires par groupe.

**5. Période récente :**
Les vidéos de 2025–2026 reflètent 
la langue et les expressions actuelles 
utilisées sur les réseaux sociaux marocains.

---

---

### Observations sur la qualité des données

**Qualité générale :** Bonne, avec des défis spécifiques

**Problèmes rencontrés :**

| Problème | Description | Fréquence |
|---------|-------------|-----------|
| Emojis seuls | Commentaires composés uniquement d'emojis sans texte | Très fréquent |
| Spam | "Subscribe to my channel", liens publicitaires | Fréquent |
| Timestamps | Références au temps de la vidéo "10:17 😂" | Fréquent |
| Répétitions | "واااааعرة", "broooooo" (allongements expressifs) | Fréquent |
| Doublons | Même commentaire posté plusieurs fois | Modéré |
| MSA mélangé | Commentaires majoritairement en arabe standard | Modéré |
| Mentions | "@username tu as vu ça ?" | Fréquent |
| URLs | Liens YouTube, réseaux sociaux | Modéré |

**Avantages de ces sources :**

- ✅ Données **publiques** et légalement accessibles via l'API
- ✅ **Authenticité** : langue naturelle non filtrée
- ✅ **Volume** : milliers de commentaires par vidéo
- ✅ **Diversité** : plusieurs thématiques et styles d'expression
- ✅ **Métadonnées disponibles** : date, likes, auteur, ID vidéo
- ✅ **Représentativité** : reflète l'usage réel de la Darija en 2025-2026

---

## 4.2 Collecte et Nettoyage du Dataset

### Méthode de collecte

**Outil :** YouTube Data API v3 (Google)
**Bibliothèque Python :** google-api-python-client
**Format de stockage :** JSON

**Configuration de collecte utilisée :**

```python
MAX_TOTAL_COMMENTS = 60000
TARGET_PER_CHANNEL = 10000

DATE_START = "2025-01-01T00:00:00Z"
DATE_END   = "2026-02-28T23:59:59Z"
**Pour chaque commentaire collecté :**

{
  "comment_id": "UgwB-RyY85dLvW9WV6x4AaABAg",
  "text": "FLHL9A JAYA JIB BIMO SABIRI",
  "video_id": "8jK1_1Iya1U",
  "author": "@ABOUSALIHRayane",
  "date": "2026-02-22T12:43:08Z",
  "likes": 1,
  "channel": "Simo Sedraty"
}
**Processus de scraping :**
1. Recherche de l'ID de la chaîne par nom via l'API YouTube
2. Récupération des vidéos publiées entre janvier 2025 et février 2026

**Volume collecté :**
- Groupe 1 : ~70 000 commentaires bruts
- Groupe 2 : ~60 000 commentaires bruts
- **Total brut : ~130 000 commentaires**

## 4.2 🧹 Pipeline de Nettoyage et Prétraitement

Afin d'unifier les données des deux groupes, nous avons mis en place un pipeline de nettoyage rigoureux et décisionnel. L'objectif est de transformer un texte brut bruité en une entrée sémantique propre pour nos modèles de Machine Learning.

### 🧠 Notre Approche Décisionnelle
Plutôt qu'un simple nettoyage par suppression, nous utilisons un workflow qui évalue la structure de chaque commentaire :

1. **Filtrage de Surface** : Élimination immédiate du bruit (URLs, @mentions, #hashtags, timestamps) et des doublons exacts.
2. **Normalisations Linguistiques** :
   - **Arabe** : Unification des alphabets arabe (`أإآ` → `ا`) et de la (`ة` → `ه`) pour réduire la dispersion lexicale.
   - **Latin** : Réduction des élongations expressives (ex: `waaaaaw` → `waaw`) tout en gardant l'emphase émotionnelle (2 répétitions max).
3. **Détection Intelligente du Darija** :
   - Utilisation de **lexiques de racines dialectales** (+200 mots clés).
   - Détection morphologique des **préfixes verbaux** (`ka-`, `gh-`, `ta-`) et de la **double négation** (`ma...ch`).
   - Gestion de l'**Arabizi** via la validation des chiffres phonétiques (`3`, `7`, `9`, `2`).
4. **Conservation de la Polarité** :
   - **Crucial** : Nous avons conçu des listes de *stopwords* personnalisées qui **excluent les négations** (`ma`, `la`, `ch`, `machy`). 
   - *Justification* : Supprimer "ma" inverserait totalement le sentiment (ex: "ma mzyanch" deviendrait "mzyan").

### 📊 Impact du Nettoyage (Volume Unifié)

| Étape du Pipeline | Pourcentage de rétention | Justification du choix |
|:--- |:---:|:--- |
| **Données Brutes Unifiées** | 100% | Fusion des collectes des deux groupes (~130k) |
| **Suppression Bruit & Spam** | ~85% | Retrait des publicités et phrases génériques |
| **Filtrage Darija (Seuil 0.4)** | ~75% | Rejet du MSA (Arabe Classique) pour la pureté du dataset |
| **Dataset Final Exploitable** | **~70%** | **Qualité garantie pour l'apprentissage** |

## 4.3 🏷️ Annotation du Gold Dataset

### Création du Gold Dataset

Le **Gold Dataset** a été créé par **annotation manuelle** à l'aide de **Label Studio**.
Il contient **1 600 commentaires**, répartis entre les membres du groupe :

| Annotateur | Commentaires annotés |
|-----------|----------------------|
| Annotateur 1 | 500 |
| Annotateur 2 | 500 |
| Annotateur 3 | 600 |
| **Total** | **1 600** |

Chaque commentaire a été annoté une seule fois par un seul annotateur.
L'annotation n'a pas été croisée.

---

### Pourquoi ce Gold Dataset ?

Ce jeu annoté manuellement a servi à :

- définir des règles d'annotation claires et cohérentes ;
- construire une base de référence humaine fiable ;
- fournir des exemples équilibrés pour guider le LLM ;
- lancer correctement la phase de pré-annotation automatique.

Le Gold Dataset a été construit de manière **équilibrée** entre les trois classes avant d'être donné au LLM, afin d'éviter tout biais dans la pré-annotation.

---

### Outil utilisé : Label Studio

Label Studio est une plateforme d'annotation open source.
Nous l'avons utilisé pour :

- afficher chaque commentaire dans une interface claire ;
- sélectionner une seule classe par commentaire parmi les 3 ;
- exporter les annotations dans un format structuré (JSON) ;
- préparer le fichier final pour la phase LLM.

---

### Règles d'annotation

Chaque commentaire a été classé dans **une seule classe** :

**Positive :** appréciation, satisfaction, admiration, soutien.
> Exemples : `واعر بزاف` ، `مزيان` ، `3jbni bzzaf` ، `bravo`

**Negative :** critique, rejet, mécontentement, insulte, dégoût.
> Exemples : `خايب` ، `ما عجبنيش` ، `تفو` ، `حشومة`

**Neutral :** question, information factuelle, absence d'opinion claire.
> Exemples : `شكون هو هاد الشخص؟` ، `هاد الحلقة منين؟`

---

### Difficultés rencontrées

- **Commentaires très courts :** difficile de déterminer le sentiment.
- **Darija non standardisée :** un même mot peut s'écrire de plusieurs façons.
- **Mélange de langues :** certains commentaires mélangent Darija, français et Arabizi.
- **Sarcasme :** difficile à détecter sans contexte ni emojis.

---

### Conclusion

Le Gold Dataset de **1 600 commentaires** annoté manuellement avec Label Studio a constitué
une étape essentielle du projet.
Il a permis de définir les règles d'annotation, de construire une base équilibrée,
et de préparer les exemples nécessaires à la phase de labellisation semi-automatique par LLM.
## 4.4 🤖 Labellisation Semi-Automatique avec IA

**Méthode utilisée :**
Automatisation via interface web (Scripting / DOM Manipulation) utilisant l'extension **Tampermonkey** pour interagir directement avec l'environnement conversationnel du LLM, remplaçant ainsi l'usage classique d'une API payante.

**Nom exact du modèle utilisé :**
**Google Gemini 3.1 Pro** (via l'interface web Gemini Advanced).

**Description du processus :**
Pour relever le défi du volume de données (92 645 commentaires) et des limites de contexte du modèle, nous avons mis en place une architecture d'annotation automatisée et structurée en plusieurs étapes :

1. **Préparation et Découpage (Splitting) :** Le dataset global non annoté a été découpé au préalable en plusieurs sous-fichiers JSON (batches) de taille réduite. Cela nous a permis d'éviter les hallucinations du modèle liées à une surcharge de tokens et de garantir une qualité d'analyse constante.

2. **Ingénierie de Prompt (Few-Shot Prompting) :** Nous avons élaboré un prompt système strict imposant au modèle d'agir comme un expert en traitement du langage naturel spécialisé en Darija marocaine. Ce prompt contenait :
   - Des règles de classification strictes.
   - Des exemples concrets (Few-Shot) pour chaque classe (positif, négatif, neutre) afin d'illustrer les nuances culturelles, les expressions idiomatiques locales et les cas d'ironie.

3. **Automatisation via Tampermonkey (Le cœur du système) :** Nous avons développé deux scripts JavaScript personnalisés exécutés via Tampermonkey directement sur la page web de Gemini :
   - **Script d'Interface (Pop-up) :** Création d'une interface graphique (IHM) superposée sur le site de Gemini. Ce module nous permettait de charger séquentiellement nos sous-fichiers JSON locaux en quelques clics.
   - **Script d'Exécution :** Ce script injectait automatiquement le "System Prompt" suivi d'un batch de commentaires, déclenchait la requête, puis "écoutait" la réponse de l'IA pour extraire et formater uniquement le code JSON retourné (ID du commentaire + Label).

4. **Reconstruction :** Au fur et à mesure de l'exécution, les réponses étiquetées par Gemini 3.1 Pro étaient sauvegardées, puis finalement concaténées via un script Python que nous avons conçu pour reformer le dataset global de 92 645 lignes pré-annotées, prêt pour notre étape de vérification humaine.
# 4.5 🔍 Vérification et Validation

## Comment nous avons vérifié les labels

Nous avons mis en place un processus de contrôle qualité rigoureux en utilisant **Label Studio**, une plateforme professionnelle d'annotation de données. Ce processus nous a permis de valider ou de rectifier chaque étiquette produite par l'IA selon les critères suivants :

### 🔎 Relecture manuelle
Chaque commentaire a été lu par un annotateur humain afin d'évaluer sa pertinence linguistique (Darija marocaine) et sa clarté.

### ✅ Action de validation (Garder)
Un commentaire est conservé si :
- Il est écrit en Darija (ou Arabizi) compréhensible.
- Il n'est pas ambigu.
- Il ne contient pas d'insultes graves ou de contenus hors-sujet.
- Il n'est pas rédigé dans une langue totalement étrangère au contexte du dataset.

### ✏️ Correction des labels
Une fois le commentaire jugé valide, nous comparions le sentiment prédit par le LLM avec notre analyse humaine.  
- Si la réponse de l’IA était correcte, nous validions l’enregistrement.  
- Dans le cas contraire, nous modifiions manuellement le sentiment avant de passer au commentaire suivant.

### ❌ Action de rejet
Tout commentaire ne respectant pas les critères de qualité (bruit, langue incorrecte, ambiguïté totale) a été immédiatement rejeté du dataset final.

---

## 👥 Qui a vérifié ?

L'ensemble des membres de notre équipe de projet, agissant en tant qu'experts linguistiques natifs.  
Cette expertise humaine était cruciale pour interpréter correctement les nuances culturelles et les expressions idiomatiques propres au dialecte marocain.

---

## 🛠️ Méthode utilisée

La méthodologie a été structurée autour de l'interface de Label Studio :

### 🧩 Interface d'annotation
Configuration d'un projet de **"Text Classification"** dans Label Studio où les commentaires étaient présentés un par un avec les pré-annotations de Gemini 3.1 Pro.



### 📤 Audit et export
Après la session d'annotation, les données validées ont été exportées pour être utilisées dans les étapes suivantes du projet.

---

## 4.6 📊 Analyse des Erreurs de l’IA

Après comparaison entre les prédictions du LLM et la validation humaine, nous avons analysé les erreurs restantes afin de comprendre précisément les limites du modèle sur la Darija marocaine. Cette étape est importante, car elle montre que le modèle ne se trompe pas au hasard : ses erreurs suivent des schémas linguistiques récurrents.

### Types d’erreurs observées

- **Mauvaise classification** : le modèle attribue un mauvais label alors que le commentaire contient bien une opinion.
- **Ambiguïté** : le commentaire est trop court, elliptique ou dépend fortement du contexte de la vidéo.
- **Sarcasme / ironie** : le sens réel est opposé au sens littéral, ce qui reste difficile à détecter automatiquement.

### Exemples concrets observés dans notre analyse

Les erreurs les plus fréquentes concernent les commentaires courts, familiers, ou rédigés dans un mélange de Darija, Arabizi et français. Voici les cas les plus représentatifs :

#### 1) Confusion entre neutre et négatif
- **Commentaire** : `ba4i dir buz`
- **Prédiction du LLM** : Neutre
- **Validation humaine** : Négatif
- **Correction** : Neutre → Négatif

Ce type de commentaire est court et informel. Le modèle interprète souvent la structure comme un simple énoncé, alors qu’en contexte il exprime une critique directe.

#### 2) Sarcasme avec marqueurs d’intensité
- **Commentaire** : `bamou fiha wahed l3ya9a yaasalam z3ma rani kanakol sushi wfach l9at zaghba f plat bghat declari hh`
- **Prédiction du LLM** : Positif
- **Validation humaine** : Négatif
- **Correction** : Positif → Négatif

Ici, la présence de mots positifs ou d’un ton apparemment léger masque en réalité une moquerie. Le `l3ya9a,hh` final renforce l’ironie, mais le modèle reste sensible au sens littéral.

#### 3) Faux positif lié au rire ou à la répétition
- **Commentaire** : `hahahahhaha toma chofo reda wahabi kikan makayna la raghda la walo`
- **Prédiction du LLM** : Positif
- **Validation humaine** : Négatif
- **Correction** : Positif → Négatif

Le rire ne traduit pas ici une émotion positive ; il accompagne au contraire une critique ou un rejet. Ce type de signal est particulièrement fréquent dans les commentaires de YouTube.

#### 4) Formules mixtes et tonalité péjorative
- **Commentaire** : `sma7li 7amed o 7amed sorry`
- **Prédiction du LLM** : Neutre
- **Validation humaine** : Négatif
- **Correction** : Neutre → Négatif

Le mélange de mots arabizi et de français perturbe le modèle, qui classe parfois ce type de message comme simple formulation polie alors qu’il contient une intention négative.

#### 5) Commentaires très courts en Darija
- **Commentaire** : ` غبرات وماشي وغملات`
- **Prédiction du LLM** : Neutre
- **Validation humaine** : Négatif
- **Correction** : Neutre → Négatif

Ces cas sont difficiles car la phrase est très brève et dépend fortement du contexte conversationnel.

#### 6) Expression implicite et non littérale
- **Commentaire** : `  مو   علي امعني  عليا ليكايمعني سيمولايف `
- **Prédiction du LLM** : Neutre
- **Validation humaine** : Négatif
- **Correction** : Neutre → Négatif

Ce cas illustre bien une limite du modèle : il détecte la structure textuelle, mais peine à comprendre l’implicite et les nuances pragmatiques propres à la Darija orale.

### Conclusion de l’analyse des erreurs

Notre analyse montre que les erreurs sont principalement dues à trois facteurs :

1. **La brièveté des commentaires**, qui réduit les indices disponibles.
2. **Le mélange de langues**, très fréquent dans les commentaires YouTube marocains.
3. **Le sarcasme,l'ironie et l’implicite**, souvent plus importants que le sens littéral.

La confusion dominante reste **neutre ↔ négatif**

---

## 4.7 📈 Statistiques de Performance

Les chiffres ci-dessous proviennent de notre analyse finale dans le notebook final_analysis.ipynb et résument la qualité globale du processus LLM → vérification humaine sur un échantillon vérifié d’environ **63 000 commentaires**.

### Avant correction

- **Nombre total de commentaires comparés** : environ **63 000**
- **Nombre d’erreurs estimé** : environ **3 300**
- **Taux d’erreur global** : **5.18%**

### Après correction

- **Nombre corrigé manuellement** : l’ensemble des prédictions incorrectes détectées lors de la vérification
- **Qualité finale estimée** : **94.82% d’accuracy**
- **Taux d’erreur final** : **5.18%**

### Lecture des performances par classe

- **Négatif** : environ **92%** bien classée, avec des confusions principales vers le neutre.
- **Neutre** : environ **98%** bien classée, c’est la meilleure classe du modèle.
- **Positif** : environ **95%** bien classée, avec quelques erreurs vers le neutre lorsque le ton est implicite ou ironique.

### Analyse synthétique de la matrice de confusion

- La confusion dominante est **neutre ↔ négatif**.
- Les erreurs sur le **positif** apparaissent surtout dans les commentaires sarcastiques ou ambigus.
- Le modèle se comporte mieux sur les commentaires factuels ou clairement exprimés que sur les commentaires émotionnels, implicites ou mixtes.

### Conclusion de performance

Ces résultats confirment que notre méthode semi-automatique est fiable pour constituer un dataset final de grande taille. La correction humaine a permis de sécuriser les cas ambigus, de réduire les erreurs les plus visibles et de conserver un niveau de cohérence global élevé, adapté à une utilisation en analyse de sentiment sur la Darija marocaine.

---

## 4.8 🔧 Correction des Erreurs

Les erreurs détectées après la prédiction automatique n’ont pas été corrigées de manière mécanique ; elles ont été traitées par une vérification humaine structurée.

### Comment les erreurs ont été corrigées

- **Relecture humaine systématique** : chaque désaccord entre le LLM et l’annotation humaine a été réévalué manuellement.
- **Priorité au contexte linguistique** : nous avons privilégié le sens global du commentaire plutôt que la simple présence de mots positifs ou négatifs.
- **Gestion des cas ambigus** : lorsque le message était trop court ou dépendait du contexte, la correction se basait sur l’interprétation la plus cohérente avec la Darija marocaine.
- **Traitement du sarcasme** : les commentaires ironiques ont été corrigés avec attention, car le sens littéral ne correspond pas toujours au sentiment réel.

### Difficultés rencontrées

- **Commentaires très courts** : peu d’indices pour décider du sentiment.
- **Mélange de langues** : Darija, Arabizi et français dans un même message.
- **Sarcasme et ironie** : souvent difficiles à distinguer d’un commentaire réellement positif.
- **Formulations locales** : certaines expressions sont très contextuelles et ne suivent pas une syntaxe standard.

Cette étape de correction a permis d’augmenter la fiabilité finale du dataset et de réduire les erreurs les plus sensibles pour l’entraînement d’un modèle de sentiment.

---

## 4.9 📊 Statistiques du Dataset

Le dataset final a été construit à partir de la fusion des données des deux groupes, puis filtré et vérifié afin de conserver uniquement les exemples les plus exploitables.

### Nombre total d’exemples

- **Commentaires comparés dans l’analyse finale** : **83 397**
- **Commentaires vérifiés manuellement dans l’analyse détaillée** : environ **63 000**
- **Commentaires correctement classés** : **79 075**
- **Taux global de validation** : **94.82%**

### Répartition des classes

L’analyse exploratoire du dataset final montre une répartition globalement équilibrée entre les trois classes :

- **Positif** : légèrement dominant
- **Négatif** : très proche du positif
- **Neutre** : un peu moins représenté, mais toujours bien présent

Cette répartition est importante car elle limite le biais d’apprentissage et améliore la stabilité des modèles de classification.

### Problèmes de déséquilibre

Le dataset n’est pas parfaitement uniforme, mais le déséquilibre reste modéré.

- Les commentaires **positifs** sont souvent plus fréquents sur YouTube.
- Les commentaires **négatifs** apparaissent davantage sur certaines chaînes polémiques.
- La classe **neutre** est naturellement plus difficile à capter car elle dépend du contexte et des formulations courtes.

Nous avons donc conservé une distribution proche de l’équilibre, sans forcer artificiellement les classes, afin de préserver la réalité linguistique du corpus.

---

## 4.10 ⚠️ Limites

Même si le dataset final est solide, il présente certaines limites qu’il faut mentionner clairement.

### Biais des données

- Les données proviennent principalement de YouTube ; elles reflètent donc le style d’expression propre à cette plateforme.
- Certaines chaînes ont une tonalité plus polémique que d’autres, ce qui peut renforcer artificiellement la classe négative.
### Limites linguistiques

- La **Darija** n’est pas standardisée : un même mot peut être écrit de plusieurs façons.
- L’**Arabizi** ajoute une variabilité supplémentaire à cause des chiffres et des orthographes multiples.
- Le **mélange de langues** (Darija, arabe standard, français, anglais) complique la séparation nette entre les classes.
- Le **sarcasme** reste l’une des principales limites pour tout système automatique de sentiment.

### Limites du modèle IA

- Le modèle comprend bien les cas directs, mais reste moins robuste sur les formulations implicites.
- Les commentaires courts offrent peu de contexte pour une décision fiable.
- Les expressions culturelles locales peuvent être mal interprétées si elles ne sont pas explicitement vues pendant l’annotation.

Ces limites montrent que la validation humaine reste essentielle, surtout dans un contexte dialectal aussi riche et variable que la Darija marocaine.

---

## 4.11 🚀 Améliorations

Plusieurs pistes d’amélioration peuvent être envisagées pour renforcer la qualité du travail futur.

### Données

- Étendre la collecte à d’autres chaînes et formats de contenus.
- Ajouter davantage d’exemples rares, notamment pour les cas de sarcasme et d’ambiguïté.
### Annotation

- Mettre en place une double annotation sur une partie du corpus pour mesurer l’accord inter-annotateur.
- Formaliser davantage les règles de décision pour les cas limites.
- Construire un guide d’annotation plus détaillé pour harmoniser les décisions humaines.

### Modèle IA

- Tester des modèles plus spécialisés en dialectes ou en text classification multilingue.
- Intégrer des représentations contextuelles plus robustes pour mieux gérer le sarcasme.
- Combiner l’analyse par mots avec une approche par caractères pour mieux capter l’Arabizi.

### Perspective générale

Ces améliorations permettraient de réduire encore les erreurs sur les commentaires courts, implicites ou mixtes, tout en renforçant la généralisation du modèle sur de nouveaux contenus marocains.