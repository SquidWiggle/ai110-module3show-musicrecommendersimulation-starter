# Music Recommender Implementation Plan

## 1. Context & Objective
Implement a content-based music recommender in `src/recommender.py` evaluated against `tests/test_recommender.py` and `data/songs.csv`.

## 2. Agreed Multi-Feature Composite Scoring Model

Total Points Budget: **10.0 pts**

### 1. Emotion (3.5 pts)
- **`mood` (2.0 pts)**: Exact match (`song.mood == user.favorite_mood`).
- **`valence` (1.5 pts)**: Proximity: `1.5 * (1.0 - abs(target_val - song.valence))`.

### 2. Style (2.5 pts) - Multi-Feature Composite
*Style is not just a genre tag; it includes rhythmic and energy profile:*
- **Genre Tag (1.5 pts)**: `1.5 if song.genre == user.favorite_genre else 0.0`.
- **Style Profile (1.0 pt)**: Alignment in sonic space combining `danceability` and `energy` closeness:
  `1.0 * (1.0 - 0.5 * abs(target_dance - song.danceability) - 0.5 * abs(target_energy - song.energy))`.

### 3. Groove (2.0 pts) - Danceability Gated by Valence
*Groove requires rhythmic stability (`danceability`) locked to an exact emotional tone (`valence`):*
- **Base Groove**: Proximity to target `danceability`.
- **Valence Lock Multiplier**: If `abs(target_val - song.valence) <= 0.15`, full groove score is awarded. If valence drifts further, groove points are throttled:
  `groove_pts = 2.0 * (1.0 - abs(target_dance - song.danceability)) * max(0.0, 1.0 - 2.0 * abs(target_val - song.valence))`.

### 4. Intensity (2.0 pts) - Energy + Tempo Composite
*Physical loudness combined with speed:*
- **Energy (1.0 pt)**: `1.0 * (1.0 - abs(target_energy - song.energy))`.
- **Tempo BPM (1.0 pt)**: `1.0 * max(0.0, 1.0 - abs(target_bpm - song.tempo_bpm) / 100.0)`.

## 3. Files to Touch
1. `src/recommender.py`:
   - Implement `load_songs(csv_path)`: CSV reader returning song dictionaries or Song instances.
   - Implement `score_song(user_prefs, song)`: Returns `(score: float, reasons: List[str])`.
   - Implement `Recommender.recommend(user, k)`: Scores all songs, sorts descending, returns top $k$.
   - Implement `Recommender.explain_recommendation(user, song)`: Returns human-readable string explanation.
   - Implement `recommend_songs(user_prefs, songs, k)`: Functional API for script entry.
2. `tests/test_recommender.py`:
   - Run `pytest` to verify all test suites pass.

## 4. Next Concrete Step
In a fresh session: Open `notes/recommender-plan.md`, read the spec, and implement the methods in `src/recommender.py`.
