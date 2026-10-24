# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version of this project is a small content-based music recommender that loads a catalog of songs from a CSV file and ranks them for a listener described by a taste profile. The profile stores a favorite genre and mood plus target values for energy, tempo, valence, danceability, and acousticness. Each song is scored out of a maximum of 9.0 by adding points for an exact genre match and for graded, numeric closeness on each audio feature (the farther a song's value is from the user's target, the fewer points it earns, with components floored at zero). The system then sorts all songs from highest to lowest score — breaking ties by which song's energy is closest to the target — and recommends the top five, printing a point-by-point explanation for every recommendation so a reader can see exactly why each song was chosen. I also ran the recommender for several different listener profiles (lofi/chill, lofi/focused, rock/intense, and jazz/relaxed) to see how the same scoring rule adapts to different tastes, and noted where it leans too heavily on genre and on categories that are common in the catalog.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Each Song in my system has features such as genre, mood, energy, and tempo. The UserProfile stores the listener’s favorite genres and artists, preferred moods and energy levels, and listening history, such as liked or recently played songs. The Recommender compares a song’s features with the user’s preferences, adds points for matches, and adjusts the score based on listening history. It then sorts songs from highest to lowest score and recommends the top-scoring songs




Algorithm Recipe: Song Scoring
Give each song a score from 0 to 100 based on how well it fits the listener’s current needs and preferences.
1. Start with a baseline of 50 points.
2. Add points for preference matches:
   - Genre match: +20
   - Artist match: +15
   - Mood match: +15
   - Tempo or energy match: +10
3. Adjust for the current context:
   - Fits the requested activity or setting: +10
   - Fits the time of day: +5
4. Use listening history:
   - Played often recently: −5 to −15, depending on how frequently
   - Liked or saved before: +5
   - Skipped before: −10
5. Keep the score between 0 and 100.
Rule: Give more weight to what the listener asked for right now than to general listening history. If two songs tie, choose the one that better matches the requested mood or activity

Note: One potential bias is that exact genre or mood matches could receive so many points that they outweigh the song’s other qualities. This might cause the recommender to overlook a song that fits the user’s energy, tempo, and mood well but has a different genre. The system may also favor genres and moods that appear more often in the CSV, since it has fewer examples of less common categories.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```
Top 5 recommendations
--------------------------------------------------------------
 1. Midnight Coding — LoRoom
    [lofi / chill]  Score: 7.82 / 9.00
      • genre match: lofi (+2.0)
      • mood match: chill (+1.0)
      • energy 0.42 vs target 0.5 (+1.7)
      • tempo_bpm 78bpm vs target 90bpm (+0.8)
      • valence 0.56 vs target 0.6 (+0.9)
      • danceability 0.62 vs target 0.6 (+0.5)
      • acousticness 0.71 vs target 0.7 (+1.0)
--------------------------------------------------------------
 2. Library Rain — Paper Lanterns
    [lofi / chill]  Score: 7.20 / 9.00
      • genre match: lofi (+2.0)
      • mood match: chill (+1.0)
      • energy 0.35 vs target 0.5 (+1.4)
      • tempo_bpm 72bpm vs target 90bpm (+0.6)
      • valence 0.6 vs target 0.6 (+1.0)
      • danceability 0.58 vs target 0.6 (+0.5)
      • acousticness 0.86 vs target 0.7 (+0.7)
--------------------------------------------------------------
 3. Focus Flow — LoRoom
    [lofi / focused]  Score: 6.72 / 9.00
      • genre match: lofi (+2.0)
      • energy 0.4 vs target 0.5 (+1.6)
      • tempo_bpm 80bpm vs target 90bpm (+0.8)
      • valence 0.59 vs target 0.6 (+1.0)
      • danceability 0.6 vs target 0.6 (+0.5)
      • acousticness 0.78 vs target 0.7 (+0.8)
--------------------------------------------------------------
 4. Dust Road Hymn — Harlan Jeeters
    [country / romantic]  Score: 4.65 / 9.00
      • energy 0.55 vs target 0.5 (+1.8)
      • tempo_bpm 102bpm vs target 90bpm (+0.8)
      • valence 0.72 vs target 0.6 (+0.8)
      • danceability 0.57 vs target 0.6 (+0.5)
      • acousticness 0.63 vs target 0.7 (+0.9)
--------------------------------------------------------------
 5. Velvet Hourglass — Seraphine Cole
    [R&B / romantic]  Score: 4.42 / 9.00
      • energy 0.58 vs target 0.5 (+1.7)
      • tempo_bpm 88bpm vs target 90bpm (+1.0)
      • valence 0.7 vs target 0.6 (+0.8)
      • danceability 0.68 vs target 0.6 (+0.4)
      • acousticness 0.48 vs target 0.7 (+0.6)
```

