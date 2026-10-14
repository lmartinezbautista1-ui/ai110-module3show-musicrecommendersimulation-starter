"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    """Load the song catalog, score it against the taste profile, and print ranked recommendations."""
    songs = load_songs("data/songs.csv") 

    # Taste profile
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.50,
        "target_tempo_bpm": 90,
        "target_valence": 0.60,
        "target_danceability": 0.60,
        "target_acousticness": 0.70,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Terminal-friendly layout
    line = "-" * 62
    print(f"\nTop {len(recommendations)} recommendations\n{line}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank:>2}. {song['title']} — {song['artist']}")
        print(f"    [{song['genre']} / {song['mood']}]  Score: {score:.2f} / 9.00")
        if explanation:
            for reason in explanation.split("; "):
                print(f"      • {reason}")
        else:
            print("      • No preference matches")
        print(line)


if __name__ == "__main__":
    main()
