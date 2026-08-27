import pickle
import streamlit as st
import requests
from groq import Groq
from auth import sign_in, sign_up, sign_out
from database import add_profile, add_favorite, get_favorites,remove_favorite
from database import save_history,get_history,clear_history,is_favorite,remove_favorite_by_movie
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.set_page_config(
    page_title="Movie Explorer",
    page_icon="🎬",
    layout="wide"
)

load_css()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ------------------ LOGIN SESSION ------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ------------------ SESSION STATE ------------------
if "page_state" not in st.session_state:
    st.session_state.page_state = "home"

if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None

if "selected_movie_name" not in st.session_state:
    st.session_state.selected_movie_name = ""
# ------------------ LOGIN PAGE ------------------

if not st.session_state.logged_in:

    st.title("🎬 Movie Recommendation System")

    option = st.radio("Choose", ["Login", "Signup"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Signup":

        if st.button("Create Account"):

            response, error = sign_up(email, password)

            if error:
                st.error(error)
            else:
                st.success("Account created successfully!")
                st.info("Now login using your email and password.")

    else:

        if st.button("Login"):

            response, error = sign_in(email, password)

            if error:
                st.error(error)
            else:

                st.session_state.logged_in = True
                st.session_state.user = response.user
                add_profile(response.user)

                st.success("Login Successful")
                st.rerun()

    st.stop()     # ✅ Yahan hona chahiye (Signup/Login dono ke baad)
# ------------------ LOAD DATA ------------------
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# ------------------ API FUNCTIONS ------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster = data.get('poster_path')
    if poster:
        return "https://image.tmdb.org/t/p/w500/" + poster
    return "https://via.placeholder.com/300x450"

def fetch_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    data = requests.get(url).json()
    return data.get('overview', "No description"), data.get('vote_average', "N/A")

def fetch_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=en-US"
    data = requests.get(url).json()

    if 'results' not in data:
        return None

    for video in data['results']:
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

def fetch_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=en-US"
    data = requests.get(url).json()

    if 'cast' not in data:
        return []

    return [actor['name'] for actor in data['cast'][:5]]

def show_movie_details():

    overview, rating = fetch_details(st.session_state.selected_movie_id)
    poster = fetch_poster(st.session_state.selected_movie_id)

    st.title(f"🎬 {st.session_state.selected_movie_name}")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(poster)

    with col2:
        st.write(f"⭐ Rating: {rating}")
        st.write("### Overview")
        st.write(overview)

        cast = fetch_cast(st.session_state.selected_movie_id)
        if cast:
            st.markdown(
                f"<b>Cast:</b> {', '.join(cast)}",
                unsafe_allow_html=True
            )

        trailer = fetch_trailer(st.session_state.selected_movie_id)
        if trailer:
            st.video(trailer)

    if st.button("⬅ Back"):
        st.session_state.page_state = "home"
        st.rerun()

# ------------------ RECOMMEND ------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),
                       reverse=True, key=lambda x: x[1])

    names, posters, ids = [], [], []

    for i in distances[1:21]:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
        ids.append(movie_id)

    return names, posters, ids
def ai_movie_search(user_query):
    prompt = f"""
    You are a movie recommendation expert.

    User query:
    {user_query}

    Suggest EXACTLY 3 movies.

    Return ONLY in this format.

    Movie 1
    Movie 2
    Movie 3
    """

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()

# ------------------ SIDEBAR ------------------
st.sidebar.title("📂 Menu")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Manual Recommendation","❤️ My Favorites",   "🕒 Watch History"]
)
category = st.sidebar.selectbox(
    "Category",
    ["All", "Trending", "Top Rated", "Popular"]
)

