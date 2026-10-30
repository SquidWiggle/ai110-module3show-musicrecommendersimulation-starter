from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    load_songs,
    score_song,
    recommend_songs,
    format_recommendation_card,
    format_recommendations,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_returns_list_of_dicts():
    songs = load_songs("data/songs.csv")
    assert isinstance(songs, list)
    assert len(songs) > 0
    assert isinstance(songs[0], dict)
    expected_keys = {
        "id", "title", "artist", "genre", "mood",
        "energy", "tempo_bpm", "valence", "danceability",
        "acousticness", "popularity", "duration_ms", "release_year",
    }
    assert expected_keys.issubset(songs[0].keys())


def test_load_songs_casts_numerical_types():
    song = load_songs("data/songs.csv")[0]

    # Discrete integer fields
    assert isinstance(song["id"], int)
    assert isinstance(song["popularity"], int)
    assert isinstance(song["duration_ms"], int)
    assert isinstance(song["release_year"], int)

    # Continuous float fields
    assert isinstance(song["energy"], float)
    assert isinstance(song["tempo_bpm"], float)
    assert isinstance(song["valence"], float)
    assert isinstance(song["danceability"], float)
    assert isinstance(song["acousticness"], float)

    # Categorical string fields
    assert isinstance(song["title"], str)
    assert isinstance(song["artist"], str)
    assert isinstance(song["genre"], str)
    assert isinstance(song["mood"], str)


def test_load_songs_from_isolated_csv(tmp_path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness,popularity,duration_ms,release_year\n"
        "99,Demo Song,Demo Artist,pop,happy,0.75,120.0,0.80,0.65,0.15,80,200000,2023\n"
    )
    result = load_songs(str(csv_file))
    assert len(result) == 1
    assert result[0] == {
        "id": 99,
        "title": "Demo Song",
        "artist": "Demo Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.75,
        "tempo_bpm": 120.0,
        "valence": 0.80,
        "danceability": 0.65,
        "acousticness": 0.15,
        "popularity": 80,
        "duration_ms": 200000,
        "release_year": 2023,
    }


def test_score_song_perfect_match_documents_scoring_breakdown():
    """
    Documents how score_song computes a maximum 10.0 score across all 5 components:
    1. Emotion (3.0 pts): exact mood (1.8) + valence proximity (1.2)
    2. Style (2.0 pts): genre (1.1) + rhythm/energy (0.6) + acoustic (0.3)
    3. Groove (2.0 pts): valence-gated danceability (2.0)
    4. Intensity (2.0 pts): energy (1.0) + tempo proximity (1.0)
    5. Discovery & Era (1.0 pt): popularity (0.5) + era proximity (0.5)
    """
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.9,
        "danceability": 0.8,
        "tempo": 120.0,
        "year": 2024,
        "likes_acoustic": False,
    }
    song = {
        "id": 1,
        "title": "Perfect Match Track",
        "artist": "Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 120.0,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.15,
        "popularity": 100,
        "duration_ms": 180000,
        "release_year": 2024,
    }

    score, reasons = score_song(user_prefs, song)

    assert score == 10.0
    assert len(reasons) == 10
    assert "mood match (+1.80)" in reasons
    assert "genre match (+1.10)" in reasons
    assert "groove match (+2.00)" in reasons


def test_score_song_mismatch_yields_low_score_and_omits_unmatched_reasons():
    """Documents how score_song penalizes mismatches and suppresses zero-point reasons."""
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "valence": 0.9,
        "danceability": 0.9,
        "tempo": 140.0,
        "year": 2024,
        "likes_acoustic": False,
    }
    mismatched_song = {
        "id": 2,
        "title": "Opposite Track",
        "artist": "Artist",
        "genre": "classical",
        "mood": "sad",
        "energy": 0.1,
        "tempo_bpm": 40.0,
        "valence": 0.1,
        "danceability": 0.1,
        "acousticness": 0.95,
        "popularity": 0,
        "duration_ms": 200000,
        "release_year": 2000,
    }

    score, reasons = score_song(user_prefs, mismatched_song)

    assert score < 2.0
    assert not any("mood match" in r for r in reasons)
    assert not any("genre match" in r for r in reasons)


