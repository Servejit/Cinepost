# ====================================================
# STREAMLIT APP: Bollywood Poster Gallery
# ====================================================
import streamlit as st
import os
from PIL import Image, ImageDraw

# -------------------------------
# Setup: Create posters folder & sample images
# -------------------------------
BASE_DIR = "posters"

# Sample data (Year -> Movies)
sample_data = {
    "2022": ["Gangubai.jpg", "RRR.jpg"],
    "2023": ["Jawan.jpg", "Pathaan.jpg"]
}

# Create folders and placeholder images if not exist
if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)

for year, movies in sample_data.items():
    year_folder = os.path.join(BASE_DIR, year)
    if not os.path.exists(year_folder):
        os.mkdir(year_folder)
    for movie in movies:
        file_path = os.path.join(year_folder, movie)
        if not os.path.exists(file_path):
            # Create a placeholder image
            img = Image.new('RGB', (300, 450), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.text((10, 200), movie.replace(".jpg",""), fill=(255, 255, 0))
            img.save(file_path)

# -------------------------------
# App Layout
# -------------------------------
st.set_page_config(page_title="🎬 Bollywood Posters", layout="wide")
st.title("🎬 Bollywood Posters Gallery")

# --- Functions ---
def get_years():
    return sorted([d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))])

def get_movies(year):
    folder = os.path.join(BASE_DIR, year)
    return sorted([f for f in os.listdir(folder) if f.lower().endswith((".jpg",".png",".jpeg"))])

# --- Session State for Likes/Comments ---
if 'likes' not in st.session_state:
    st.session_state['likes'] = {}
if 'comments' not in st.session_state:
    st.session_state['comments'] = {}

# --- Select Year ---
st.sidebar.title("Select Year")
years = get_years()
selected_year = st.sidebar.selectbox("Year", [""] + years)

# --- Movie Thumbnails in Sidebar ---
selected_movie = None
if selected_year:
    st.sidebar.title(f"Movies in {selected_year}")
    movies = get_movies(selected_year)
    
    for movie in movies:
        cols = st.sidebar.columns([1,4])
        movie_path = os.path.join(BASE_DIR, selected_year, movie)
        thumbnail = Image.open(movie_path).resize((50, 75))
        cols[0].image(thumbnail)
        if cols[1].button(movie.replace(".jpg",""), key=movie):
            selected_movie = movie

# --- Show Full Poster and Interaction ---
if selected_movie:
    movie_path = os.path.join(BASE_DIR, selected_year, selected_movie)
    st.image(Image.open(movie_path), use_column_width=True)

    # --- Like/Unlike ---
    movie_key = f"{selected_year}_{selected_movie}"
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

    # --- Comments ---
    st.subheader("Comments")
    if movie_key not in st.session_state['comments']:
        st.session_state['comments'][movie_key] = []

    comment_input = st.text_input("Add a comment", key=f"comment_{movie_key}")
    if st.button("Post Comment", key=f"post_{movie_key}") and comment_input.strip() != "":
        st.session_state['comments'][movie_key].append(comment_input)
        st.experimental_rerun()  # Refresh to show new comment

    for c in st.session_state['comments'][movie_key]:
        st.write(f"- {c}")
