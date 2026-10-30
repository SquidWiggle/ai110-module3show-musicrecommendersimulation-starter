import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    duration_ms: int = 180000
    release_year: int = 2024

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_valence: float = 0.5
    target_danceability: float = 0.5
    target_tempo_bpm: float = 120.0
    target_year: int = 2022
    likes_acoustic: bool = False

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "popularity": int(row["popularity"]),
                "duration_ms": int(row["duration_ms"]),
                "release_year": int(row["release_year"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    fav_genre = user_prefs.get("favorite_genre", user_prefs.get("genre", ""))
    fav_mood = user_prefs.get("favorite_mood", user_prefs.get("mood", ""))
    target_energy = float(user_prefs.get("target_energy", user_prefs.get("energy", 0.5)))
    target_valence = float(user_prefs.get("likes_valence", user_prefs.get("valence", 0.5)))
    target_dance = float(user_prefs.get("target_danceability", user_prefs.get("danceability", 0.5)))
    target_bpm = float(user_prefs.get("target_tempo_bpm", user_prefs.get("tempo_bpm", user_prefs.get("tempo", 120.0))))
    target_year = int(user_prefs.get("target_year", user_prefs.get("year", 2024)))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))

    reasons: List[str] = []

    # 1. Emotion (max 3.0 pts)
    mood_pts = 1.8 if song.get("mood") == fav_mood else 0.0
    if mood_pts > 0:
        reasons.append(f"mood match (+{mood_pts:.2f})")

    valence_diff = abs(target_valence - float(song.get("valence", 0.5)))
    valence_pts = 1.2 * max(0.0, 1.0 - valence_diff)
    if valence_pts > 0:
        reasons.append(f"valence match (+{valence_pts:.2f})")

    # 2. Style (max 2.0 pts)
    genre_pts = 1.1 if song.get("genre") == fav_genre else 0.0
    if genre_pts > 0:
        reasons.append(f"genre match (+{genre_pts:.2f})")

    dance_diff = abs(target_dance - float(song.get("danceability", 0.5)))
    energy_diff = abs(target_energy - float(song.get("energy", 0.5)))
    rhythm_pts = 0.6 * max(0.0, 1.0 - 0.5 * dance_diff - 0.5 * energy_diff)
    if rhythm_pts > 0:
        reasons.append(f"rhythm & energy match (+{rhythm_pts:.2f})")

    target_acoustic = 0.85 if likes_acoustic else 0.15
    acoustic_diff = abs(target_acoustic - float(song.get("acousticness", 0.5)))
    acoustic_pts = 0.3 * max(0.0, 1.0 - acoustic_diff)
    if acoustic_pts > 0:
        reasons.append(f"acoustic texture match (+{acoustic_pts:.2f})")

    # 3. Groove (max 2.0 pts)
    groove_val_factor = max(0.0, 1.0 - 2.0 * valence_diff)
    groove_pts = 2.0 * max(0.0, 1.0 - dance_diff) * groove_val_factor
    if groove_pts > 0:
        reasons.append(f"groove match (+{groove_pts:.2f})")

    # 4. Intensity (max 2.0 pts)
    intensity_energy_pts = 1.0 * max(0.0, 1.0 - energy_diff)
    if intensity_energy_pts > 0:
        reasons.append(f"energy intensity match (+{intensity_energy_pts:.2f})")

    bpm_diff = abs(target_bpm - float(song.get("tempo_bpm", 120.0)))
    tempo_pts = 1.0 * max(0.0, 1.0 - bpm_diff / 100.0)
    if tempo_pts > 0:
        reasons.append(f"tempo match (+{tempo_pts:.2f})")

    # 5. Discovery & Era (max 1.0 pt)
    pop_pts = 0.5 * (float(song.get("popularity", 50)) / 100.0)
    if pop_pts > 0:
        reasons.append(f"popularity boost (+{pop_pts:.2f})")

    year_diff = abs(target_year - int(song.get("release_year", 2024)))
    era_pts = 0.5 * max(0.0, 1.0 - year_diff / 10.0)
    if era_pts > 0:
        reasons.append(f"era proximity match (+{era_pts:.2f})")

    total_score = (
        mood_pts
        + valence_pts
        + genre_pts
        + rhythm_pts
        + acoustic_pts
        + groove_pts
        + intensity_energy_pts
        + tempo_pts
        + pop_pts
        + era_pts
    )

    return round(total_score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
