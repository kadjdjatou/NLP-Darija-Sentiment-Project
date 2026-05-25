# Collecte Multi-Plateformes de Données pour l'Analyse de Sentiment en Darija

Ce répertoire contient les outils et méthodologies utilisés pour constituer le corpus brut du projet. Nous avons adopté une approche multi-sources afin de capturer la diversité du dialecte marocain (Darija) sur les réseaux sociaux les plus populaires au Maroc : **YouTube** et **Instagram**.

## 📊 Aperçu de la Collecte
Le corpus total brut est composé de plus de **70 500 commentaires**, répartis comme suit :
* **YouTube** : ~70 000 commentaires (collecte automatisée via API).
* **Instagram** : 514 commentaires ciblés (collecte via Scraping).

---

## 📹 Source 1 : YouTube (Collecte via API)

### 📝 Présentation du Script
Le script Python exploite l'**API YouTube Data v3** pour extraire des données sous des vidéos publiées entre le **01/01/2025** et le **28/02/2026**.

### 🛠️ Fonctionnalités du Code
1.  **Identification des Chaînes (`get_channel_id`)** : Résolution des noms de chaînes en IDs uniques via une requête de recherche.
2.  **Filtrage Temporel (`get_videos`)** : Extraction exclusive des vidéos publiées dans la fenêtre 2025-2026.
3.  **Extraction Intelligente (`get_comments`)** : Récupération des textes, likes et dates avec gestion de la pagination (tokens).
4.  **Optimisation** : Dédoublonnage en temps réel via un ensemble (`set`) d'identifiants et respect des délais d'attente pour la stabilité de l'API.

### ⚖️ Logique de Plafonnage et Quotas (Pacing)
Le script intègre une logique de contrôle stricte pour garantir une distribution équilibrée des données et respecter les limites de l'API :

* **Plafond Global (`MAX_TOTAL_COMMENTS`)** : Limite la session à **60 000** commentaires pour éviter l'épuisement des quotas journaliers de la clé API.
* **Objectif par Chaîne (`TARGET_PER_CHANNEL`)** : Le script tente de collecter jusqu'à **20 000** commentaires par chaîne. Cela garantit qu'une seule chaîne très populaire ne domine pas l'ensemble du dataset.
* **Dynamique par Vidéo** : Pour chaque vidéo d'une chaîne, le script calcule le besoin restant (`remaining_for_channel`). Si une vidéo possède 5 000 commentaires mais que la chaîne a déjà atteint 19 500, le script n'extraira que les 500 derniers nécessaires avant de passer à la chaîne suivante.
* **Gestion des Doublons** : Avant la sauvegarde finale, une vérification par dictionnaire garantit l'unicité stricte de chaque `comment_id`.

### 🏢 Chaînes YouTube Ciblées
* **Actualités & Société** : Bladna 24, Rimal TV.
* **Vulgarisation & Tech** : Swinga, PILOTA.
* **Lifestyle & Humour** : SAFAA, BOTATO.

---

## 📸 Source 2 : Instagram (Collecte via Apify)

### 📝 Méthodologie
Pour compléter les données YouTube, nous avons extrait des commentaires issus de **Reels et publications Instagram** via la plateforme **Apify**. Cela permet de capturer un langage plus urbain et spontané.

### 👤 Comptes Instagram Sélectionnés
* **Médias** : Hesspress, i3lamtv.
* **Divertissement** : Simo Sedraty, Marouane53, oussamaqhiwa, marouanelamari.
* **Influenceurs** : samidghail1, Lallafatihaa, iamlilpatty, bilal.fraiha.
* **Éducation/Santé** : sehti.fid9i9a, othmane.safsafi.

---

## ⚙️ Configuration Technique Globale
* **Format de sortie** : JSON (UTF-8) pour préserver l'arabe, le tifinagh et les emojis.
* **Fenêtre temporelle** : Janvier 2025 à Février 2026.
* **Objectif de Diversité** : Couverture multi-thématique (politique, sport, humour, religion).

## 🚀 Installation & Utilisation (YouTube)
Installer la bibliothèque Google API :
```bash
pip install google-api-python-client