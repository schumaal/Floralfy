import streamlit as st
from PIL import Image
from transformers import pipeline
import torch  # ← WICHTIG: Muss importiert sein!

st.set_page_config(
    page_title="🌿 Plantify",
    page_icon="🌱",
    layout="wide"
)

# Grünes Design
st.markdown("""
<style>
    .main {background-color: #f0f7f0;}
    h1, h2, h3 {color: #1b5e20;}
    .stButton>button {
        background-color: #4caf50; 
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .plant-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #81c784;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Modell laden
@st.cache_resource
def load_classifier():
    return pipeline(
        "image-classification", 
        model="google/vit-base-patch16-224",
        device=-1   # CPU
    )

classifier = load_classifier()

# Pflanzen-Datenbank
plant_db = {
    "daisy": {"name": "Gänseblümchen", "info": ["🌼 Blüht fast ganzjährig", "Essbar", "Bienenmagnet", "Liebt sonnige Wiesen"]},
    "rose": {"name": "Rose", "info": ["🌹 Symbol der Liebe", "Über 300 Arten", "Braucht viel Pflege", "Duftet intensiv"]},
    "sunflower": {"name": "Sonnenblume", "info": ["🌻 Dreht sich mit der Sonne", "Bis 3 Meter hoch", "Liefert Öl", "Sehr robust"]},
    "tulip": {"name": "Tulpe", "info": ["🌷 Frühjahrsblüher", "Beliebt in Gärten", "Viele Farben"]},
}

st.title("🌿 **Plantify** – Dein Pflanzen-Erkenner")
st.markdown("**KI erkennt Blumen & gibt Infos**")

tab1, tab2 = st.tabs(["📸 Bild hochladen", "🔍 Pflanze suchen"])

with tab1:
    uploaded_file = st.file_uploader("Pflanzenfoto hochladen", type=['jpg', 'jpeg', 'png', 'webp'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
        
        if st.button("🌱 Jetzt erkennen", type="primary"):
            with st.spinner("KI analysiert das Bild..."):
                try:
                    results = classifier(image)
                    
                    top = results[0]
                    st.success(f"**Erkannt:** {top['label']}")
                    st.info(f"**Konfidenz:** {top['score']:.1%}")
                    
                    # Passende Infos suchen
                    label_lower = top['label'].lower()
                    key = next((k for k in plant_db if k in label_lower), None)
                    
                    if key:
                        info = plant_db[key]
                        st.markdown(f"### {info['name']}")
                        for item in info["info"]:
                            st.markdown(f"• {item}")
                    else:
                        st.markdown("### Weitere Infos")
                        st.write("Schöne Pflanze! Mehr Details folgen bald.")
                    
                    # Top 3 Ergebnisse
                    st.subheader("Andere mögliche Arten:")
                    for r in results[1:4]:
                        st.write(f"• {r['label']} ({r['score']:.1%})")
                except Exception as e:
                    st.error("Fehler bei der Analyse. Versuche ein anderes Bild.")

with tab2:
    search_term = st.text_input("🔍 Nach einer Pflanze suchen...", placeholder="Rose, Gänseblümchen, Sonnenblume...")
    if search_term:
        matches = [v for k, v in plant_db.items() if search_term.lower() in k or search_term.lower() in v["name"].lower()]
        if matches:
            for m in matches:
                st.markdown(f"""
                <div class="plant-card">
                    <h3>{m['name']}</h3>
                    <ul>{"".join(f"<li>{item}</li>" for item in m['info'])}</ul>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Keine Treffer gefunden. Versuche andere Begriffe.")

with st.sidebar:
    st.image("https://picsum.photos/id/1015/300/200", use_column_width=True)
    st.markdown("### 🌱 Über Plantify")
    st.write("Verwendet Google ViT-Modell für Bilderkennung.")
    st.caption("Tipp: Gute Beleuchtung und klare Blüten verbessern die Genauigkeit.")

st.caption("🌱 Viel Spaß beim Erkunden der Pflanzenwelt!")
st.markdown("### 🌱 Über Plantify")
    st.write("Elegante KI-Pflanzenerkennung")
    st.caption("Schriftart: Great Vibes (ähnlich Bickham Script)")
