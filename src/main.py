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
    user_prefs = {"genre": "pop", 
                  "mood": "happy", 
                  "energy": 0.8, 
                  'valence': 0.6, 
                  'danceability': 0.67,
                  'tempo': 120,
                  'year': 2022,
                  'likes_acoustic': False}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 80)
    print("  MUSIC RECOMMENDER — TOP RECOMMENDATIONS")
    print(format_recommendations(recommendations))
    print()


if __name__ == "__main__":
    main()
