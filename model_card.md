# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**TempoMatch 1.0** — a genre-gated, attribute-similarity recommender that ranks a 20-song catalog against a single taste profile.

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

My TempoMatch 1.0 generates ranked top-k song recommendations from a fixed 20-song catalog for a single listener whose taste is described by one favorite genre, one favorite mood, and target values for energy, tempo, valence, danceability, and acousticness. It assumes the user can state those preferences explicitly up front — it does not learn taste from listening history, skips, or ratings, and it assumes the numeric targets are meaningful to the user in the first place. This is a classroom exploration tool built for the AI110 module 3 simulation, not a production system for real listeners; its purpose is to make scoring tradeoffs, filter bubbles, and profile comparisons visible and testable.

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

TempoMatch compares each song to the user's taste and awards points out of a maximum of 8.0. It looks at seven things per song: genre, mood, and five numeric attributes (energy, tempo, valence, danceability, acousticness). The favorite genre earns the biggest bonus — a flat 2.0 points for an exact match — and the mood match would earn 1.0, though I temporarily disabled the mood bonus during my experiments to measure how much it drives the ranking. Each numeric attribute is scored on a sliding scale: the closer the song's value is to the user's target, the more points it earns, fading linearly to zero once the difference passes a tolerance (0.5 for most attributes, 50 BPM for tempo), and never going negative. The starter logic only added up points for matches; my main changes were making the numeric scoring graded and floored at zero, accepting two different naming conventions for the preference dictionary, and breaking score ties by preferring the song whose energy is closest to the user's energy target before falling back to catalog order.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog is a small, hand-crafted CSV of exactly 20 songs across 14 genres — pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, reggae, metal, country, folk, electronic, R&B, and punk rock — spanning moods from happy and chill to intense, angry, sad, romantic, dreamy, and playful. Each song carries eight fields: title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. I did not add or remove any songs; I used the starter data as-is and varied only the user profiles in my experiments. The dataset's biggest gaps in musical taste are coverage and repetition: several genres (hip-hop, classical, R&B, punk rock, country, folk) have only a single song, and no dimension captures lyrics, vocals, production era, or artist affinity at all — so tastes like instrumental vs. vocal, live vs. studio, or a favorite artist cannot be represented.

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

TempoMatch works best for users whose favorite genre is well-represented in the catalog and whose numeric targets are moderate rather than extreme — the lofi/chill listener got a tight, sensible cluster (Midnight Coding, Focus Flow, Library Rain within 0.62 points of each other), and the pop/gym listener correctly surfaced Gym Hero and Sunrise City. The scoring captures a real pattern: within a genre cluster, the graded numeric similarity orders songs in a way that matches intuition, putting the most on-profile track first. Extreme profiles also get one clearly correct answer — the classical/sad listener's #1 (Still Water Prayer at 7.39) and the hip-hop listener's #1 (Concrete Verse at 7.46) were exactly the songs I would have picked by hand, and the B vs. C pair comparison confirming the two rankings are near-perfect inverses shows the numeric component measures musical distance coherently. Overall, whenever a song obviously matches the stated taste, the model ranks it first, which is the most important property to get right.

---

## 6. Limitations and Bias  

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

One weakness I discovered during my experiments is that the genre bonus creates a strong filter bubble. Because an exact genre match is worth 2.0 points — more than any single numeric feature — a user's favorite genre effectively dominates the ranking, and nearly all of the top results collapse into that one genre. When I tested a lofi profile, all three lofi songs in the 20-song catalog took the top three spots, leaving only two slots for the other sixteen songs, which appeared there only because of loose numeric similarity rather than any real preference. This means users are rarely shown music from genres they haven't already declared, so the system reinforces existing taste instead of helping it grow. It also makes the recommendations vulnerable to the small catalog: a genre with only three songs is quickly exhausted, while a typo or casing mismatch in a genre label (e.g., "R&B" vs "r&b") would silently remove a whole cluster of songs from consideration.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

