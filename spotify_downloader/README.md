#  Spotify Playlist Downloader

> Télécharge et écoute tes playlists Spotify exportées — sans API, sans abonnement payant.

Un outil Python avec interface graphique pour convertir tes playlists Spotify exportées en fichiers audio MP3 locaux, organisés par playlist, avec un lecteur audio intégré.

---

## Aperçu de l'interface


![Interface Spotify Downloader](/spotify_downloader/screeshots/preview.png)

---

## Table des Matières

1. [Prérequis](#1-prérequis)
2. [Installation](#2-installation)
3. [Workflow complet](#3-workflow-complet)
   - [Étape 1 — Exporter les playlists depuis Spotify](#étape-1--exporter-les-playlists-depuis-spotify)
   - [Étape 2 — Lancer l'application](#étape-2--lancer-lapplication)
   - [Étape 3 — Extraire les données CSV](#étape-3--extraire-les-données-csv)
   - [Étape 4 — Parcourir, télécharger et écouter](#étape-4--parcourir-télécharger-et-écouter)
4. [Architecture du projet](#4-architecture-du-projet)
5. [Fonctionnement interne](#5-fonctionnement-interne)
   - [Extraction (`extraction.py`)](#extraction-extractionpy)
   - [Téléchargement (`downloader.py`)](#téléchargement-downloaderpy)
   - [Lecture audio (`player.py`)](#lecture-audio-playerpy)
6. [Structure des dossiers de sortie](#6-structure-des-dossiers-de-sortie)
7. [Notes importantes](#7-notes-importantes)

---

## 1. Prérequis

- **Python 3.10+**
- **pip**
- **ffmpeg** (requis pour l'extraction des pochettes et la conversion audio)
- **yt-dlp** (téléchargement audio depuis YouTube / YouTube Music)

Vérifier les installations :

```bash
python3 --version
ffmpeg -version
yt-dlp --version
```

---

## 2. Installation

```bash
# Cloner le projet
git clone https://github.com/Bee07-DD/courses_projects/spotify_downloader
cd spotify_downloader

# Installer les dépendances Python
pip3 install customtkinter pillow pygame pandas yt-dlp
```

> **ffmpeg** doit être installé séparément selon ton OS :
> - Ubuntu/Debian : `sudo apt install ffmpeg`
> - macOS : `brew install ffmpeg`
> - Windows : [ffmpeg.org](https://ffmpeg.org/download.html)

---

## 3. Workflow complet

### Étape 1 — Exporter les playlists depuis Spotify

1. Rendez-vous sur **[Exportify](https://exportify.net/)** et connectez-vous avec votre compte Spotify.
2. Exportez vos playlists au format **CSV**.
3. Placez tous les fichiers `.csv` dans le dossier `SPFY_PLAYLISTS/` à la racine du projet.

```
spotify_downloader/
└── SPFY_PLAYLISTS/
    ├── Ma Playlist Rap.csv
    ├── BEST_OF_NF.csv
    └── ...
```

### Étape 2 — Lancer l'application

```bash
python3 main.py
```

L'interface graphique s'ouvre. Si un fichier `playlists.json` existe déjà, les playlists sont chargées automatiquement dans la barre latérale.

### Étape 3 — Extraire les données CSV

Cliquer sur **"Extraire CSV"** dans la sidebar. Le module `PlaylistExtractor` lit tous les `.csv` du dossier `SPFY_PLAYLISTS/`, génère `playlists.json` et rafraîchit automatiquement la liste des playlists.

### Étape 4 — Parcourir, télécharger et écouter

- **Sélectionner une playlist** dans la sidebar pour afficher ses pistes.
- Les pistes déjà téléchargées apparaissent en **vert** 🟢 avec un bouton **▶** pour lire.
- Les pistes non téléchargées ont un bouton **↓** pour lancer le téléchargement individuel.
- Le bouton **"Tout Télécharger"** (en haut à droite) lance le téléchargement séquentiel de toute la playlist.
- La **barre de lecture** en bas permet de jouer, mettre en pause, passer à la piste précédente ou suivante.
- Le **panneau latéral droit** affiche la pochette de l'album et les paroles/sous-titres si disponibles.

---

## 4. Architecture du projet

```
spotify_downloader/
├── main.py                  # Point d'entrée — interface graphique (customtkinter)
├── core/
│   ├── extraction.py        # Lecture des CSV et génération de playlists.json
│   ├── downloader.py        # Téléchargement audio via yt-dlp
│   └── player.py            # Lecture audio via pygame + extraction miniatures ffmpeg
├── SPFY_PLAYLISTS/          # Dossier des exports CSV Exportify
├── playlists.json           # Données structurées des playlists (généré automatiquement)
└── Downloads/               # Fichiers MP3 téléchargés (généré automatiquement)
```

---

## 5. Fonctionnement interne

### Extraction (`extraction.py`)

La classe `PlaylistExtractor` lit les fichiers CSV Exportify et extrait les colonnes utiles :

`Track URI`, `Track Name`, `Album Name`, `Artist Name(s)`, `Release Date`, `Duration (ms)`, `Popularity`, `Explicit`, `Genres`, `Record Label`

Les champs multi-valeurs (`Artist Name(s)`, `Genres`) sont automatiquement convertis en listes Python. Le résultat est sérialisé dans `playlists.json`.

### Téléchargement (`downloader.py`)

La classe `MusicDownloader` utilise `yt-dlp` en sous-processus avec les options suivantes :

- Format de sortie : **MP3**, qualité maximale (`--audio-quality 0`)
- Métadonnées intégrées : `--add-metadata`, `--embed-thumbnail`
- Sous-titres (paroles) : `--write-subs`, `--all-subs`, `--embed-subs`

**Stratégies de recherche (fallback) :**

| Ordre | Requête |
|-------|---------|
| 1 | `ytsearch1:official audio {Artiste} - {Titre}` |
| 2 | `ytsearch1:{Artiste} - {Titre}` |

Si la première stratégie ne produit pas de fichier, la suivante prend le relais. Le succès est confirmé en vérifiant l'existence du fichier de sortie attendu.

### Lecture audio (`player.py`)

La classe `AudioPlayer` utilise **pygame.mixer** pour la lecture MP3 et **ffmpeg** (via subprocess) pour extraire les pochettes intégrées dans les métadonnées. Les fichiers de paroles `.vtt`, `.srt` ou `.txt` portant le même nom de base que le MP3 sont automatiquement détectés et affichés dans le panneau de l'interface.

---

## 6. Structure des dossiers de sortie

```
Downloads/
├── BEST_OF_NF/
│   ├── NF - Mansion.mp3
│   ├── NF - The Search.mp3
│   └── ...
├── Ma Playlist Rap/
│   ├── Artiste X - Titre Y.mp3
│   └── ...
└── ...
```

Chaque playlist correspond à un sous-dossier dont le nom est assaini (caractères spéciaux supprimés).

---

## 7. Notes importantes

- **Légalité** : Ce projet est fourni à des fins personnelles et éducatives uniquement. Le téléchargement de contenu protégé par des droits d'auteur sans autorisation peut être illégal dans votre juridiction. L'utilisateur est seul responsable de l'utilisation qu'il en fait.
- **Qualité audio** : La meilleure qualité disponible est sélectionnée automatiquement par `yt-dlp`.
- **Fiabilité** : Les stratégies de fallback maximisent les chances de succès, mais certaines pistes peu diffusées peuvent rester introuvables.
- **Emojis** : Les emojis utilisés dans ce projet proviennent de [emojidb.org](https://emojidb.org).
- **Aucun outil payant** : Ce projet ne dépend d'aucune API payante (ni Spotify, ni autre service tiers).