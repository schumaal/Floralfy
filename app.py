import streamlit as st
from PIL import Image
from plants_info import plants_data

# ---------------------------
# Streamlit Config
# ---------------------------

st.set_page_config(
    page_title="🌿 Pflanzen Erkennung",
    page_icon="🌱",
    layout="centered"
)

# ---------------------------
# CSS Styling
# ---------------------------

st.markdown("""
<style>

body {
    background-color: #e8f5e9;
}

.main {
    background: linear-gradient(135deg, #c8e6c9, #e8f5e9);
    border-radius: 20px;
    padding: 20px;
}

h1 {
    color: #1b5e20;
    text-align: center;
}

.plant-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border-left: 8px solid #4caf50;
    margin-top: 20px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

.stButton>button {
    background-color: #43a047;
    color: white;
    border-radius: 10px;
    border: none;
}

.stTextInput>div>div>input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Modell laden
# ---------------------------


st.title("🌿 Pflanzen Erkennungs-App")