I tested four distinct user profiles against the same 20-song catalog: a **lofi/chill** listener (mid energy, 90 BPM, acoustic-leaning), a **pop/gym** listener (high energy, 130 BPM, very danceable, low acousticness), a **classical/sad** listener (very low energy and valence, high acousticness, slow tempo), and a **hip-hop/energetic** listener (high energy and danceability, ~95 BPM, low acousticness). For each profile I checked that the top result was the song that most obviously matches the stated taste, that scores and explanations made sense, and that the ranking sorted correctly in descending order. I also ran a comparison where I temporarily disabled the mood-match bonus to see how sensitive the ranking was to each feature.

The results were mostly intuitive — the lofi profile surfaced Midnight Coding, Library Rain, and Focus Flow; the gym profile surfaced Gym Hero and Sunrise City; the classical profile surfaced Still Water Prayer; and the hip-hop profile surfaced Concrete Verse — which matched my intuition about each taste. What surprised me most was how sharply the results clustered around the favorite genre: every profile got its favorite genre at rank #1, and the remaining slots were filled by songs from unrelated genres (country and R&B for the lofi user, rock for the gym user) purely because of numeric proximity, which felt arbitrary rather than intentional. I was also surprised by how much a single feature mattered — when I disabled the mood-match bonus, Library Rain (the archetypal chill song) dropped from rank #2 to #3 behind a "focused" song, showing the ranking is very sensitive to the mood weight. Finally, I noticed that two of the top three lofi results were by the same artist (LoRoom), which suggested the model does not penalize repetition of the same artist or sound within the top-k list.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

First, I would attack the filter bubble described in section 6: cap the genre bonus per slot or reserve one or two top-k positions for non-favorite genres so users occasionally discover music outside their declared taste, and make genre matching case-insensitive so "R&B" and "r&b" can't silently drop a whole cluster. Second, I would re-enable the mood bonus with a tunable weight (and let users express multiple moods or genres with individual weights) instead of the current one-genre, one-mood hard assignments, which would handle mixed tastes like "chill on weekdays, gym music on weekends." Third, I would add artist-diversity enforcement in the top-k — I noticed two of the lofi profile's top three were both by LoRoom — and richer explanations that show a point-by-point breakdown of why a song beat its neighbors. Longer term, I'd replace the hand-set numeric targets with learned preferences from implicit feedback (likes, skips) so users never have to state that they want exactly 0.70 acousticness.

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this taught me that a recommender's output is shaped less by the data than by the weights someone chose — a single 2.0-point genre bonus silently turned every profile's list into a one-genre cluster with arbitrary filler beneath it, and a 1.0-point mood bonus moving one song from rank #2 to #3 showed how sensitive rankings are to small weight changes. The most unexpected discovery was that profile behavior depends on where the targets sit in the feature space: extreme profiles (classical/sad) get one dominant match and a huge score gap, while mid-range profiles get a tight competitive cluster — same algorithm, very different experience. I also learned the value of adversarial testing: disabling one feature at a time was the only way to see how much each weight actually mattered. It changed how I use real recommendation apps — I now assume that what I'm shown reflects a weighting decision and a limited catalog, not an objective measure of what I'd enjoy, and that the "diversity" I see (or don't see) was designed in deliberately or absent by accident.

## 10. Profile Pair Comparison Comments

I tested four profiles (A: lofi/chill, B: pop/gym, C: classical/sad, D: hip-hop/energetic). Below is a comparison comment for each pair, describing what changed between their outputs and why that makes sense.

### A (lofi/chill) vs B (pop/gym)
A's top three are all lofi (Midnight Coding 6.82, Focus Flow 6.72, Library Rain 6.20), while B's top two are both pop (Gym Hero 7.15, Sunrise City 6.64). The difference comes almost entirely from the +2.0 genre bonus: each profile's favorite genre acts as a gate that pulls its own cluster to the top, while the numeric scores (B's high energy/danceability, A's acousticness/low tempo) only fine-tune the order *within* each cluster. It makes sense that the two profiles never share a top-2 song — their genre and mood targets point to opposite ends of the catalog. They do share some crossover in the lower ranks (e.g., Rooftop Lights for B and Velvet Hourglass-style near-misses for A), which shows numeric similarity alone can surface songs regardless of genre.

