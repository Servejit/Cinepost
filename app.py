# ====================================================
# STREAMLIT APP: Bollywood Poster Gallery with Music
# ====================================================
import streamlit as st
import os
from PIL import Image, ImageDraw

# -------------------------------
# Setup: Create posters + audio folder
# -------------------------------
BASE_DIR = "movies"
POSTER_DIR = os.path.join(BASE_DIR, "posters")
SONG_DIR = os.path.join(BASE_DIR, "songs")

# Sample data: Year -> Movies (50 can be simulated)
sample_data = {
    "2022": ["Gangubai", "RRR", "Bhool Bhulaiyaa 2", "Shamshera", "Vikram Vedha"],
    "2023": ["Jawan", "Pathaan", "Tiger 3", "Rocky Aur Rani Ki Prem Kahani", "Bholaa"]
}

# Create folders
for folder in [POSTER_DIR, SONG_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Generate placeholder posters and songs
for year, movies in sample_data.items():
    year_folder = os.path.join(POSTER_DIR, year)
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)
    for movie in movies:
        poster_path = os.path.join(year_folder, f"{movie}.jpg")
        song_path = os.path.join(SONG_DIR, f"{movie}.mp3")
        if not os.path.exists(poster_path):
            # Placeholder poster
            img = Image.new('RGB', (300, 450), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.text((10, 200), movie, fill=(255, 255, 0))
            img.save(poster_path)
        if not os.path.exists(song_path):
            # Placeholder audio: 1 second silent mp3
            with open(song_path, "wb") as f:
                f.write(b'\x00')  # minimal dummy audio

# -------------------------------
# App Layout
# -------------------------------
st.set_page_config(page_title="🎬 Bollywood Posters Gallery", layout="wide")
st.title("🎬 Bollywood Posters Gallery with Music")

# --- Session State for Likes/Comments ---
if 'likes' not in st.session_state:
    st.session_state['likes'] = {}
if 'comments' not in st.session_state:
    st.session_state['comments'] = {}
if 'selected_movie' not in st.session_state:
    st.session_state['selected_movie'] = None
if 'selected_year' not in st.session_state:
    st.session_state['selected_year'] = None

# --- Functions ---
def get_years():
    return sorted([d for d in os.listdir(POSTER_DIR) if os.path.isdir(os.path.join(POSTER_DIR, d))])

def get_movies(year):
    folder = os.path.join(POSTER_DIR, year)
    return sorted([f.replace(".jpg","") for f in os.listdir(folder) if f.lower().endswith(".jpg")])

# --- Display Year-wise Movie List ---
for year in get_years():
    st.header(f"{year}")
    movies = get_movies(year)
    cols = st.columns(5)
    for idx, movie in enumerate(movies):
        movie_path = os.path.join(POSTER_DIR, year, f"{movie}.jpg")
        thumbnail = Image.open(movie_path).resize((150, 225))
        if cols[idx%5].button(movie):
            st.session_state['selected_movie'] = movie
            st.session_state['selected_year'] = year

# --- Show Selected Movie Poster + Music ---
if st.session_state['selected_movie']:
    year = st.session_state['selected_year']
    movie = st.session_state['selected_movie']
    poster_path = os.path.join(POSTER_DIR, year, f"{movie}.jpg")
    song_path = os.path.join(SONG_DIR, f"{movie}.mp3")
    
    st.image(Image.open(poster_path), use_column_width=True)
    
    # Background music
    st.audio(song_path, format='audio/mp3', start_time=0)
    
    # Like/Unlike
    movie_key = f"{year}_{movie}"
    if movie_key not in st.session_state['likes']:
        st.session_state['likes'][movie_key] = False
    
    col1, col2 = st.columns([1,3])
    with col1:
        if st.session_state['likes'][movie_key]:
            if st.button("💔 Unlike", key=f"unlike_{movie_key}"):
                st.session_state['likes'][movie_key] = False
        else:
            if st.button("❤️ Like", key=f"like_{movie_key}"):
                st.session_state['likes'][movie_key] = True
    with col2:
        st.write("Liked" if st.session_state['likes'][movie_key] else "Not liked yet")
    
    # Comments
    st.subheader("Comments")
    if movie_key not in st.session_state['comments']:
        st.session_state['comments'][movie_key] = []

    comment_input = st.text_input("Add a comment", key=f"comment_{movie_key}")
    if st.button("Post Comment", key=f"post_{movie_key}") and comment_input.strip() != "":
        st.session_state['comments'][movie_key].append(comment_input)
        st.experimental_rerun()

    for c in st.session_state['comments'][movie_key]:
        st.write(f"- {c}")
