# 🎬 Movie Recommendation System

This is a **content-based movie recommender system** that suggests similar movies based on the details of a selected movie. It uses information such as **genres**, **keywords**, **cast**, **crew**, and **overviews** from the TMDB dataset.

## 🚀 How It Works?

###  1. Data Preprocessing
The system starts by cleaning and combining key features into a new column called `tags`.

✔️ Steps involved:
- Removing spaces  
- Converting text to lowercase  
- Stemming using `PorterStemmer`

This ensures the text is normalized and ready for comparison.

---

### 2. Text Vectorization
- Uses `CountVectorizer` to convert the `tags` column into numerical vectors.
- Limits to the **top 5000** keywords and removes common English stopwords.
- This turns each movie into a structured numeric representation of its content.

---

###  3. Cosine Similarity Calculation
- Computes **cosine similarity** using scikit-learn.
- Measures how close each movie is to every other based on vector similarity.

---

###  4. Recommendation Function
When a user selects a movie, the system:
1. Finds its index in the dataset  
2. Retrieves its similarity scores  
3. Sorts the results  
4. Returns the **top 5 most similar movies** (excluding the original)

---

###  5. Model Saving
- Saves the processed movie list and similarity matrix using `pickle`
- This avoids recomputing on every run

📂 Files saved:
- `movie_list.pkl`
- `similarity.pkl`

---

## 🌐 Web Frontend with Streamlit

The frontend is built using **Streamlit**, allowing users to:
- 🎥 **Select a movie** from a dropdown menu
- 📌 **Click a button** to get recommendations
- 🖼️ **View posters and titles** of 5 recommended movies fetched via the TMDB API

---

## ▶️ How to Run

To start the Streamlit app:
```bash
streamlit run app.py