### A (lofi/chill) vs C (classical/sad)
Both profiles like calm, acoustic music, but C's extreme targets (energy 0.15, valence 0.25, acousticness 0.95, 65 BPM) push its top result to Still Water Prayer (7.39), while A's mid-range targets favor Midnight Coding (6.82). The interesting difference is the *score spread*: C's #2 (Spacewalk Thoughts, 3.76) is nearly 4 points below its #1, while A's top three are within 0.62 points of each other. That makes sense because C's extreme targets match almost nothing else in the catalog — Still Water Prayer is the only song close to all four targets — whereas A's moderate targets are within tolerance of half the catalog, so several lofi songs compete closely. This shows the linear scoring behaves very differently depending on where the user's targets sit in the range: extreme profiles get one dominant match, mid-range profiles get a tight cluster.

### A (lofi/chill) vs D (hip-hop/energetic)
A's list is dominated by slow, acoustic lofi tracks; D's list is dominated by Concrete Verse (7.46) at #1, then a big drop to Night Drive Loop (4.60). The gap between D's #1 and #2 (~2.9 points) is the largest of any profile, because Concrete Verse is the only hip-hop song in the catalog and the only one matching D's genre — once the genre bonus is exhausted, the rest of the list is held together only by graded numeric similarity, which D's high danceability/energy targets earn from synthwave, pop, and electronic songs. This mirrors A's behavior (a single-genre cluster at the top, arbitrary filler below) but is more extreme because hip-hop has only one representative in the catalog. It makes sense that both profiles show the same structural pattern — the genre bonus concentrates results around the favorite genre, and the numeric scores just decide the order of what's left.

### B (pop/gym) vs C (classical/sad)
This is the most opposite pair. B's top results are all high-energy, high-danceability, low-acousticness songs (Gym Hero 7.15, Sunrise City 6.64, Neon Ballroom 5.13); C's top results are the exact opposite (Still Water Prayer 7.39, Spacewalk Thoughts 3.76, Paper Lantern Waltz 3.48). There is zero overlap between their top-3 lists, which makes sense because B and C sit at opposite extremes of every numeric feature — energy (0.90 vs 0.15), valence (0.80 vs 0.25), danceability (0.85 vs 0.15), acousticness (0.10 vs 0.95), and tempo (130 vs 65 BPM). Every numeric component that gives B points actively takes points away from C, so the two rankings are close to inverses of each other. Interestingly, both still show the same "one genre cluster at the top, filler below" pattern, which confirms the genre bonus is the structural driver of the output regardless of which genre the user picks.

### B (pop/gym) vs D (hip-hop/energetic)
B and D both want high energy and high danceability, so their lists share real overlap: Rooftop Lights and Neon Ballroom appear in both, and B's Storm Runner and D's Night Drive Loop are similar in spirit. The key difference is the mood: B's favorite mood is "energetic" but its top song (Gym Hero) is "intense", while D's top song (Concrete Verse) is exactly "energetic" — because the pop genre bonus outweighs B's mood mismatch, while D's genre and mood align perfectly on its #1. This makes sense given the weighting: genre (+2.0) is worth twice the mood bonus (+1.0), so for B the genre gate on pop dominates the mood signal, while for D both signals reinforce each other on Concrete Verse, producing the highest single-profile score (7.46) of any top result. It shows how the fixed weights make genre the dominant signal even when a user's mood preference is equally strong.

### C (classical/sad) vs D (hip-hop/energetic)
C's list skews toward slow, acoustic, low-valence songs, while D's skews toward high-energy, danceable ones — a near-opposite pairing like B vs C, but with one important nuance: D's list has more genuine overlap with B's (both want "energetic" music) than C has with either. C's numeric targets are so extreme that only one song (Still Water Prayer) comes close on all dimensions, so C's ranking is essentially "one great match, then whatever is least-bad." D, by contrast, has multiple plausible matches (hip-hop, synthwave, pop, electronic) because its targets sit in a crowded region of the catalog. This makes sense: the scoring gives a smooth score to every song, so profiles whose targets sit in a dense part of the feature space (D) get diverse-ish lists, while profiles whose targets sit in a sparse corner (C) get one dominant song and a long tail of weak matches.
