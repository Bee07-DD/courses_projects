import sys
from spotify_api import SpotifyAPI
from downloader import Downloader
import os

def main():
    spotify_api = SpotifyAPI()
    downloader = Downloader()

    playlist_urls = [
        "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M", # Exemple: Top 50 Global
        # "https://open.spotify.com/playlist/VOTRE_AUTRE_PLAYLIST_ID",
    ]

    if len(sys.argv) > 1:
        playlist_urls = sys.argv[1:]

    if not playlist_urls:
        print("Veuillez fournir au moins une URL de playlist Spotify en argument ou modifier le script.")
        sys.exit(1)

    for url in playlist_urls:
        playlist_name, playlist_id = spotify_api.get_playlist_info(url)
        if playlist_name and playlist_id:
            track_urls = spotify_api.get_playlist_track_urls(playlist_id)
            downloader.download_tracks(track_urls, playlist_name)
        else:
            print(f"Skipping playlist: {url} due to error.")

    print("\nProcessus de téléchargement terminé.")

if __name__ == "__main__":
    main()