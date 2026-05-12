import customtkinter as ctk
import os
import json
import threading
from pathlib import Path
from PIL import Image

# Importations des modules locaux
from core.extraction import PlaylistExtractor
from core.downloader import MusicDownloader
from core.player import AudioPlayer

class SpotifyToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Spotify_downloader - Outil de téléchargement et lecture de playlists Spotify")
        self.geometry("1200x850")

        # Initialisation des composants core
        self.extractor = PlaylistExtractor()
        self.downloader = MusicDownloader()
        self.player = AudioPlayer()

        # État de l'application
        self.playlists_data = {}
        self.current_playlist = None
        self.current_track_index = -1
        self.show_lyrics = False

        self.setup_ui()
        self.load_initial_data()

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="DOWNLOADER", font=("Arial", 22, "bold"), text_color="#1DB954").pack(pady=20)
        
        ctk.CTkButton(self.sidebar, text="Extraire CSV", command=self.on_extract, fg_color="#1DB954", hover_color="#17a34a").pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="Rafraîchir", command=self.load_initial_data).pack(pady=10, padx=20)
        
        ctk.CTkLabel(self.sidebar, text="Playlists", font=("Arial", 14, "bold")).pack(pady=(20, 10))
        self.playlist_list = ctk.CTkScrollableFrame(self.sidebar)
        self.playlist_list.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Main Content Area ---
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=0) # Pour le panneau latéral de lecture
        self.main.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(self.main, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        self.title_label = ctk.CTkLabel(header, text="Bienvenue", font=("Arial", 28, "bold"))
        self.title_label.pack(side="left")
        
        self.download_all_btn = ctk.CTkButton(header, text="Tout Télécharger", command=self.on_download_all, state="disabled")
        self.download_all_btn.pack(side="right")

        # Tracks View
        self.tracks_view = ctk.CTkScrollableFrame(self.main, label_text="Pistes")
        self.tracks_view.grid(row=1, column=0, sticky="nsew")

        # --- Visual Player Panel (Right Side) ---
        self.visual_panel = ctk.CTkFrame(self.main, width=350, corner_radius=15)
        self.visual_panel.grid(row=1, column=1, sticky="nsew", padx=(20, 0))
        self.visual_panel.grid_propagate(False)
        
        self.cover_label = ctk.CTkLabel(self.visual_panel, text="Pochette", width=300, height=300, fg_color="#2b2b2b", corner_radius=10)
        self.cover_label.pack(pady=20, padx=20)
        
        self.lyrics_view = ctk.CTkTextbox(self.visual_panel, width=300, height=300, corner_radius=10, fg_color="#1a1a1a")
        self.lyrics_view.pack(pady=10, padx=20, fill="both", expand=True)
        self.lyrics_view.insert("0.0", "Paroles / Sous-titres s'afficheront ici...")

        # --- Player Bar (Bottom) ---
        self.player_bar = ctk.CTkFrame(self, height=120, corner_radius=0, fg_color="#121212")
        self.player_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.player_bar.grid_columnconfigure(1, weight=1)

        self.track_info_frame = ctk.CTkFrame(self.player_bar, fg_color="transparent")
        self.track_info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.track_name_label = ctk.CTkLabel(self.track_info_frame, text="Aucun titre", font=("Arial", 14, "bold"))
        self.track_name_label.pack(anchor="w")
        self.track_artist_label = ctk.CTkLabel(self.track_info_frame, text="Artiste inconnu", font=("Arial", 12), text_color="gray")
        self.track_artist_label.pack(anchor="w")

        controls = ctk.CTkFrame(self.player_bar, fg_color="transparent")
        controls.grid(row=0, column=1)
        
        ctk.CTkButton(controls, text="⏮", width=45, height=45, corner_radius=22, command=self.on_prev).pack(side="left", padx=10)
        self.play_btn = ctk.CTkButton(controls, text="▶", width=55, height=55, corner_radius=27, fg_color="white", text_color="black", hover_color="#e6e6e6", command=self.on_toggle_play)
        self.play_btn.pack(side="left", padx=10)
        ctk.CTkButton(controls, text="⏭", width=45, height=45, corner_radius=22, command=self.on_next).pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(self.player_bar, text="Prêt", font=("Arial", 10), text_color="gray")
        self.status_label.grid(row=0, column=2, padx=20, pady=10, sticky="e")

        self.progress = ctk.CTkProgressBar(self.player_bar, progress_color="#1DB954", height=6)
        self.progress.grid(row=1, column=0, columnspan=3, sticky="ew", padx=30, pady=(0, 15))
        self.progress.set(0)
        
        self.update_loop()

    def load_initial_data(self):
        if Path("playlists.json").exists():
            with open("playlists.json", "r", encoding="utf-8") as f:
                self.playlists_data = json.load(f)
            self.refresh_playlist_sidebar()

    def refresh_playlist_sidebar(self):
        for w in self.playlist_list.winfo_children(): w.destroy()
        for name in sorted(self.playlists_data.keys()):
            ctk.CTkButton(self.playlist_list, text=name, fg_color="transparent", anchor="w", 
                          command=lambda n=name: self.on_select_playlist(n)).pack(fill="x", pady=2)

    def on_extract(self):
        def run():
            try:
                self.update_status("Extraction...")
                self.playlists_data = self.extractor.extract()
                self.after(0, self.refresh_playlist_sidebar)
                self.update_status("Extraction terminée")
            except Exception as e:
                self.update_status(f"Erreur: {e}")
        threading.Thread(target=run, daemon=True).start()

    def on_select_playlist(self, name):
        self.current_playlist = name
        self.title_label.configure(text=name)
        self.download_all_btn.configure(state="normal")
        self.refresh_tracks_view()

    def refresh_tracks_view(self):
        for w in self.tracks_view.winfo_children(): w.destroy()
        tracks = self.playlists_data[self.current_playlist].get("tracks", [])
        
        for i, track in enumerate(tracks):
            frame = ctk.CTkFrame(self.tracks_view, fg_color="transparent")
            frame.pack(fill="x", pady=2)
            
            is_dl = self.downloader.is_downloaded(self.current_playlist, track)
            color = "#1DB954" if is_dl else None
            
            t_name = track.get('Track Name', 'Unknown')
            t_artist = track.get('Artist Name(s)', 'Unknown')
            if isinstance(t_artist, list): t_artist = ", ".join(t_artist)

            ctk.CTkLabel(frame, text=f"{t_name} - {t_artist}", 
                         anchor="w", text_color=color).pack(side="left", padx=10, fill="x", expand=True)
            
            if is_dl:
                ctk.CTkButton(frame, text="▶", width=35, height=35, corner_radius=17, command=lambda idx=i: self.on_play(idx)).pack(side="right", padx=5)
            else:
                ctk.CTkButton(frame, text="⬇︎", width=35, height=35, corner_radius=17, command=lambda t=track: self.on_download(t)).pack(side="right", padx=5)

    def on_download(self, track):
        def run():
            self.downloader.download(self.current_playlist, track, self.update_status)
            self.after(0, self.refresh_tracks_view)
        threading.Thread(target=run, daemon=True).start()

    def on_download_all(self):
        tracks = self.playlists_data[self.current_playlist].get("tracks", [])
        def run():
            for t in tracks:
                if not self.downloader.is_downloaded(self.current_playlist, t):
                    self.downloader.download(self.current_playlist, t, self.update_status)
                    self.after(0, self.refresh_tracks_view)
            self.update_status("Tous les téléchargements terminés")
        threading.Thread(target=run, daemon=True).start()

    def on_play(self, index):
        self.current_track_index = index
        track = self.playlists_data[self.current_playlist]["tracks"][index]
        filename = self.downloader.get_track_filename(track)
        path = self.downloader.base_dir / self.downloader.sanitize(self.current_playlist) / filename
        
        if self.player.load_and_play(path):
            t_name = track.get('Track Name')
            t_artist = track.get('Artist Name(s)')
            if isinstance(t_artist, list): t_artist = ", ".join(t_artist)
            
            self.track_name_label.configure(text=t_name)
            self.track_artist_label.configure(text=t_artist)
            self.play_btn.configure(text="⏸")
            
            # Mise à jour visuelle (Pochette et Paroles)
            self.update_visuals(path)

    def update_visuals(self, path):
        # Miniature
        img = self.player.get_thumbnail(path)
        if img:
            img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
            self.cover_label.configure(image=img_ctk, text="")
        else:
            self.cover_label.configure(image=None, text="Pas de pochette")
        
        # Paroles
        lyrics = self.player.get_lyrics(path)
        self.lyrics_view.delete("0.0", "end")
        self.lyrics_view.insert("0.0", lyrics)

    def on_toggle_play(self):
        if self.player.toggle():
            self.play_btn.configure(text="⏸" if self.player.is_playing else "▶")

    def on_prev(self):
        if self.current_track_index > 0: self.on_play(self.current_track_index - 1)

    def on_next(self):
        if self.current_playlist and self.current_track_index < len(self.playlists_data[self.current_playlist]["tracks"]) - 1:
            self.on_play(self.current_track_index + 1)

    def update_status(self, msg):
        self.after(0, lambda: self.status_label.configure(text=msg))

    def update_loop(self):
        if self.player.is_playing:
            # Simulation de progression (pygame ne donne pas la durée totale facilement sans mutagen)
            self.progress.set((self.player.get_pos() % 200) / 200) 
            if not self.player.is_busy():
                self.on_next()
        self.after(1000, self.update_loop)

if __name__ == "__main__":
    app = SpotifyToolApp()
    app.mainloop()
