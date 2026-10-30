from src.recommender import Song, UserProfile, Recommender, load_songs

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
