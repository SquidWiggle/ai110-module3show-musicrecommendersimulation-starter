# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeMatcher

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate
    - Content based recommendation based on similarities in content's features.
- What assumptions does it make about the user
    - The user enjoys content of similar features, for example, songs of the same energy or genre, rather than music of various genre and styles.
- Is this for real users or classroom exploration
    - Classroom exploration only.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
    - Mood, valence, genre, accousticness, danceability, energy, tempo_bpm, release_year, popularity.
- What user preferences are considered  
    - The user's favorite genre, mood, preference for valnce, energy, tempo BGM, accousticness, release year.
- How does the model turn those into a score  
    - The scorer draw score from 5 components that add up to 10 points max.
        1. Emotion (max 3.0 pts)
            - Checks if the song's mood word matches the user's choice (1.8 points) and adds up to 1.2 points the closer the song's valence is to the target
        2. Style (max 2.0 pts)
            - Checks if the song's genre word matches (1.1 points), adds up to 0.6 points for close danceability and energy, and adds up to 0.3 points for acoustic closeness
        3. Groove (max 2.0 pts)
            - Awards up to 2.0 points only when the song matches both danceability and happiness targets together
        4. Intensity (max 2.0 pts)
            - Adds up to 1.0 point for matching target energy and up to 1.0 point the closer the track speed is to the target tempo (beats per minute) within a 100-BPM window
        5. Discovery & Era (max 1.0 pt)
            - Gives up to 0.5 points for catalog popularity and up to 0.5 points if the release year is within 10 years of the user's target year
- What changes did you make from the starter logic
    - I added the user's year into the score considerations.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
    - 18 songs
- What genres or moods are represented  
    - 13 Genres: Pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, metal, classical, reggae, hip hop, r&b, techno, country.
    - 14 Moods: Happy, chill, intense, relaxed, moody, focused, nostalgic, aggressive, melancholic, groovy, confident, romantic, dark, peaceful.
- Did you add or remove data  
    - Added: 8 new songs (IDs 11–18) and 3 new feature columns across all tracks (popularity, duration_ms, release_year).
- Are there parts of musical taste missing in the dataset  
    - older music is missing. More genre would be better.
---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider
    - duration_ms and artist is not considered. I tried to incorporate all other features but genre is under weighted than others.
- Genres or moods that are underrepresented
    - blues, punk, edm, latin
- Cases where the system overfits to one preference
    - It overfits danceable, high-valence pop profiles
- Ways the scoring might unintentionally favor some users
    - It favors mainstream, upbeat, modern dance listeners over niche, acoustic, vintage, and melancholic tastes.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested
    - Chill Lofi
    - Deep Intense Rock
    - Adversarial: The Genre Hijack
    - Adversarial: The Casing Trap
    - Adversarial: The Sad Banger
    - Adversarial: The Dark Clubber
    - Adversarial: Out-of-Bounds Exploit
- What you looked for in the recommendations
    - I looked for frquency of the songs showing up under each user profile, and what features contribted the most to their recommendations.
- What surprised you
    - Removing my top weighted feature did not make the formula better but made it worse
- Any simple tests or comparisons you ran  
    - I removed valence from the calculation, but surprisingly, the recommender became worse ad recommended more of the same song (7 repeats each on 2 songs)
No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
    - I'd like to add artist into the scorer, reduce popularity bias to allow the user to discover indie hits, and add a few older years into the mix instead of only looking at recent years from the user profile.
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