cols = st.sidebar.slider("Grid columns", 3, 8, 5)
# ------------------ Movie_card------------------
def show_movie_card(movie_id, movie_name, key, show_poster=True):

    if show_poster:
        st.image(fetch_poster(movie_id))
        st.markdown(
            f"""
            <div style="
                height:90px;
                display:flex;
                align-items:center;
                justify-content:center;
                text-align:center;
                font-size:18px;
                font-weight:700;
                color:#111827;
                padding:0 8px;
                overflow:hidden;
            ">
                {movie_name}
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button("🔓 Open", key=f"open_{key}"):

        save_history(
            st.session_state.user.id,
            int(movie_id),
            movie_name
        )

        st.session_state.selected_movie_id = movie_id
        st.session_state.selected_movie_name = movie_name
        st.session_state.page_state = "details"

        st.rerun()

    if is_favorite(st.session_state.user.id, int(movie_id)):

        if st.button("❤️", key=f"heart_{key}"):

            remove_favorite_by_movie(
                st.session_state.user.id,
                int(movie_id)
            )

            st.rerun()

    else:

        if st.button("🤍", key=f"heart_{key}"):

            add_favorite(
                st.session_state.user.id,
                int(movie_id),
                movie_name
            )

            st.rerun()

# ------------------ COMMON MOVIE GRID ------------------
def show_movies(data):

    columns = st.columns(cols)

    for i in range(len(data)):

        with columns[i % cols]:

            movie_id = data.iloc[i].movie_id
            title = data.iloc[i].title

            show_movie_card(
                movie_id,
                title,
                f"home_{movie_id}_{i}"
            )
# ------------------ HOME PAGE ------------------
if page == "Home":


    if st.session_state.page_state == "details":
        show_movie_details()

    # 🏠 HOME VIEW
    else:

        st.title("🎬 Movie Explorer")

        if category == "Trending":
            st.subheader("🔥 Trending")
            show_movies(movies.head(15))

        elif category == "Top Rated":
            st.subheader("⭐ Top Rated")
            show_movies(movies.tail(15))

        elif category == "Popular":
            st.subheader("🎥 Popular")
            show_movies(movies.sample(15))

        else:
            st.subheader("🔥 Trending")
            show_movies(movies.head(15))

            st.subheader("⭐ Top Rated")
            show_movies(movies.tail(15))

            st.subheader("🎥 Popular")
            show_movies(movies.sample(15))

# ------------------ RECOMMENDATION PAGE ------------------
elif page == "Manual Recommendation":
    if st.session_state.page_state == "details":
        show_movie_details()


    else:
        st.title("🎬 Movie Recommender")

        query = st.text_input("Search by movie title (keyword)", key="search")

        filtered_movies = movies[movies['title'].str.lower().str.contains(query.lower())] if query else movies

        selected_movie = st.selectbox(
            "Suggestions",
            filtered_movies['title'].values,
            key="select"
        )

        if st.button("Show Recommendation"):




            names, posters, ids = recommend(selected_movie)

            st.session_state.names = names
            st.session_state.posters = posters
            st.session_state.ids = ids

        if "names" in st.session_state:

            st.subheader("Results")

            columns = st.columns(cols)

            for i in range(len(st.session_state.names)):
                with columns[i % cols]:
                    for i in range(len(st.session_state.names)):
                        with columns[i % cols]:
                            show_movie_card(
                                st.session_state.ids[i],
                                st.session_state.names[i],
                                f"manual_{st.session_state.ids[i]}_{i}"
                            )


elif page == "AI Recommendation":

    if st.session_state.page_state == "details":
        show_movie_details()

    else:

        st.title("🤖 AI Movie Assistant")

        if "ai_movies" not in st.session_state:
            st.session_state.ai_movies = []

        if "similar_names" not in st.session_state:
            st.session_state.similar_names = []

        if "similar_posters" not in st.session_state:
            st.session_state.similar_posters = []

        if "similar_ids" not in st.session_state:
            st.session_state.similar_ids = []

        ai_query = st.text_input(
            "Describe what you want",
            placeholder="Example: Funny family movie"
        )

        if st.button("🤖 Ask AI"):

            if ai_query:

                response = ai_movie_search(ai_query)

                movie_list = []

                for line in response.split("\n"):

                    line = line.strip()

                    if "." in line:
                        parts = line.split(".", 1)
                        if parts[0].strip().isdigit():
                            line = parts[1].strip()

                    if ":" in line:
                        line = line.split(":")[-1].strip()

                    if line:
                        movie_list.append(line)

                st.session_state.ai_movies = movie_list

                # New AI search → clear old similar movies
                st.session_state.similar_names = []
                st.session_state.similar_posters = []
                st.session_state.similar_ids = []

        if len(st.session_state.ai_movies) > 0:

            st.subheader("🎬 AI Suggestions")

            for movie in st.session_state.ai_movies:

                if movie in movies['title'].values:

                    movie_id = movies[movies['title'] == movie].iloc[0].movie_id

                    poster = fetch_poster(movie_id)

                    overview, rating = fetch_details(movie_id)

                    st.image(fetch_poster(movie_id), width=350)
                    st.subheader(movie)

                    st.write(f"⭐ Rating: {rating}")

                    st.write(overview)
                    show_movie_card(
                        movie_id,
                        movie,
                        f"ai_{movie_id}",
                        show_poster=False
                    )


                    if st.button(
                        f"Show Similar Movies - {movie}",
                        key=f"similar_{movie}"
                    ):

                        names, posters, ids = recommend(movie)

                        st.session_state.similar_names = names
                        st.session_state.similar_posters = posters
                        st.session_state.similar_ids = ids

                        st.rerun()

        if len(st.session_state.similar_names) > 0:

            st.subheader("🎬 Similar Movies")

            columns = st.columns(cols)

            for i in range(len(st.session_state.similar_names)):
                with columns[i % cols]:
                    show_movie_card(
                        st.session_state.similar_ids[i],
                        st.session_state.similar_names[i],
                        f"similar_{st.session_state.similar_ids[i]}"
                    )


elif page == "❤️ My Favorites":

        st.title("❤️ My Favorites")

        favorites = get_favorites(st.session_state.user.id)

        columns = st.columns(cols)
        for i, movie in enumerate(favorites):
            with columns[i % cols]:
                poster = fetch_poster(movie["movie_id"])

                st.image(poster)

                st.caption(movie["movie_name"])
                if st.button("❌ Remove", key=f"remove_{movie['id']}"):
                    st.write("REMOVE BUTTON CLICKED")
                    print("Deleting ID:", movie["id"])

                    print("REMOVE BUTTON CLICKED")
                    remove_favorite(movie["id"])

                    st.success("Removed from Favorites ❤️")

                    st.rerun()
elif page == "🕒 Watch History":

    if st.session_state.page_state == "details":
        show_movie_details()

    else:

        st.title("🕒 Watch History")
        if st.button("🗑 Clear History"):
            clear_history(st.session_state.user.id)

            st.success("History Cleared Successfully ✅")

            st.rerun()

        history = get_history(st.session_state.user.id)

        if len(history) == 0:
            st.info("No movies watched yet.")

        else:

            cols = 5
            columns = st.columns(cols)

            for i, movie in enumerate(history):
                with columns[i % cols]:
                    show_movie_card(
                        movie["movie_id"],
                        movie["movie_name"],
                        f"history_{movie['id']}"
                    )

                    st.caption(f"📅 {movie['viewed_at'][:10]}")
if st.session_state.logged_in:

        st.sidebar.success(
            f"Logged in as {st.session_state.user.email}"
        )

        if st.sidebar.button("Logout"):
            sign_out()

            st.session_state.logged_in = False

            st.session_state.user = None

            st.rerun()
