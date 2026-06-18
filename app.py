import streamlit as st
from PIL import Image
from transformers import pipeline
import io

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
        font-size: 1.9rem;
    }
    .stButton>button {
        background-color: #4caf50;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .plant-card {
        background-color: white;
        padding: 22px;
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
        device=-1
    )

classifier = load_classifier()

# ====================== PFLANZEN-DATENBANK MIT VIEL MEHR ESOTERIK ======================
plant_db = {
    "daisy": {
        "name": "Gänseblümchen (Bellis perennis)",
        "info": [
            "🌼 Blüht fast ganzjährig",
            "Essbar (Blüten und Blätter)",
            "Bienenmagnet",
            "Sehr robust und trittfest",
            "🌟 Esoterik: Symbol für Unschuld, kindliche Freude und Neuanfang",
            "Verbindet mit dem inneren Kind, fördert Leichtigkeit und emotionale Heilung",
            "Hilft bei der Loslösung von alten Verletzungen"
        ]
    },
    "rose": {
        "name": "Rose (Rosa)",
        "info": [
            "🌹 Symbol der Liebe",
            "Über 300 Arten weltweit",
            "Blütezeit: Juni bis September",
            "Braucht sonnigen Standort und nährstoffreichen Boden",
            "🌟 Esoterik: Starke Herz-Chakra-Pflanze",
            "Steht für bedingungslose Liebe, Leidenschaft und spirituelle Öffnung des Herzens",
            "Fördert Selbstliebe, heilt Herzschmerz und aktiviert Venus-Energie"
        ]
    },
    "sunflower": {
        "name": "Sonnenblume (Helianthus annuus)",
        "info": [
            "🌻 Dreht sich mit der Sonne",
            "Bis 3 Meter hoch",
            "Liefert Öl und essbare Kerne",
            "Blütezeit: Juli bis Oktober",
            "🌟 Esoterik: Symbol für Lebensfreude, göttliches Licht und innere Stärke",
            "Stärkt das Solarplexus-Chakra, fördert Selbstvertrauen und Manifestation",
            "Sonnengott-Energie – Optimismus, Erfolg und spirituelle Ausrichtung"
        ]
    },
    "lavender": {
        "name": "Lavendel (Lavandula)",
        "info": [
            "💜 Beruhigender Duft",
            "Essbar",
            "Blütezeit: Juni bis August",
            "Liebt volle Sonne und trockenen Boden",
            "🌟 Esoterik: Mächtige Reinigungs- und Schutzpflanze",
            "Beruhigt den Geist, fördert tiefen Schlaf und spirituelle Klarheit",
            "Unterstützt Meditation und Verbindung zu höheren Bewusstseinsebenen"
        ]
    },
    "marigold": {
        "name": "Ringelblume (Calendula officinalis)",
        "info": [
            "🌼 Essbar und heilend",
            "Blütezeit: Mai bis Oktober",
            "Gute Bodenverbesserer",
            "🌟 Esoterik: Starke Schutzpflanze gegen negative Energien",
            "Fördert positive Transformation, Heilung und Feuer-Element-Energie",
            "Hilft bei der Loslassung alter Wunden"
        ]
    },
    "chamomile": {
        "name": "Kamille (Matricaria chamomilla)",
        "info": [
            "🌼 Berühmter Heiltee",
            "Essbar",
            "Blütezeit: Mai bis September",
            "🌟 Esoterik: Pflanze des inneren Friedens und der Sanftmut",
            "Beruhigt emotionale Stürme und fördert spirituelle Regeneration"
        ]
    },
    "violet": {
        "name": "Veilchen (Viola)",
        "info": [
            "🌸 Zarte Frühlingsblume",
            "Essbar",
            "Blüht März bis Mai",
            "🌟 Esoterik: Symbol für Bescheidenheit, Intuition und mystische Weisheit",
            "Öffnet das Dritte Auge, fördert spirituelle Einsichten und Verbindung zur Feenwelt"
        ]
    },
    "nasturtium": {
        "name": "Kapuzinerkresse (Tropaeolum majus)",
        "info": [
            "🌺 Essbare Blüten und Blätter (scharf)",
            "Blütezeit: Juni bis Oktober",
            "Schädlingsabwehrend",
            "🌟 Esoterik: Pflanze des Mutes, der Vitalität und des persönlichen Schutzes"
        ]
    },
    "lily": {
        "name": "Lilie (Lilium)",
        "info": [
            "⚪ Elegante Blüten",
            "Blütezeit: Juni bis August",
            "🌟 Esoterik: Symbol für Reinheit, spirituelles Erwachen und göttliche Weiblichkeit",
            "Stärkt das Kronen-Chakra"
        ]
    },
    "cornflower": {
        "name": "Kornblume (Centaurea cyanus)",
        "info": [
            "🌼 Leuchtend blau",
            "Blütezeit: Juni bis September",
            "Essbar",
            "🌟 Esoterik: Pflanze der Wahrheit, Treue und geistigen Klarheit",
            "Unterstützt die Kommunikation mit der geistigen Welt"
        ]
    },
    "narcissus": {
        "name": "Narzisse",
        "info": [
            "Blütezeit: März bis April",
            "🌟 Esoterik: Symbol für Wiedergeburt, Hoffnung und innere Erneuerung",
            "Hilft bei Neuanfängen und Selbstreflexion"
        ]
    }
}

st.markdown("<h1>🌿 Plantify</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.25rem;'>Dein Pflanzen-Erkenner mit tiefer Esoterik</p>", unsafe_allow_html=True)

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
                   
                    label_lower = top['label'].lower().replace(" ", "").replace("-", "")
                    key = next((k for k in plant_db if k in label_lower or plant_db[k]["name"].lower() in top['label'].lower()), None)
                   
                    if key:
                        info = plant_db[key]
                        st.markdown(f"<h3>{info['name']}</h3>", unsafe_allow_html=True)
                        for item in info["info"]:
                            st.markdown(f"• {item}")
                    else:
                        st.markdown("<h3>Weitere Informationen</h3>", unsafe_allow_html=True)
                        st.write("Diese Pflanze wird bald mit mehr esoterischen Details ergänzt.")
                   
                    st.subheader("Weitere mögliche Arten:")
                    for r in results[1:5]:
                        st.write(f"• {r['label']} ({r['score']:.1%})")
                except:
                    st.error("Fehler bei der Analyse. Bitte versuche ein anderes Bild.")

with tab2:
    search_term = st.text_input("🔍 Nach einer Pflanze suchen...", placeholder="Rose, Lavendel, Ringelblume...")
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
    st.markdown("### Über Plantify")
    st.write("KI-gestützte Pflanzenerkennung mit praktischen und tiefen esoterischen Informationen.")

st.caption("🌱 Viel Freude beim Entdecken der magischen Pflanzenwelt!")
