# 🎬 Movie Recommendation System

A smart movie recommendation web application built with **Streamlit** that recommends movies based on content similarity. The application also provides movie details, posters, trailers, user authentication, favorites, and watch history.

## 🚀 Features

* 🎯 **Content-Based Movie Recommendation**

  * Recommends movies similar to the selected movie.
  * Uses **cosine similarity** to find similar movies.

* 🔍 **Movie Search**

  * Search movies by title.
  * Select a movie and get personalized recommendations.

* 🎬 **Movie Details**

  * Movie poster
  * Rating
  * Overview/description
  * Cast information
  * YouTube trailer

* 👤 **User Authentication**

  * User signup and login
  * Logout functionality
  * Authentication handled using Supabase

* ❤️ **Favorites**

  * Add movies to favorites.
  * Remove movies from favorites.

* 🕒 **Watch History**

  * Stores movies opened by the user.
  * View previously watched movies.
  * Clear watch history.

* 🤖 **AI Movie Assistant**

  * Uses Groq's AI model to generate movie suggestions from a user's description.

* 📱 **Interactive UI**

  * Built using Streamlit.
  * Responsive movie grid with customizable columns.

## 🛠️ Technologies Used

| Technology   | Purpose                                            |
| ------------ | -------------------------------------------------- |
| Python       | Application development                            |
| Streamlit    | Web application and UI                             |
| Pandas       | Movie dataset processing                           |
| Scikit-learn | Similarity-based recommendation                    |
| Pickle       | Storing trained movie data and similarity matrix   |
| TMDB API     | Movie posters, details, ratings, cast and trailers |
| Supabase     | Authentication and database                        |
| Groq API     | AI-based movie suggestions                         |
| CSS          | Custom UI styling                                  |

## 🧠 How the Recommendation System Works

This project uses a **content-based filtering** approach.

1. Movie information is processed from the dataset.
2. Relevant movie features are converted into numerical representations.
3. A similarity matrix is created between movies.
4. **Cosine similarity** is used to calculate how similar two movies are.
5. When a user selects a movie, the system finds the movies with the highest similarity scores.
6. The top similar movies are displayed to the user.

The precomputed recommendation data is stored in:

```text
movie_list.pkl
similarity.pkl
```

`similarity.pkl` is managed using **Git LFS** because of its large file size.

## 📂 Project Structure

```text
Movie-Recommendation-System/
│
├── app.py                  # Main Streamlit application
├── auth.py                 # User authentication functions
├── database.py             # Favorites and watch history operations
├── supabase_config.py      # Supabase configuration
├── style.css               # Custom application styling
│
├── movie_list.pkl          # Movie dataset
├── similarity.pkl          # Precomputed similarity matrix
│
├── requirements.txt        # Python dependencies
├── .gitignore              # Files excluded from Git
├── .gitattributes          # Git LFS configuration
│
├── img.png                 # Application screenshot
└── notebook86c26b4f17.ipynb # Development/analysis notebook
```
## 🎯 Future Improvements

* Add genre-based filtering
* Add movie release-year filtering
* Improve recommendation accuracy
* Add pagination for large movie collections
* Add deployment using Streamlit Cloud or another hosting platform
* Improve AI recommendation matching with the movie dataset

## 👨‍💻 Author

**Sadaf Ahmad**

B.Tech Student | Aspiring Software Engineer

