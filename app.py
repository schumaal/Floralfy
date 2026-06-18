import streamlit as st
from PIL import Image
from transformers import pipeline
import torch

st.set_page_config(
    page_title="🌿 Plantify",
    page_icon="🌱",
    layout="wide"
)

# Design mit Times New Roman
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');

    * {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    .main {background-color: #f0f7f0;}
    
    h1 {
        color: #1b5e20;
        font-size: 3.0rem;
        text-align: center;
        margin-bottom: 10px;
    }
    
    h3 {
        color: #1b5e20;
        font-size: 1.8rem;
    }
    
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
    
    /* Überschriften etwas eleganter machen */
    h1, h2, h3 {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Modell laden
@st.cache_resource
def load_classifier():
    return pipeline(
        "image-classification", 
        model="google/vit-base-patch16-224",
        device=-1
    )

classifier = load_classifier()

# Pflanzen-Datenbank
plant_db = {
    "daisy": {"name": "Gänseblümchen", "info": ["🌼 Blüht fast ganzjährig", "Essbar", "Bienenmagnet", "Liebt sonnige Wiesen"]},
    "rose": {"name": "Rose", "info": ["🌹 Symbol der Liebe", "Über 300 Arten", "Braucht viel Pflege", "Duftet intensiv"]},
    "sunflower": {"name": "Sonnenblume", "info": ["🌻 Dreht sich mit der Sonne", "Bis 3 Meter hoch", "Liefert Öl", "Sehr robust"]},
    "tulip": {"name": "Tulpe", "info": ["🌷 Frühjahrsblüher", "Beliebt in Gärten", "Viele Farben"]},
    flowers = [
    {
        "name": "Rose",
        "edible": True,
        "blooming_period": "Juni bis September",
        "requirements": "Sonniger Standort, nährstoffreicher Boden, regelmäßige Bewässerung",
        "esoteric_meaning": "Liebe, Herzenergie, Harmonie, Venus-Energie"
    },
    {
        "name": "Lavendel",
        "edible": True,
        "blooming_period": "Juni bis August",
        "requirements": "Volle Sonne, trockener und durchlässiger Boden",
        "esoteric_meaning": "Reinigung, Schutz, innere Ruhe, spirituelle Klarheit"
    },
    {
        "name": "Sonnenblume",
        "edible": True,
        "blooming_period": "Juli bis Oktober",
        "requirements": "Viel Sonne, nährstoffreicher Boden, ausreichend Wasser",
        "esoteric_meaning": "Lebenskraft, Erfolg, Sonnenenergie, Optimismus"
    },
    {
        "name": "Ringelblume",
        "edible": True,
        "blooming_period": "Mai bis Oktober",
        "requirements": "Sonnig bis halbschattig, lockerer Boden",
        "esoteric_meaning": "Heilung, Schutz, positive Transformation"
    },
    {
        "name": "Kamille",
        "edible": True,
        "blooming_period": "Mai bis September",
        "requirements": "Sonniger Standort, mäßig trockener Boden",
        "esoteric_meaning": "Frieden, Gelassenheit, Regeneration"
    },
    {
        "name": "Löwenzahn",
        "edible": True,
        "blooming_period": "April bis Juni",
        "requirements": "Anspruchslos, sonnig bis halbschattig",
        "esoteric_meaning": "Wunscherfüllung, Freiheit, Manifestation"
    },
    {
        "name": "Veilchen",
        "edible": True,
        "blooming_period": "März bis Mai",
        "requirements": "Halbschatten, humusreicher Boden",
        "esoteric_meaning": "Bescheidenheit, Intuition, spirituelle Weisheit"
    },
    {
        "name": "Kapuzinerkresse",
        "edible": True,
        "blooming_period": "Juni bis Oktober",
        "requirements": "Sonnig bis halbschattig, mäßig nährstoffreicher Boden",
        "esoteric_meaning": "Mut, Schutz, Vitalität"
    },
    {
        "name": "Jasmin",
        "edible": Teilweise,
        "blooming_period": "Mai bis September",
        "requirements": "Warmer, sonniger Standort, durchlässiger Boden",
        "esoteric_meaning": "Liebe, Sinnlichkeit, Mondenergie"
    },
    {
        "name": "Hibiskus",
        "edible": True,
        "blooming_period": "Juli bis September",
        "requirements": "Sonnig, windgeschützt, nährstoffreicher Boden",
        "esoteric_meaning": "Leidenschaft, Weiblichkeit, Lebensfreude"
    }
]
}

st.markdown("<h1>🌿 Plantify</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Dein Pflanzen-Erkenner</p>", unsafe_allow_html=True)

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
                    
                    label_lower = top['label'].lower()
                    key = next((k for k in plant_db if k in label_lower), None)
                    
                    if key:
                        info = plant_db[key]
                        st.markdown(f"<h3>{info['name']}</h3>", unsafe_allow_html=True)
                        for item in info["info"]:
                            st.markdown(f"• {item}")
                    else:
                        st.markdown("<h3>Weitere Informationen</h3>", unsafe_allow_html=True)
                        st.write("Mehr Details zu dieser Pflanze folgen bald.")
                    
                    st.subheader("Weitere mögliche Arten:")
                    for r in results[1:4]:
                        st.write(f"• {r['label']} ({r['score']:.1%})")
                except:
                    st.error("Fehler bei der Analyse. Bitte anderes Bild versuchen.")

with tab2:
    search_term = st.text_input("🔍 Nach einer Pflanze suchen...", placeholder="Rose, Gänseblümchen...")
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
            st.info("Keine Treffer gefunden.")

with st.sidebar:
    st.markdown("### Über Plantify")
    st.write("KI-gestützte Pflanzenerkennung")
    st.caption("Schriftart: Times New Roman")

st.caption("🌱 Viel Freude beim Entdecken der Pflanzenwelt!")
