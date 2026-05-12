import pygame
from pathlib import Path
from PIL import Image
import io
import subprocess

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.is_playing = False
        self.current_track_path = None

    def load_and_play(self, file_path):
        if Path(file_path).exists():
            try:
                pygame.mixer.music.load(str(file_path))
                pygame.mixer.music.play()
                self.is_playing = True
                self.current_track_path = file_path
                return True
            except Exception as e:
                print(f"Erreur lecture: {e}")
                return False
        return False

    def toggle(self):
        if not self.current_track_path:
            return False
            
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
        return True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.current_track_path = None

    def get_pos(self):
        return pygame.mixer.music.get_pos() / 1000 if self.is_playing else 0

    def is_busy(self):
        return pygame.mixer.music.get_busy()

    def get_thumbnail(self, file_path):
        """Extrait la miniature intégrée dans le fichier MP3 en utilisant ffmpeg."""
        try:
            # Commande pour extraire l'image de couverture vers stdout
            cmd = [
                "ffmpeg", "-i", str(file_path),
                "-an", "-vcodec", "copy",
                "-f", "image2pipe", "-"
            ]
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0 and result.stdout:
                img_data = io.BytesIO(result.stdout)
                return Image.open(img_data)
        except Exception as e:
            print(f"Erreur extraction miniature: {e}")
        return None

    def get_lyrics(self, file_path):
        """Tente de trouver un fichier de sous-titres (.vtt, .srt) correspondant."""
        p = Path(file_path)
        # yt-dlp télécharge souvent en .vtt ou .srt avec le même nom de base
        potential_lyrics = list(p.parent.glob(f"{p.stem}.*"))
        for f in potential_lyrics:
            if f.suffix in [".vtt", ".srt", ".txt"]:
                try:
                    with open(f, "r", encoding="utf-8") as ly:
                        return ly.read()
                except:
                    continue
        return "Aucune parole disponible."
