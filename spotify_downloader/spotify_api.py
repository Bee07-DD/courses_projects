import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

class SpotifyAPI:
    def __init__(self):
        load_dotenv()  # Charge les variables d'environnement depuis le fichier .env
        self.client_id = os.environ.get("SPOTIPY_CLIENT_ID")
        self.client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
        self.sp = self._authenticate()

    def _authenticate(self):
        if not self.client_id or not self.client_secret:
            print("Erreur: Les variables d'environnement SPOTIPY_CLIENT_ID et SPOTIPY_CLIENT_SECRET ne sont pas définies.")
            print("Veuillez les définir avant d'exécuter le script. Voir le README pour plus de détails.")
            sys.exit(1)
        try:
            auth_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
            return spotipy.Spotify(auth_manager=auth_manager)
        except Exception as e:
            print(f"Erreur d'authentification Spotipy: {e}")
            sys.exit(1)

    def get_playlist_info(self, playlist_url):
        try:
            playlist_id = playlist_url.split("/")[-1].split("?")[0]
            playlist = self.sp.playlist(playlist_id)
            return playlist["name"], playlist_id
        except Exception as e:
            print(f"Erreur lors de la récupération des informations de la playlist {playlist_url}: {e}")
            return None, None

    def get_playlist_track_urls(self, playlist_id):
        track_urls = []
        results = self.sp.playlist_items(playlist_id)
        tracks = results["items"]
        while results["next"]:
            results = self.sp.next(results)
            tracks.extend(results["items"])
        
        for item in tracks:
            track = item["track"]
            if track and track["external_urls"] and "spotify" in track["external_urls"]:
                track_urls.append(track["external_urls"]["spotify"])
        return track_urls