### Additional profile runs

**focus_listener** (lofi / focused)

```text
Top 5 recommendations
--------------------------------------------------------------
 1. Focus Flow — LoRoom
    [lofi / focused]  Score: 8.26 / 9.00
      • genre match: lofi (+2.0)
      • mood match: focused (+1.0)
      • energy 0.4 vs target 0.4 (+2.0)
      • tempo_bpm 80bpm vs target 80bpm (+1.0)
      • valence 0.59 vs target 0.55 (+0.9)
      • danceability 0.6 vs target 0.5 (+0.4)
      • acousticness 0.78 vs target 0.75 (+0.9)
--------------------------------------------------------------
 2. Midnight Coding — LoRoom
    [lofi / chill]  Score: 7.16 / 9.00
      • genre match: lofi (+2.0)
      • energy 0.42 vs target 0.4 (+1.9)
      • tempo_bpm 78bpm vs target 80bpm (+1.0)
      • valence 0.56 vs target 0.55 (+1.0)
      • danceability 0.62 vs target 0.5 (+0.4)
      • acousticness 0.71 vs target 0.75 (+0.9)
--------------------------------------------------------------
 3. Library Rain — Paper Lanterns
    [lofi / chill]  Score: 6.74 / 9.00
      • genre match: lofi (+2.0)
      • energy 0.35 vs target 0.4 (+1.8)
      • tempo_bpm 72bpm vs target 80bpm (+0.8)
      • valence 0.6 vs target 0.55 (+0.9)
      • danceability 0.58 vs target 0.5 (+0.4)
      • acousticness 0.86 vs target 0.75 (+0.8)
--------------------------------------------------------------
 4. Paper Lantern Waltz — June and the Foxes
    [folk / dreamy]  Score: 4.59 / 9.00
      • energy 0.31 vs target 0.4 (+1.6)
      • tempo_bpm 84bpm vs target 80bpm (+0.9)
      • valence 0.58 vs target 0.55 (+0.9)
      • danceability 0.35 vs target 0.5 (+0.3)
      • acousticness 0.88 vs target 0.75 (+0.7)
--------------------------------------------------------------
 5. Coffee Shop Stories — Slow Stereo
    [jazz / relaxed]  Score: 4.54 / 9.00
      • energy 0.37 vs target 0.4 (+1.9)
      • tempo_bpm 90bpm vs target 80bpm (+0.8)
      • valence 0.71 vs target 0.55 (+0.7)
      • danceability 0.54 vs target 0.5 (+0.5)
      • acousticness 0.89 vs target 0.75 (+0.7)
```

**workout_listener** (rock / intense)

```text
Top 5 recommendations
--------------------------------------------------------------
 1. Storm Runner — Voltline
    [rock / intense]  Score: 7.74 / 9.00
      • genre match: rock (+2.0)
      • mood match: intense (+1.0)
      • energy 0.91 vs target 0.9 (+2.0)
      • tempo_bpm 152bpm vs target 145bpm (+0.9)
      • valence 0.48 vs target 0.7 (+0.6)
      • danceability 0.66 vs target 0.8 (+0.4)
      • acousticness 0.1 vs target 0.1 (+1.0)
--------------------------------------------------------------
 2. Gym Hero — Max Pulse
    [pop / intense]  Score: 5.80 / 9.00
      • mood match: intense (+1.0)
      • energy 0.93 vs target 0.9 (+1.9)
      • tempo_bpm 132bpm vs target 145bpm (+0.7)
      • valence 0.77 vs target 0.7 (+0.9)
      • danceability 0.88 vs target 0.8 (+0.4)
      • acousticness 0.05 vs target 0.1 (+0.9)
--------------------------------------------------------------
 3. Neon Ballroom — DJ Solstice
    [electronic / energetic]  Score: 4.82 / 9.00
      • energy 0.88 vs target 0.9 (+1.9)
      • tempo_bpm 128bpm vs target 145bpm (+0.7)
      • valence 0.74 vs target 0.7 (+0.9)
      • danceability 0.9 vs target 0.8 (+0.4)
      • acousticness 0.14 vs target 0.1 (+0.9)
--------------------------------------------------------------
 4. Sunrise City — Neon Echo
    [pop / happy]  Score: 4.19 / 9.00
      • energy 0.82 vs target 0.9 (+1.7)
      • tempo_bpm 118bpm vs target 145bpm (+0.5)
      • valence 0.84 vs target 0.7 (+0.7)
      • danceability 0.79 vs target 0.8 (+0.5)
      • acousticness 0.18 vs target 0.1 (+0.8)
--------------------------------------------------------------
 5. Static Parade — Gutter Sonnets
    [punk rock / angry]  Score: 4.01 / 9.00
      • energy 0.93 vs target 0.9 (+1.9)
      • tempo_bpm 176bpm vs target 145bpm (+0.4)
      • valence 0.38 vs target 0.7 (+0.4)
      • danceability 0.71 vs target 0.8 (+0.4)
      • acousticness 0.09 vs target 0.1 (+1.0)
```

