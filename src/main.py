"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, format_recommendations


def main() -> None:
    songs = load_songs("data/songs.csv")
    user_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "valence": 0.80,
            "danceability": 0.80,
            "tempo": 125,
            "year": 2023,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "valence": 0.60,
            "danceability": 0.55,
            "tempo": 75,
            "year": 2021,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "valence": 0.45,
            "danceability": 0.60,
            "tempo": 150,
            "year": 2019,
            "likes_acoustic": False,
        },
    }

    adversarial_profiles = {
        "Adversarial: The Sad Banger": {
            "genre": "metal",
            "mood": "sad",
            "energy": 0.90,
            "valence": 0.10,
            "danceability": 0.30,
            "tempo": 160,
            "year": 2020,
            "likes_acoustic": False,
        },
        "Adversarial: The Genre Hijack": {
            "genre": "rock",
            "mood": "happy",
            "energy": 0.80,
            "valence": 0.80,
            "danceability": 0.80,
            "tempo": 120,
            "year": 2022,
            "likes_acoustic": False,
        },
        "Adversarial: The Casing Trap": {
            "genre": "Pop",
            "mood": "Happy",
            "energy": 0.85,
            "valence": 0.80,
            "danceability": 0.80,
            "tempo": 125,
            "year": 2023,
            "likes_acoustic": False,
        },
        "Adversarial: The Dark Clubber": {
            "genre": "techno",
            "mood": "dark",
            "energy": 0.90,
            "valence": 0.05,
            "danceability": 0.95,
            "tempo": 138,
            "year": 2021,
            "likes_acoustic": False,
        },
        "Adversarial: Out-of-Bounds Exploit": {
            "genre": "pop",
            "mood": "happy",
            "energy": 999.0,
            "valence": -5.0,
            "danceability": 10.0,
            "tempo": 0,
            "year": 3000,
            "likes_acoustic": False,
        },
    }

    all_profiles = {**user_profiles, **adversarial_profiles}

    for profile_name, user_prefs in all_profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print("\n" + "=" * 80)
        print(f"  MUSIC RECOMMENDER — TOP RECOMMENDATIONS ({profile_name})")
        print(format_recommendations(recommendations))
    print()


if __name__ == "__main__":
    main()
