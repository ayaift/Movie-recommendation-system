# Movie Recommendation System

This is a **content-based movie recommender system** that suggests similar movies based on the details of a selected movie. It uses information such as **genres**, **keywords**, **cast**, **crew**, and **overviews** from the TMDB dataset.

##  How It Works?

###  1. Data Preprocessing
The system starts by cleaning and combining key features into a new column called `tags`.

 Steps involved:
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

 Files saved:
- `movie_list.pkl`
- `similarity.pkl`

---

##  Web Frontend with Streamlit

The frontend is built using **Streamlit**, allowing users to:
- **Select a movie** from a dropdown menu
- **Click a button** to get recommendations
- **View posters and titles** of 5 recommended movies fetched via the TMDB API

---

## How to Run and Launch the project

### Clone the Repository

Start by cloning the repository from GitHub:

```bash
git clone https://github.com/ayaift/Movie-recommendation-system.git
```

Then navigate to the project folder:

```bash
cd Movie-recommendation-system
```

---

### Explore the Notebook

If you want to understand the model logic or see intermediate results:

1. Launch Jupyter Notebook:

    ```bash
    jupyter notebook
    ```

    > This will open a local tab in your browser at `http://localhost:8888/tree`.

2. Navigate to the `.ipynb` file in the directory (e.g., `Movie_Recommendation_Development.ipynb`).

3. Click on the file to open it.

4. Run all cells sequentially (`Kernel > Restart & Run All`).

**Don't have Jupyter installed?**  
You can install it via pip:

```bash
pip install notebook
```

Or with Poetry:

```bash
poetry add notebook
```

---

### Install Dependencies

#### With Poetry (recommended):

If you have [Poetry](https://python-poetry.org/) installed:

```bash
poetry install
```

#### Or with pip (if you don’t use Poetry):

```bash
pip install -r requirements.txt
```

---

### Run the Streamlit App

#### With Poetry:

```bash
poetry run streamlit run app.py
```

#### Or directly with Streamlit (if installed globally):

```bash
streamlit run app.py
```

---

### Done!

Your default browser should open with the app running at:

```
http://localhost:8501
```

If it doesn't open automatically, simply copy and paste the link into your browser.

---

### Problems that may occur

- **`streamlit: command not found`**  
  → Make sure you installed Streamlit (`pip install streamlit`) or used Poetry.

- **`ModuleNotFoundError`**  
  → Double-check that dependencies were installed properly.

---

Enjoy exploring and discovering new movies 🎬!
