from pathlib import Path
import pandas as pd
import json
import re

input_dir = Path("SPFY_PLAYLISTS")
output_json = Path("playlists.json")
output_summary = Path("playlists_summary.csv")

wanted_cols = [
    "Track URI", "Track Name", "Album Name", "Artist Name(s)",
    "Release Date", "Duration (ms)", "Popularity", "Explicit",
    "Added By", "Added At", "Genres", "Record Label",
    "Danceability", "Energy", "Key", "Loudness", "Mode",
    "Speechiness", "Acousticness", "Instrumentalness",
    "Liveness", "Valence", "Tempo", "Time Signature"
]

def split_list(value):
    if pd.isna(value):
        return None
    if isinstance(value, str):
        parts = [x.strip() for x in re.split(r",\s*|;\s*", value) if x.strip()]
        return parts if len(parts) > 1 else (parts[0] if parts else None)
    return value

playlists = {}

for csv_file in sorted(input_dir.glob("*.csv")):
    df = pd.read_csv(csv_file)
    tracks = []

    for _, row in df.iterrows():
        track = {}
        for col in wanted_cols:
            if col not in df.columns:
                continue
            value = row[col]
            if pd.isna(value):
                continue

            if col in ["Artist Name(s)", "Genres"]:
                value = split_list(value)

            track[col] = value

        if track:
            tracks.append(track)

    playlists[csv_file.stem] = {
        "source_csv": csv_file.name,
        "track_count": len(tracks),
        "tracks": tracks
    }

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(playlists, f, ensure_ascii=False, indent=2)

summary = pd.DataFrame([
    {"playlist": name, "source_csv": data["source_csv"], "track_count": data["track_count"]}
    for name, data in playlists.items()
])
summary.to_csv(output_summary, index=False)

print(f"JSON créé: {output_json}")
print(f"Résumé créé: {output_summary}")