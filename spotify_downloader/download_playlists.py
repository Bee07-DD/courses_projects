import json
import os
import subprocess
import sys
import re

def sanitize_filename(name):
    """Supprime les caractères non autorisés dans les noms de fichiers."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_track(track_name, artist_names, album_name, output_dir):
    """
    Tente de télécharger une piste avec plusieurs stratégies de recherche.
    """
    if isinstance(artist_names, list):
        artists = ", ".join(artist_names)
    else:
        artists = artist_names
        
    search_query = f"{artists} - {track_name} ({album_name})"
    filename = sanitize_filename(f"{artists} - {track_name}")
    output_path = os.path.join(output_dir, f"{filename}.%(ext)s")
    
    # Stratégie 1 : YouTube Music (Recherche précise)
    # Stratégie 2 : YouTube (Recherche classique)
    # On utilise yt-dlp qui est l'outil le plus robuste et gratuit.
    
    fallbacks = [
        f"ytsearch1:official audio {search_query}",
        f"ytsearch1:{search_query}",
        f"ytsearch1:{artists} {track_name}"
    ]
    
    success = False
    for query in fallbacks:
        print(f"  -> Tentative avec : {query}")
        try:
            command = [
                "yt-dlp",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "0",
                "--output", output_path,
                "--no-playlist",
                "--quiet",
                "--no-warnings",
                query
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  [SUCCÈS] Téléchargé : {filename}")
                success = True
                break
        except Exception as e:
            print(f"  [ERREUR] {e}")
            
    if not success:
        print(f"  [ÉCHEC] Impossible de télécharger : {search_query}")
    return success

def main(json_file):
    if not os.path.exists(json_file):
        print(f"Fichier {json_file} introuvable.")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    base_download_dir = "Downloads"
    if not os.path.exists(base_download_dir):
        os.makedirs(base_download_dir)

    for playlist_name, playlist_info in data.items():
        print(f"\nTraitement de la playlist : {playlist_name}")
        
        # Création du dossier pour la playlist
        playlist_dir = os.path.join(base_download_dir, sanitize_filename(playlist_name))
        if not os.path.exists(playlist_dir):
            os.makedirs(playlist_dir)
            
        tracks = playlist_info.get("tracks", [])
        total_tracks = len(tracks)
        
        for i, track in enumerate(tracks, 1):
            track_name = track.get("Track Name", "Unknown")
            artists = track.get("Artist Name(s)", "Unknown")
            album = track.get("Album Name", "Unknown")
            
            print(f"[{i}/{total_tracks}] Téléchargement de : {track_name} par {artists}...")
            download_track(track_name, artists, album, playlist_dir)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        json_path = "playlists.json"
    
    # Vérification de la présence de yt-dlp
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True)
    except FileNotFoundError:
        print("Erreur : 'yt-dlp' n'est pas installé. Veuillez l'installer avec 'pip install yt-dlp'.")
        sys.exit(1)
        
    main(json_path)
