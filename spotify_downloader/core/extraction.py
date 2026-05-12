import json
import pandas as pd
from pathlib import Path
import re

class PlaylistExtractor:
    def __init__(self, input_dir="SPFY_PLAYLISTS", output_json="playlists.json"):
        self.input_dir = Path(input_dir)
        self.output_json = Path(output_json)
        self.wanted_cols = [
            "Track URI", "Track Name", "Album Name", "Artist Name(s)",
            "Release Date", "Duration (ms)", "Popularity", "Explicit",
            "Genres", "Record Label"
        ]

    def split_list(self, value):
        if pd.isna(value):
            return None
        if isinstance(value, str):
            parts = [x.strip() for x in re.split(r",\s*|;\s*", value) if x.strip()]
            return parts if len(parts) > 1 else (parts[0] if parts else None)
        return value

    def extract(self):
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Dossier {self.input_dir} introuvable.")

        playlists = {}
        for csv_file in sorted(self.input_dir.glob("*.csv")):
            try:
                df = pd.read_csv(csv_file)
                tracks = []
                for _, row in df.iterrows():
                    track = {}
                    for col in self.wanted_cols:
                        if col in df.columns and not pd.isna(row[col]):
                            value = row[col]
                            if col in ["Artist Name(s)", "Genres"]:
                                value = self.split_list(value)
                            track[col] = value
                    if track:
                        tracks.append(track)
                
                playlists[csv_file.stem] = {
                    "source_csv": csv_file.name,
                    "track_count": len(tracks),
                    "tracks": tracks
                }
            except Exception as e:
                print(f"Erreur lors du traitement de {csv_file}: {e}")

        with open(self.output_json, "w", encoding="utf-8") as f:
            json.dump(playlists, f, ensure_ascii=False, indent=2)
        
        return playlists
