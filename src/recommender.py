import csv
import re
from typing import List, Dict, Tuple, Optional, Union
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
        user_dict = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_valence": user.likes_valence,
            "target_danceability": user.target_danceability,
            "target_tempo_bpm": user.target_tempo_bpm,
            "target_year": user.target_year,
            "likes_acoustic": user.likes_acoustic,
        }
        scored = [
            (song, score_song(user_dict, vars(song))[0])
            for song in self.songs
        ]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_dict = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_valence": user.likes_valence,
            "target_danceability": user.target_danceability,
            "target_tempo_bpm": user.target_tempo_bpm,
            "target_year": user.target_year,
            "likes_acoustic": user.likes_acoustic,
        }
        _, reasons = score_song(user_dict, vars(song))
        return ", ".join(reasons) if reasons else "No specific matching criteria recorded."

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


def parse_reason(reason_str: str) -> Tuple[float, str, str]:
    """
    Parses a reason string like 'mood match (+1.80)' into (1.80, '+1.80', 'mood match').
    """
    match = re.search(r"\(\+?(-?\d+(?:\.\d+)?)\)", reason_str)
    if match:
        val = float(match.group(1))
        pts_str = f"+{val:.2f}" if val >= 0 else f"{val:.2f}"
        label = reason_str[: match.start()].strip()
        return val, pts_str, label
    return 0.0, "", reason_str.strip()


def format_recommendation_card(
    rank: int,
    song: Dict,
    score: float,
    reasons: Union[List[str], str],
    width: int = 80,
) -> str:
    """
    Formats a single song recommendation into a balanced 2-column card.
    """
    # 1. Normalize reasons
    if isinstance(reasons, str):
        raw_reasons = [r.strip() for r in reasons.split(",") if r.strip()]
    else:
        raw_reasons = list(reasons)

    parsed_reasons = [parse_reason(r) for r in raw_reasons]
    # Sort descending by impact
    parsed_reasons.sort(key=lambda x: x[0], reverse=True)

    # 2. Header
    title = song.get("title", "Untitled")
    artist = song.get("artist", "Unknown Artist")
    header_left = f"#{rank}  {title} — {artist}"
    header_right = f"Score: {score:.2f} / 10.00"

    if len(header_left) + len(header_right) + 2 > width:
        max_title_len = width - len(header_right) - len(artist) - 10
        if max_title_len > 10:
            title = title[: max_title_len - 3] + "..."
            header_left = f"#{rank}  {title} — {artist}"

    spacing = max(2, width - len(header_left) - len(header_right))
    header_line = f"{header_left}{' ' * spacing}{header_right}"

    # 3. Subtitle / metadata
    meta = []
    if song.get("genre"):
        meta.append(str(song["genre"]).title())
    if song.get("mood"):
        meta.append(str(song["mood"]).title())
    if song.get("release_year"):
        meta.append(str(song["release_year"]))
    meta_line = f"    {' • '.join(meta)}" if meta else ""

    # 4. Reasons in balanced 2-column layout
    reasons_lines = ["    Reasons:"]
    if not parsed_reasons:
        reasons_lines.append("      • No specific matching criteria recorded.")
    else:
        col_width = (width - 10) // 2
        for i in range(0, len(parsed_reasons), 2):
            val1, pts1, label1 = parsed_reasons[i]
            col1 = f"• {pts1}  {label1}" if pts1 else f"• {label1}"

            if i + 1 < len(parsed_reasons):
                val2, pts2, label2 = parsed_reasons[i + 1]
                col2 = f"• {pts2}  {label2}" if pts2 else f"• {label2}"
                line = f"      {col1:<{col_width}}  {col2}"
            else:
                line = f"      {col1}"
            reasons_lines.append(line)

    divider = "=" * width
    end_divider = "-" * width

    parts = [divider, header_line] if rank == 1 else [header_line]
    if meta_line:
        parts.append(meta_line)
    parts.extend(reasons_lines)
    parts.append(end_divider)
    return "\n".join(parts)


def format_recommendations(
    recommendations: List[Tuple[Dict, float, Union[List[str], str]]],
    width: int = 80,
) -> str:
    """
    Formats the list of recommendations into a clean terminal layout.
    """
    cards = [
        format_recommendation_card(rank, song, score, explanation, width=width)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1)
    ]
    return "\n".join(cards)

