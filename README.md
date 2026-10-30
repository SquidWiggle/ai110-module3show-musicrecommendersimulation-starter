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

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - Emotion: mood & valence
  - Style: genre & energy
  - Groove: danceability & vallene
  - Intensity: energy & tempo bgm
- What information does your `UserProfile` store
  - favorite_genre
  - favorite_mood 
  - target_energy 
  - likes_acoustic (not required in my opinion, but kept for future improvements)
  - likes_valences
  - target_danceability
  - target_tempo_bpm
- How does your `Recommender` compute a score for each song
  In a total of 10.0 pts budget, 
  1. Emotion (3.5 pts)
    - Exact mood match (`song.mood == user.favorite_mood`) gives the song 2 points.
    - Close valence gives you max 1.5 points: `1.5 * (1.0 - abs(target_val - song.valence))`.

  2. Style (2.5 pts)
    - Genre match gives a song 1.5 pts. If genre is not matched then it gets 0 points.
    - Extra 1 style point if `danceability` and `energy` are closed to the user's preference: 
    `1.0 * (1.0 - 0.5 * abs(target_dance - song.danceability) - 0.5 * abs(target_energy - song.energy))`.

  3. Groove (2.0 pts)
    - Groove is close to `danceability`, but if valence drifts too far, the song is not close to prefered groove anymore. Reward full 2 groove points if `abs(target_val - song.valence) <= 0.15`. If valence drifts further, groove points are throttled:
    `groove_pts = 2.0 * (1.0 - abs(target_dance - song.danceability)) * max(0.0, 1.0 - 2.0 * abs(target_val - song.valence))`.
   4. Intensity (2.0 pts)
    - Energy is max 1.0 pt: `1.0 * (1.0 - abs(target_energy - song.energy))`.
    - Tempo BGM is max 1.0 pt: `1.0 * max(0.0, 1.0 - abs(target_bpm - song.tempo_bpm) / 100.0)`.

- How do you choose which songs to recommend
After all scores are added up, the total points of the song is compared to the user's preference.

You can include a simple diagram or bullet list if helpful.

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



