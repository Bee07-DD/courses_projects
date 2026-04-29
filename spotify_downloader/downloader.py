import os
import subprocess

class Downloader:
    def __init__(self, download_folder="./Spotify_Downloads"):
        self.download_folder = download_folder
        os.makedirs(self.download_folder, exist_ok=True)

    def download_tracks(self, track_urls, playlist_name):
        if not track_urls:
            print("Aucun morceau à télécharger.")
            return

        output_path = os.path.join(self.download_folder, playlist_name.replace("/", "_"))
        os.makedirs(output_path, exist_ok=True)

        print(f"Téléchargement de {len(track_urls)} morceaux dans {output_path}...")
        
        for i, track_url in enumerate(track_urls):
            print(f"[{i+1}/{len(track_urls)}] Téléchargement de {track_url}...")
            try:
                command = ["spotdl", "download", track_url, "--output", output_path]
                subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"  Téléchargé: {track_url}")
            except subprocess.CalledProcessError as e:
                print(f"  Erreur lors du téléchargement de {track_url}: {e.stderr.decode().strip()}")
            except FileNotFoundError:
                print("  Erreur: spotdl n\'est pas trouvé. Assurez-vous qu\'il est installé et dans votre PATH.")
                break # Arrêter si spotdl n'est pas trouvé