def test_recommend_songs_documents_ranking_and_tuple_contract():
    """
    Documents the functional recommend_songs() specification:
    1. Input: user_prefs dict, songs list of dicts, and k integer limit.
    2. Scoring: evaluates every song using score_song(user_prefs, song).
    3. Output schema: List of tuples (song_dict, score_float, explanation_str).
    4. Ordering: sorted descending by score (highest match first).
    5. Slicing: returns at most top k results.
    """
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.9,
        "danceability": 0.8,
        "tempo": 120.0,
        "year": 2024,
        "likes_acoustic": False,
    }

    high_match_song = {
        "id": 1,
        "title": "High Match Track",
        "artist": "Artist A",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 120.0,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.15,
        "popularity": 100,
        "duration_ms": 180000,
        "release_year": 2024,
    }
    low_match_song = {
        "id": 2,
        "title": "Low Match Track",
        "artist": "Artist B",
        "genre": "classical",
        "mood": "sad",
        "energy": 0.2,
        "tempo_bpm": 60.0,
        "valence": 0.2,
        "danceability": 0.2,
        "acousticness": 0.9,
        "popularity": 10,
        "duration_ms": 240000,
        "release_year": 2000,
    }
    catalog = [low_match_song, high_match_song]

    # Request top 1
    recommendations = recommend_songs(user_prefs, catalog, k=1)

    # 1. Output length obeys k
    assert len(recommendations) == 1

    # 2. Output structure is (song_dict, score, explanation)
    top_song, top_score, explanation = recommendations[0]
    assert isinstance(top_song, dict)
    assert isinstance(top_score, float)
    assert isinstance(explanation, str)

    # 3. Best-matching song is ranked first despite catalog ordering
    assert top_song["id"] == 1
    assert top_score == 10.0
    assert "mood match" in explanation
    assert "genre match" in explanation


def test_recommend_songs_handles_boundary_cases():
    """Documents behavior with default k, catalog smaller than k, and empty catalog."""
    user_prefs = {"genre": "pop", "mood": "happy"}
    sample_song = {
        "id": 10,
        "title": "Solo Track",
        "artist": "Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.5,
        "tempo_bpm": 120.0,
        "valence": 0.5,
        "danceability": 0.5,
        "acousticness": 0.5,
        "popularity": 50,
        "duration_ms": 180000,
        "release_year": 2024,
    }

    # Catalog smaller than default k=5
    results = recommend_songs(user_prefs, [sample_song])
    assert len(results) == 1
    assert results[0][0]["id"] == 10

    # Empty catalog returns empty list
    assert recommend_songs(user_prefs, [], k=3) == []


def test_format_recommendation_card_contains_expected_fields():
    """Documents formatting layout: rank, title, artist, score, and sorted reasons."""
    song = {
        "title": "Cosmic Drift",
        "artist": "Starlight",
        "genre": "ambient",
        "mood": "calm",
        "release_year": 2023,
    }
    reasons = "mood match (+1.80), tempo match (+0.95)"
    card = format_recommendation_card(rank=1, song=song, score=8.75, reasons=reasons)

    assert "#1  Cosmic Drift — Starlight" in card
    assert "Score: 8.75 / 10.00" in card
    assert "Ambient • Calm • 2023" in card
    assert "+1.80  mood match" in card
    assert "+0.95  tempo match" in card


def test_format_recommendations_handles_empty_list():
    """Documents formatting with no recommendations."""
    assert format_recommendations([]) == ""


def test_score_song_case_insensitive_matching():
    """Validates that uppercase or whitespace in genre/mood matches catalog entries."""
    user_prefs = {"genre": " POP ", "mood": " Happy "}
    song = {
        "id": 1,
        "title": "Match",
        "artist": "Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.5,
        "tempo_bpm": 120.0,
        "valence": 0.5,
        "danceability": 0.5,
        "acousticness": 0.5,
        "popularity": 50,
        "duration_ms": 180000,
        "release_year": 2024,
    }
    _, reasons = score_song(user_prefs, song)
    assert any("mood match" in r for r in reasons)
    assert any("genre match" in r for r in reasons)



