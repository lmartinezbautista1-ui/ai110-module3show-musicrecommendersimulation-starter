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

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

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
    numeric_fields = ["id", "energy", "tempo_bpm", "valence", "danceability", "acousticness"]
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in numeric_fields:
                row[field] = float(row[field])
            row["id"] = int(row["id"])
            songs.append(row)
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm Recipe (max score = 9.0):
      - genre exact match:          +2.0
      - mood exact match:           +1.0
      - energy:   2.0 * (1 - |diff| / 0.5)
      - tempo:    1.0 * (1 - |diff| / 50)   (BPM tolerance of 50)
      - valence:  1.0 * (1 - |diff| / 0.5)
      - danceability: 0.5 * (1 - |diff| / 0.5)
      - acousticness: 1.0 * (1 - |diff| / 0.5)
    Numeric components are floored at 0. Each earned component adds a reason.
    """
    score = 0.0
    reasons: List[str] = []

    # Accept both naming conventions for the profile dict.
    fav_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    fav_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    t_energy = user_prefs.get("target_energy", user_prefs.get("energy"))
    t_tempo = user_prefs.get("target_tempo_bpm", user_prefs.get("tempo"))
    t_valence = user_prefs.get("target_valence", user_prefs.get("valence"))
    t_dance = user_prefs.get("target_danceability", user_prefs.get("danceability"))
    t_acoustic = user_prefs.get("target_acousticness", user_prefs.get("acousticness"))

    # Category matches
    if fav_genre is not None and song["genre"] == fav_genre:
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")
    if fav_mood is not None and song["mood"] == fav_mood:
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    # Numeric similarity, graded and floored at 0
    numeric_rules = [
        ("energy", "energy", 2.0, 0.5),
        ("tempo_bpm", "tempo_bpm", 1.0, 50.0),
        ("valence", "valence", 1.0, 0.5),
        ("danceability", "danceability", 0.5, 0.5),
        ("acousticness", "acousticness", 1.0, 0.5),
    ]
    targets = {
        "energy": t_energy,
        "tempo_bpm": t_tempo,
        "valence": t_valence,
        "danceability": t_dance,
        "acousticness": t_acoustic,
    }
    for song_field, target_key, max_pts, tolerance in numeric_rules:
        target = targets[target_key]
        if target is None:
            continue
        diff = abs(song[song_field] - target)
        pts = max_pts * max(0.0, 1.0 - diff / tolerance)
        if pts > 0.0:
            score += pts
            unit = "bpm" if song_field == "tempo_bpm" else ""
            reasons.append(
                f"{song_field} {song[song_field]:g}{unit} vs target {target:g}{unit} (+{pts:.1f})"
            )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    Expected return format: (song_dict, score, explanation)

    Ranking: descending score. Ties are broken by the song whose energy is
    closest to the user's energy target, then by stable CSV order.
    """
    t_energy = user_prefs.get("target_energy", user_prefs.get("energy"))

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        energy_diff = abs(song["energy"] - t_energy) if t_energy is not None else 0.0
        scored.append((score, -energy_diff, song, reasons))

    # Sort by score desc, then energy closeness desc (smaller diff first), stable for CSV order
    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)

    results = []
    for score, _neg_diff, song, reasons in scored[:k]:
        explanation = "; ".join(reasons) if reasons else "No preference matches"
        results.append((song, score, explanation))
    return results
