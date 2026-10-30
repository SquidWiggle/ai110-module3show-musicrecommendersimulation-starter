# Music Recommender Implementation Plan

## 1. Context & Objective
Implement a content-based music recommender in `src/recommender.py` evaluated against `tests/test_recommender.py` and `data/songs.csv`.

## 2. Updated Multi-Feature Composite Scoring Model

Total Points Budget: **10.0 pts**

### 1. Emotion (3.0 pts)
- **`mood` (1.8 pts)**: Exact match (`1.8 if song.mood == user.favorite_mood else 0.0`).
- **`valence` (1.2 pts)**: Proximity: `1.2 * (1.0 - abs(target_val - song.valence))`.

### 2. Style (2.0 pts) - Multi-Feature Composite
- **Genre Tag (1.1 pts)**: `1.1 if song.genre == user.favorite_genre else 0.0`.
- **Rhythm & Energy Profile (0.6 pt)**: `0.6 * (1.0 - 0.5 * abs(target_dance - song.danceability) - 0.5 * abs(target_energy - song.energy))`.
- **Acoustic Texture (0.3 pt)**: `0.3 * (1.0 - abs(target_acoustic - song.acousticness))` (where `target_acoustic = 0.85 if likes_acoustic else 0.15`).

### 3. Groove (2.0 pts) - Danceability Gated by Valence
- **Base Groove + Valence Lock**:
  `groove_pts = 2.0 * (1.0 - abs(target_dance - song.danceability)) * max(0.0, 1.0 - 2.0 * abs(target_val - song.valence))`.

### 4. Intensity (2.0 pts) - Energy + Tempo Composite
- **Energy (1.0 pt)**: `1.0 * (1.0 - abs(target_energy - song.energy))`.
- **Tempo BPM (1.0 pt)**: `1.0 * max(0.0, 1.0 - abs(target_bpm - song.tempo_bpm) / 100.0)`.

### 5. Discovery & Era (1.0 pt) - Popularity + Release Year
- **Popularity (0.5 pt)**: Normalized score: `0.5 * (song.popularity / 100.0)`.
- **Release Year (0.5 pt)**: Era closeness within a 10-year window:
  `0.5 * max(0.0, 1.0 - abs(target_year - song.release_year) / 10.0)`.

## 3. Implementation Steps
1. Update `UserProfile` in `src/recommender.py`: add default values (`target_year: int = 2022`, defaults for `likes_valence`, `target_danceability`, `target_tempo_bpm`) to resolve dataclass initialization errors.
2. Implement `load_songs(csv_path)` with CSV parsing into `Song` dataclasses and dictionaries.
3. Implement `score_song(user_prefs, song)` and explanation generator adhering to the 10.0 pt formula.
4. Implement `Recommender.recommend()` and `recommend_songs()`.
5. Run `PYTHONPATH=. pytest` to verify test suite passes.

## 4. Next Concrete Step
Implement updated `UserProfile` dataclass and `load_songs()` in `src/recommender.py`.
