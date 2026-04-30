# Téléchargeur de Playlists Spotify (sans API)

Ce projet fournit un script Python pour télécharger des pistes musicales à partir de playlists Spotify exportées, sans utiliser l'API Spotify ni aucune autre API payante. Il s'appuie sur `yt-dlp` pour extraire l'audio de sources publiques comme YouTube et YouTube Music, en offrant plusieurs stratégies de recherche (fallbacks) pour maximiser les chances de succès. Les musiques téléchargées sont organisées automatiquement dans des dossiers distincts pour chaque playlist.

## Table des Matières

1.  [Prérequis](#1-prérequis)
2.  [Génération du fichier `playlists.json`](#2-génération-du-fichier-playlistsjson)
3.  [Utilisation du script `download_playlists.py`](#3-utilisation-du-script-download_playlistspy)
    *   [Description](#description)
    *   [Installation des dépendances](#installation-des-dépendances)
    *   [Exécution](#exécution)
    *   [Stratégies de Fallback](#stratégies-de-fallback)
    *   [Structure des dossiers de sortie](#structure-des-dossiers-de-sortie)
4.  [Notes Importantes](#4-notes-importantes)

## 1. Prérequis

Pour utiliser ce script, vous devez avoir les éléments suivants installés sur votre système :

*   **Python 3.x** : Le script est écrit en Python.
*   **pip** : Le gestionnaire de paquets pour Python, généralement inclus avec Python 3.x.
*   **yt-dlp** : Un outil en ligne de commande pour télécharger des vidéos et de l'audio à partir de nombreux sites web. Il est utilisé par le script pour effectuer les téléchargements.

Vous pouvez vérifier si Python et pip sont installés en ouvrant un terminal et en tapant :

```bash
python3 --version
pip3 --version
```

Si `yt-dlp` n'est pas installé, vous pouvez le faire via pip :

```bash
pip3 install yt-dlp
```

## 2. Génération du fichier `playlists.json`

Le script `download_playlists.py` s'appuie sur un fichier `playlists.json` qui contient les informations détaillées de vos playlists Spotify. Ce fichier est généré à partir de fichiers CSV exportés via **Exportify**.

Voici le processus général :

1.  **Exportez vos playlists Spotify avec Exportify** : Rendez-vous sur [Exportify](https://exportify.net/) et suivez les instructions pour exporter vos playlists au format CSV. Enregistrez tous les fichiers CSV dans un dossier dédié.
2.  **Utilisez le script `extract.py`** : Ce script lit les fichiers CSV situés dans `SPFY_PLAYLISTS/` et génère `playlists.json` ainsi que `playlists_summary.csv`.

Le fichier `playlists.json` doit avoir la structure suivante (exemple simplifié) :

```json
{
  "Nom de la Playlist 1": {
    "source_csv": "Nom_de_la_Playlist_1.csv",
    "track_count": 10,
    "tracks": [
      {
        "Track Name": "Titre de la Chanson 1",
        "Artist Name(s)": "Artiste 1",
        "Album Name": "Album 1"
      },
      {
        "Track Name": "Titre de la Chanson 2",
        "Artist Name(s)": ["Artiste 2", "Artiste 3"],
        "Album Name": "Album 2"
      }
    ]
  },
  "Nom de la Playlist 2": {
    // ... autres pistes
  }
}
```

## 3. Utilisation du script `download_playlists.py`

### Description

Le script `download_playlists.py` lit le fichier `playlists.json`, itère sur chaque playlist et chaque piste, puis tente de télécharger l'audio correspondant en utilisant `yt-dlp`. Il gère les noms de fichiers et de dossiers pour éviter les caractères non valides et organise les téléchargements.

### Installation des dépendances

Assurez-vous que `yt-dlp` est installé comme mentionné dans la section [Prérequis](#1-prérequis).

### Exécution

Pour exécuter le script, placez le fichier `download_playlists.py` et votre fichier `playlists.json` (généré précédemment) dans le même répertoire. Ensuite, ouvrez un terminal dans ce répertoire et exécutez la commande suivante :

```bash
python3 download_playlists.py [chemin/vers/playlists.json]
```

Si `playlists.json` se trouve dans le même répertoire que le script, vous pouvez simplement exécuter :

```bash
python3 download_playlists.py
```

Le script affichera la progression du téléchargement dans le terminal.

### Stratégies de Fallback

Le script utilise une approche de fallback pour trouver et télécharger les pistes. Pour chaque piste, il essaie les requêtes de recherche suivantes dans l'ordre :

1.  `ytsearch1:official audio {Artiste(s)} - {Titre de la Chanson} ({Nom de l'Album})` : Tente de trouver la version audio officielle sur YouTube Music.
2.  `ytsearch1:{Artiste(s)} - {Titre de la Chanson} ({Nom de l'Album})` : Recherche générale sur YouTube avec les détails complets.
3.  `ytsearch1:{Artiste(s)} {Titre de la Chanson}` : Recherche plus large sur YouTube si les précédentes échouent.

Si une recherche réussit, le téléchargement est effectué et le script passe à la piste suivante. Si toutes les stratégies échouent pour une piste, un message d'échec est affiché, et le script continue avec la piste suivante.

### Structure des dossiers de sortie

Toutes les musiques téléchargées seront enregistrées dans un dossier `Downloads` créé à la racine du projet. À l'intérieur de ce dossier, un sous-dossier sera créé pour chaque playlist, portant le nom de la playlist (sanitized). Par exemple :

```
./
├── download_playlists.py
├── playlists.json
└── Downloads/
    ├── BEST_OF_NF🔥🖤/
    │   ├── NF - Thing Called Love.mp3
    │   ├── NF - Mansion.mp3
    │   └── ...
    ├── Ma Super Playlist/
    │   ├── Artiste X - Titre Y.mp3
    │   └── ...
    └── ...
```

## 4. Notes Importantes

*   **Qualité Audio** : Le script télécharge l'audio avec la meilleure qualité disponible (`--audio-quality 0` de `yt-dlp`), généralement au format MP3.
*   **Légalité** : Le téléchargement de contenu protégé par des droits d'auteur sans autorisation peut être illégal dans votre juridiction. Ce script est fourni à des fins éducatives et personnelles uniquement. L'utilisateur est seul responsable de l'utilisation qu'il en fait.
*   **Fiabilité** : Bien que les stratégies de fallback augmentent les chances de succès, il n'est pas garanti que toutes les pistes soient trouvées et téléchargées, notamment si elles ne sont pas disponibles sur les plateformes de streaming vidéo publiques.
*   **Nommage des fichiers** : Les noms de fichiers sont nettoyés pour supprimer les caractères spéciaux, mais des problèmes peuvent survenir avec des noms de pistes ou d'artistes très complexes. Si un téléchargement échoue, vérifiez le nom de la piste dans le fichier JSON.

## Fonctionnalités complémentaires

*   Génération automatique de `playlists.json` depuis des exports CSV Spotify.
*   Organisation des téléchargements par playlist.
*   Succession de requêtes de recherche pour améliorer la robustesse.
*   Archivage des métadonnées de chaque playlist dans `playlists_summary.csv`.

## Objectif du projet

Ce projet répond au besoin d'écoute hors ligne en transformant des playlists Spotify exportées en fichiers audio locaux, sans dépendre d'API externes payantes. Il offre un workflow simple et autonome, facilement personnalisable pour des usages personnels.
