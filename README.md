# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works
  In real world music recommendation systems, songs are recommended based on a multi-layer model. 
  1. When there is no user data, a content based model such as a simple one like one designed here is used. It uses various features of a song to generate vector scores and compare their distances or differences.
  2. Next, when there is a pool of user generated a lot of data, a song can be recommended to a user when multiple other users listened to the same song, and also listened to the recommended songs. Bridge user (a user who listen to songs of different features) playlists can help generate more songs to recommend to other users. A user's ground truth data (did the user listen to the recommended song and stayed long enough to enjoy it, or 'liked' it) can validate if a model's behaving well.
  3. Deep neural models discover and create associations based on complex and implicit cultural patterns between songs. Even if the model does not understand what is the meaning underneath the association, it knows to associate songs that are usually enjoyed by people in the same setting.

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - Emotion: mood & valence
  - Style: genre, energy & acousticness
  - Groove: danceability & valence
  - Intensity: energy & tempo bpm
- What information does your `UserProfile` store
  - favorite_genre
  - favorite_mood
  - target_energy
  - likes_valence
  - target_danceability
  - target_tempo_bpm
  - target_year
  - likes_acoustic (toggles acoustic vs electronic sound texture preference)
- How does your `Recommender` compute a score for each song
  - In a total of 10.0 pts budget across 5 components:
    1. Emotion (3.0 pts)
      - Exact mood match (`song.mood == user.favorite_mood`) gives the song 1.8 points.
      - Close valence gives you max 1.2 points: `1.2 * (1.0 - abs(target_val - song.valence))`.

    2. Style (2.0 pts)
      - Genre match gives a song 1.1 pts: `1.1 if song.genre == user.favorite_genre else 0.0`.
      - Rhythmic and energy alignment gives max 0.6 pt:
      `0.6 * (1.0 - 0.5 * abs(target_dance - song.danceability) - 0.5 * abs(target_energy - song.energy))`.
      - Acoustic texture alignment gives max 0.3 pt:
      `0.3 * (1.0 - abs(target_acoustic - song.acousticness))` (where `target_acoustic = 0.85 if likes_acoustic else 0.15`).

    3. Groove (2.0 pts)
      - Danceability gated by valence lock:
      `groove_pts = 2.0 * (1.0 - abs(target_dance - song.danceability)) * max(0.0, 1.0 - 2.0 * abs(target_val - song.valence))`.

    4. Intensity (2.0 pts)
      - Energy is max 1.0 pt: `1.0 * (1.0 - abs(target_energy - song.energy))`.
      - Tempo BPM is max 1.0 pt: `1.0 * max(0.0, 1.0 - abs(target_bpm - song.tempo_bpm) / 100.0)`.

    5. Discovery & Era (1.0 pt)
      - Popularity is max 0.5 pt: `0.5 * (song.popularity / 100.0)`.
      - Release year era proximity is max 0.5 pt: `0.5 * max(0.0, 1.0 - abs(target_year - song.release_year) / 10.0)`.

- How do you choose which songs to recommend
After computing individual component points, total composite scores are calculated and ranked:
  1. Score each song in the catalog across Emotion, Style, Groove, Intensity, and Discovery/Era (up to 10.0 pts).
  2. Rank songs in descending order of total score.
  3. Return the top $k$ candidates along with human-readable rationale explanations.
  - Potential Bias: valence, danceability, and energy are sampled too many times in this algorithm recipe, so the recommendation can be skewed and favor these featuers. Also, popularity can be over valued.

```mermaid
flowchart TD
    A["UserProfile & Song Data"] --> B["Compute Feature Scores (10.0 pts Max)"]
    
    subgraph Scoring ["5-Component Scoring Engine"]
        B --> C1["Emotion (3.0 pts): mood & valence"]
        B --> C2["Style (2.0 pts): genre, dance, energy & acoustic"]
        B --> C3["Groove (2.0 pts): danceability gated by valence"]
        B --> C4["Intensity (2.0 pts): energy & tempo"]
        B --> C5["Discovery & Era (1.0 pt): popularity & release_year"]
    end

    C1 --> D["Sum Total Score (0 - 10.0 pts)"]
    C2 --> D
    C3 --> D
    C4 --> D
    C5 --> D

    D --> E["Rank Songs Descending by Score"]
    E --> F["Return Top-k Recommendations + Explanations"]
```

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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



