# Spotify Playlist Downloader 

Ce projet Python fournit un outil modulaire pour télécharger des morceaux à partir de playlists Spotify. Il utilise l'API Spotify via `spotipy` pour extraire les informations des playlists et `spotDL` pour télécharger les fichiers audio correspondants (généralement depuis YouTube).

## Table des Matières

1.  [Fonctionnalités](#fonctionnalités)
2.  [Prérequis](#prérequis)
3.  [Installation](#installation)
4.  [Configuration de l'API Spotify](#configuration-de-lapi-spotify)
5.  [Utilisation](#utilisation)
6.  [Structure du Projet](#structure-du-projet)
7.  [Considérations Éthiques et Mentions Légales](#considérations-éthiques-et-mentions-légales)
8.  [Licence](#licence)

## 1. Fonctionnalités

*   Extraction des informations de playlist (nom, ID) depuis Spotify.
*   Récupération des URLs de tous les morceaux d'une playlist.
*   Téléchargement des morceaux individuels via `spotDL`.
*   Organisation des morceaux téléchargés par nom de playlist dans des dossiers séparés.
*   Architecture modulaire pour une meilleure maintenabilité et extensibilité.

## 2. Prérequis

Avant d'utiliser ce script, assurez-vous d'avoir les éléments suivants installés sur votre système :

*   **Python 3.x**
*   **pip** (gestionnaire de paquets Python)

## 3. Installation

1.  **Clonez le dépôt (ou téléchargez les fichiers) :**
    ```bash
    git clone https://github.com/votre_utilisateur/spotify-playlist-downloader-modular.git
    cd spotify-playlist-downloader-modular
    ```
    *(Note: Remplacez `votre_utilisateur/spotify-playlist-downloader-modular.git` par l'URL réelle de votre dépôt si vous le mettez sur GitHub, sinon, téléchargez simplement les fichiers.)*

2.  **Installez les dépendances Python :**
    ```bash
    pip install spotipy spotdl
    ```

## 4. Configuration de l'API Spotify

Pour interagir avec l'API Spotify, vous avez besoin d'un `Client ID` et d'un `Client Secret`. Suivez ces étapes pour les obtenir :

1.  Accédez au [Tableau de bord des développeurs Spotify](https://developer.spotify.com/dashboard).
2.  Connectez-vous avec votre compte Spotify.
3.  Cliquez sur « Create an app » (Créer une application).
4.  Donnez un nom et une description à votre application. Pour l'URI de redirection (Redirect URI), vous pouvez utiliser `http://localhost:8888/callback` (cette valeur n'est pas strictement utilisée pour l'authentification `Client Credentials` mais est souvent requise lors de la création de l'application).
5.  Une fois l'application créée, vous verrez votre « Client ID » et vous pourrez cliquer sur « Show Client Secret » pour obtenir votre « Client Secret ».
6.  **Créez un fichier `.env` à la racine du projet** et ajoutez-y ces variables :
    ```bash
    SPOTIPY_CLIENT_ID="votre_client_id"
    SPOTIPY_CLIENT_SECRET="votre_client_secret"
    ```
    Le script utilise `load_dotenv()` pour charger automatiquement ces valeurs depuis le fichier `.env`.

## 5. Utilisation

Pour exécuter le script, naviguez vers le répertoire du projet et exécutez `main.py`.

### Télécharger des playlists prédéfinies

Le fichier `main.py` contient une liste d'URLs de playlists par défaut. Vous pouvez modifier cette liste directement dans le script :

```python
# main.py
playlist_urls = [
    "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M", # Exemple: Top 50 Global
    # "https://open.spotify.com/playlist/VOTRE_AUTRE_PLAYLIST_ID",
]
```

Ensuite, exécutez le script :

```bash
python main.py
```

### Télécharger des playlists via les arguments de la ligne de commande

Vous pouvez également passer les URLs des playlists directement en arguments lors de l'exécution du script :

```bash
python main.py "https://open.spotify.com/playlist/VOTRE_PLAYLIST_URL_1" "https://open.spotify.com/playlist/VOTRE_PLAYLIST_URL_2"
```

Les morceaux téléchargés seront sauvegardés dans un dossier `Spotify_Downloads` à la racine du projet, avec des sous-dossiers pour chaque playlist.

## 6. Structure du Projet

```
spotify_downloader_modular/
├── main.py
├── spotify_api.py
├── downloader.py
└── README.md
```

*   `main.py`: Le point d'entrée principal du script. Il orchestre les appels aux modules `spotify_api` et `downloader`.
*   `spotify_api.py`: Contient la logique pour interagir avec l'API Spotify, y compris l'authentification et la récupération des informations de playlist et des URLs de morceaux.
*   `downloader.py`: Gère le processus de téléchargement des morceaux en utilisant `spotDL`.
*   `README.md`: Ce fichier, fournissant la documentation du projet.

## 7. Considérations Éthiques et Mentions Légales

Le téléchargement de contenu protégé par des droits d'auteur sans autorisation est illégal dans de nombreuses juridictions. Ce guide et les scripts sont fournis à des fins éducatives et de développement personnel uniquement. L'utilisateur est seul responsable de l'utilisation qu'il fait de ces outils et doit s'assurer de respecter les lois sur les droits d'auteur et les conditions d'utilisation de Spotify. Spotify propose des abonnements premium pour l'écoute hors ligne, qui est la méthode légale et recommandée pour profiter de la musique sans connexion internet.

## 8. Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. (Si vous souhaitez inclure un fichier de licence, créez-le séparément.)
