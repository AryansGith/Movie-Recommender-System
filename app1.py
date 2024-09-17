import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:9]:  # Change from 5 to 8
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create a container for the movie posters and names
    st.markdown("""
    <div class="movie-container">
        {}
    </div>
    """.format(''.join([f"""
    <div class="movie-item">
        <img src="{recommended_movie_posters[i]}" onclick="openModal('{recommended_movie_posters[i]}')" />
        <div class="movie-name" onclick="toggleFullName(this)">
            {recommended_movie_names[i]}
        </div>
    </div>
    """ for i in range(8)])), unsafe_allow_html=True)

    # Add CSS and JavaScript to handle the modal display and click events
    st.markdown("""
    <style>
    .movie-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 20px;
        justify-content: center; /* Centers items horizontally */
    }
    .movie-item {
        text-align: center;
        position: relative;
    }
    .movie-item img {
        width: 100%;
        height: auto;
        cursor: pointer;
    }
    .movie-name {
        font-weight: bold;
        margin-top: 5px;
        white-space: normal; /* Allows text to wrap */
        overflow: hidden; /* Hides overflow text */
        text-overflow: ellipsis; /* Adds ellipsis if needed */
        max-height: 4em; /* Adjust height to control the number of lines before ellipses */
        line-height: 1.5em; /* Adjust line height for better text display */
        cursor: pointer;
    }
    .full-name {
        display: none;
        position: absolute;
        background: #333;
        color: #fff;
        padding: 5px;
        border-radius: 3px;
        bottom: 120%;
        left: 50%;
        transform: translateX(-50%);
        white-space: normal;
        width: max-content;
        z-index: 1;
    }
    .modal {
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgba(0, 0, 0, 0.8);
        justify-content: center;
        align-items: center;
    }
    .modal-content {
        max-width: 90%;
        max-height: 90%;
        margin: auto;
    }
    .modal-close {
        position: absolute;
        top: 20px;
        right: 20px;
        color: #fff;
        font-size: 40px;
        font-weight: bold;
        cursor: pointer;
    }
    .modal-close:hover,
    .modal-close:focus {
        color: #bbb;
        text-decoration: none;
    }
    </style>
    <script>
    function toggleFullName(element) {
        const fullName = element.nextElementSibling;
        if (fullName.style.display === "none") {
            fullName.style.display = "block";
        } else {
            fullName.style.display = "none";
        }
    }

    function openModal(posterUrl) {
        const modal = document.createElement('div');
        modal.classList.add('modal');
        modal.innerHTML = `
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <img class="modal-content" src="${posterUrl}">
        `;
        document.body.appendChild(modal);
        modal.style.display = 'flex';
    }

    function closeModal() {
        const modal = document.querySelector('.modal');
        if (modal) {
            modal.style.display = 'none';
            document.body.removeChild(modal);
        }
    }
    </script>
    """, unsafe_allow_html=True)
