import subprocess
import re
from pathlib import Path

class MusicDownloader:
    def __init__(self, base_download_dir="Downloads"):
        self.base_dir = Path(base_download_dir)
        self.base_dir.mkdir(exist_ok=True)

    def sanitize(self, name):
        return re.sub(r'[\\/*?:"<>|]', "", str(name))

    def get_track_filename(self, track):
        name = track.get("Track Name", "Unknown")
        artists = track.get("Artist Name(s)", "Unknown")
        if isinstance(artists, list):
            artists = ", ".join(artists)
        return f"{self.sanitize(artists)} - {self.sanitize(name)}.mp3"

    def is_downloaded(self, playlist_name, track):
        playlist_dir = self.base_dir / self.sanitize(playlist_name)
        filename = self.get_track_filename(track)
        return (playlist_dir / filename).exists()

    def download(self, playlist_name, track, callback=None):
        playlist_dir = self.base_dir / self.sanitize(playlist_name)
        playlist_dir.mkdir(exist_ok=True)
        
        name = track.get("Track Name", "Unknown")
        artists = track.get("Artist Name(s)", "Unknown")
        if isinstance(artists, list):
            artists = ", ".join(artists)
            
        search_query = f"{artists} - {name}"
        output_template = str(playlist_dir / f"{self.sanitize(search_query)}.%(ext)s")
        
        if callback: callback(f"Recherche de {search_query}...")

        # Arguments de base pour le téléchargement
        base_cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--output", output_template,
            "--no-playlist",
            "--quiet",
            "--no-warnings"
        ]

        # Options additionnelles (métadonnées, pochette, sous-titres)
        # On utilise --ignore-errors pour que le téléchargement continue même si une option échoue
        extra_options = [
            "--add-metadata",
            "--embed-thumbnail",
            "--write-subs",
            "--all-subs",
            "--embed-subs",
            "--ignore-errors" 
        ]

        # Stratégies de recherche (fallback)
        queries = [
            f"ytsearch1:official audio {search_query}",
            f"ytsearch1:{search_query}"
        ]

        success = False
        for query in queries:
            try:
                cmd = base_cmd + extra_options + [query]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                # On vérifie si le fichier de sortie existe pour confirmer le succès
                expected_file = playlist_dir / self.get_track_filename(track)
                if expected_file.exists():
                    if callback: callback("Téléchargement réussi")
                    success = True
                    break
            except Exception as e:
                if callback: callback(f"Tentative échouée: {e}")
                continue
        
        if not success and callback:
            callback(f"Échec définitif pour {name}")
            
        return success