**relaxed_listener** (jazz / relaxed)

```text
Top 5 recommendations
--------------------------------------------------------------
 1. Coffee Shop Stories — Slow Stereo
    [jazz / relaxed]  Score: 8.08 / 9.00
      • genre match: jazz (+2.0)
      • mood match: relaxed (+1.0)
      • energy 0.37 vs target 0.35 (+1.9)
      • tempo_bpm 90bpm vs target 85bpm (+0.9)
      • valence 0.71 vs target 0.65 (+0.9)
      • danceability 0.54 vs target 0.5 (+0.5)
      • acousticness 0.89 vs target 0.85 (+0.9)
--------------------------------------------------------------
 2. Library Rain — Paper Lanterns
    [lofi / chill]  Score: 5.04 / 9.00
      • energy 0.35 vs target 0.35 (+2.0)
      • tempo_bpm 72bpm vs target 85bpm (+0.7)
      • valence 0.6 vs target 0.65 (+0.9)
      • danceability 0.58 vs target 0.5 (+0.4)
      • acousticness 0.86 vs target 0.85 (+1.0)
--------------------------------------------------------------
 3. Paper Lantern Waltz — June and the Foxes
    [folk / dreamy]  Score: 4.97 / 9.00
      • energy 0.31 vs target 0.35 (+1.8)
      • tempo_bpm 84bpm vs target 85bpm (+1.0)
      • valence 0.58 vs target 0.65 (+0.9)
      • danceability 0.35 vs target 0.5 (+0.3)
      • acousticness 0.88 vs target 0.85 (+0.9)
--------------------------------------------------------------
 4. Focus Flow — LoRoom
    [lofi / focused]  Score: 4.84 / 9.00
      • energy 0.4 vs target 0.35 (+1.8)
      • tempo_bpm 80bpm vs target 85bpm (+0.9)
      • valence 0.59 vs target 0.65 (+0.9)
      • danceability 0.6 vs target 0.5 (+0.4)
      • acousticness 0.78 vs target 0.85 (+0.9)
--------------------------------------------------------------
 5. Midnight Coding — LoRoom
    [lofi / chill]  Score: 4.50 / 9.00
      • energy 0.42 vs target 0.35 (+1.7)
      • tempo_bpm 78bpm vs target 85bpm (+0.9)
      • valence 0.56 vs target 0.65 (+0.8)
      • danceability 0.62 vs target 0.5 (+0.4)
      • acousticness 0.71 vs target 0.85 (+0.7)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

- **Temporarily disabled the mood-match bonus (+1.0).** In `score_song` the exact mood-match component is commented out "TEMPORARILY DISABLED for testing". With mood scoring off, the ranking is decided almost entirely by genre match plus numeric closeness. Comparing the run with mood matching (e.g. *Focus Flow — LoRoom* at 8.26 with the focused-mood bonus) to a run without it shows the same songs still rank near the top because they were already the best numeric matches — but exact-mood songs lose exactly 1.0 point and can slip one or two positions, and non-genre-matching songs can move up when the gap between them and the leaders is under a point. This confirmed that mood match acts as a tie-breaker/booster in my system rather than the main driver of the ranking.

- **Running the same scoring rule for very different listeners.** I ran four profiles through the identical recommender: lofi/chill, lofi/focused, rock/intense (workout_listener), and jazz/relaxed (relaxed_listener). In every case the top spot went to a song with an exact genre + mood match (Storm Runner for the workout listener, Coffee Shop Stories for the relaxed listener, etc.), and scores 2–4 filled with songs from neighboring genres that matched the numeric targets. For the workout listener, *Gym Hero* (pop/intense) ranked #2 on pure numeric fit even without a genre match, showing the numeric components are strong enough to promote a song over the genre bonus gap alone.

- **Behavior for users whose favorite genre is rare in the catalog.** For workout_listener, only one rock song won the +2.0 genre bonus, so positions 2–5 were pop/electronic/punk songs scoring around 4.0–5.8, separated only by numeric fit. Compare that to lofi listeners, where three lofi songs cluster at the top with scores above 6.7. This showed the system's top-5 quality depends heavily on how many songs of the user's favorite genre exist in the CSV — a sparse genre leaves most of the list to "consolation" numeric matches.

- **What the numeric tolerances do.** Each numeric component awards its full points only when the song is within tolerance of the target and decays linearly to zero. For example, energy is worth up to +2.0 with a 0.5 tolerance and tempo up to +1.0 with a 50 BPM tolerance. This is why *Storm Runner* (energy 0.91 vs target 0.9) earned +2.0 while *Static Parade* (valence 0.38 vs target 0.7) earned only +0.4 — a song can match on energy and still lose a lot of points on valence or tempo, which keeps the top of the ranking from being dominated by any single feature.



---

## Limitations and Risks

- **Tiny catalog.** The recommender works on a single small CSV, so the top-5 list is really "the best 5 songs in a very small pool." Users get almost no diversity, and the same handful of songs will be recommended on nearly every run for a given profile.

- **Heavy dependence on the favorite genre.** The +2.0 genre bonus dominates everything else. A user whose favorite genre has few or no songs in the catalog gets a list full of weak numeric-only matches (as seen for workout_listener, whose #2–#5 all scored under 6.0), while a user whose genre is well represented gets a much stronger list.

- **Bias toward categories that are common in the CSV.** Genres and moods that appear more often in the data get recommended far more often, and rare categories are effectively invisible. If the CSV reflects only the kinds of songs the dataset author liked, those biases carry straight into the recommendations.

- **Exact-match only for categorical features.** Genre and mood must match exactly — a "lofi" song gives zero credit for a "chillhop" listener even if they are nearly identical. There is no notion of similar genres or moods.

- **Cold start: no listening history.** The profile is fully specified by the user; the system never learns from what a person actually played, liked, or skipped, so it cannot improve over time or discover that a user's stated taste differs from their real behavior.

- **No context, popularity, or novelty.** Every recommendation is the same regardless of time of day, activity, or what a user has already heard recently — the same top-5 will repeat. There is also no popularity signal, so a genuinely great but rare song competes only on feature fit.

- **No evaluation.** The system has no ground truth to compare against (no held-out likes/play data), so "score 8.26" is only a self-consistent number from my own scoring rule — I cannot measure whether the recommendations are actually good.

- **Understands lyrics, language, or song identity not at all.** The score uses only a handful of numeric features, so it knows nothing about lyrics, language, artist similarity beyond the genre field, or anything that actually makes people like songs.




---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Working on this project showed me that a recommender is really just a pipeline that turns raw data into a prediction: songs and a taste profile become numbers, a hand-written scoring rule turns those numbers into a score, and a sort turns the scores into a ranked list of recommendations. The prediction is only as good as the data representation and the weights in the rule — my +2.0 genre bonus and the numeric tolerances decide everything, and the same songs can rise or fall in the ranking just by changing those numbers. The point-by-point explanations were also a good reminder that a model should be able to justify its output: every recommendation my system makes can be traced back to specific feature matches, which is something real production recommenders should do too.

The biggest lesson was about where bias sneaks in. My system over-rewards the genre it is asked for and can't recognize related genres, so a listener whose favorite genre is rare in the CSV gets a noticeably worse top-5 than a lofi listener, purely because of what the dataset happens to contain — not because the system is worse at matching their taste. That is the same unfairness dynamic as in real systems: training data that under-represents some genres, moods, artists, or audiences produces recommendations that systematically favor whatever was over-represented, and the model looks confident the whole time because it is only optimizing the rule it was given. It also made me appreciate that a recommender needs real feedback (likes, skips, plays) and held-out evaluation to know whether it is actually helping people, rather than just being self-consistent with its own scoring formula.






