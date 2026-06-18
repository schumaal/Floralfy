import streamlit as st
from PIL import Image
from transformers import pipeline
import io

st.set_page_config(
    page_title="🌿 Plantify",
    page_icon="🌱",
    layout="wide"
)

# Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
    * {font-family: 'Times New Roman', Times, serif !important;}
    .main {background-color: #f0f7f0;}
    h1 {color: #1b5e20; font-size: 3.0rem; text-align: center; margin-bottom: 10px;}
    h3 {color: #1b5e20; font-size: 1.9rem;}
    .stButton>button {background-color: #4caf50; color: white; border-radius: 8px; font-weight: bold;}
    .plant-card {
        background-color: white;
        padding: 22px;
        border-radius: 15px;
        border: 2px solid #81c784;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .example-img {border-radius: 12px; margin: 10px 0;}
</style>
""", unsafe_allow_html=True)

# Modell
@st.cache_resource
def load_classifier():
    return pipeline("image-classification", model="google/vit-base-patch16-224", device=-1)

classifier = load_classifier()

# ====================== DATENBANK MIT ERWEITERTER ESOTERIK ======================
plant_db = {
    "daisy": {
        "name": "Gänseblümchen (Bellis perennis)",
        "info": [
            "🌼 Blüht fast ganzjährig",
            "Essbar (Blüten und Blätter)",
            "Bienenmagnet & sehr robust",
            "🌟 Esoterik: Symbol für Unschuld, kindliche Freude und Neuanfang",
            "Hilft bei der Verbindung zum inneren Kind und fördert Leichtigkeit",
            "Unterstützt emotionale Heilung nach schmerzhaften Erfahrungen"
        ],
        "example_image": "https://picsum.photos/id/1015/600/400"
    },
    "rose": {
        "name": "Rose (Rosa)",
        "info": [
            "🌹 Die Königin der Blumen",
            "Blütezeit: Juni bis September",
            "🌟 Esoterik: Starke Herz-Chakra-Pflanze",
            "Symbol für bedingungslose Liebe, Leidenschaft und spirituelle Öffnung",
            "Hilft bei der Heilung von Herzschmerz und fördert Selbstliebe",
            "Venus-Energie – Schönheit, Sinnlichkeit und Harmonie"
        ],
        "example_image": "https://picsum.photos/id/1016/600/400"
    },
    "sunflower": {
        "name": "Sonnenblume (Helianthus annuus)",
        "info": [
            "🌻 Folgt der Sonne",
            "Bis 3 Meter hoch",
            "🌟 Esoterik: Symbol für Lebensfreude, Vitalität und göttliches Licht",
            "Stärkt das Solarplexus-Chakra und das Selbstvertrauen",
            "Hilft bei der Manifestation von Zielen und innerer Stärke",
            "Sonnengott-Energie – Optimismus und Erfolg"
        ],
        "example_image": "https://picsum.photos/id/1074/600/400"
    },
    "lavender": {
        "name": "Lavendel (Lavandula)",
        "info": [
            "💜 Beruhigender Duft",
            "Essbar",
            "🌟 Esoterik: Starke Reinigungs- und Schutzpflanze",
            "Beruhigt den Geist und fördert tiefen, erholsamen Schlaf",
            "Unterstützt Meditation und spirituelle Klarheit",
            "Verbindet mit höheren Bewusstseinsebenen"
        ],
        "example_image": "https://picsum.photos/id/201/600/400"
    },
    "marigold": {
        "name": "Ringelblume (Calendula officinalis)",
        "info": [
            "🌼 Essbar und heilend",
            "🌟 Esoterik: Starke Schutzpflanze gegen negative Energien",
            "Fördert positive Transformation und innere Heilung",
            "Verbindung zur Sonne und zum Feuer-Element",
            "Hilft bei der Loslassung alter Wunden"
        ],
        "example_image": "https://picsum.photos/id/251/600/400"
    },
    "chamomile": {
        "name": "Kamille (Matricaria chamomilla)",
        "info": [
            "🌼 Berühmter Heiltee",
            "🌟 Esoterik: Pflanze des inneren Friedens und der Sanftmut",
            "Beruhigt emotionale Turbulenzen",
            "Fördert Gelassenheit und spirituelle Regeneration"
        ],
        "example_image": "https://picsum.photos/id/292/600/400"
    },
    "violet": {
        "name": "Veilchen (Viola)",
        "info": [
            "🌸 Zarte Frühlingsblume",
            "🌟 Esoterik: Symbol für Bescheidenheit, Intuition und mystische Weisheit",
            "Öffnet das Dritte Auge und fördert spirituelle Einsichten",
            "Hilft bei der Verbindung zur Feenwelt"
        ],
        "example_image": "https://picsum.photos/id/1018/600/400"
    },
    "nasturtium": {
        "name": "Kapuzinerkresse (Tropaeolum majus)",
        "info": [
            "🌺 Essbar mit scharfem Geschmack",
            "🌟 Esoterik: Pflanze des Mutes und der Lebensfreude",
            "Stärkt die persönliche Kraft und schützt vor Energievampiren"
        ],
        "example_image": "https://picsum.photos/id/866/600/400"
    },
    "lily": {
        "name": "Lilie (Lilium)",
        "info": [
            "⚪ Elegante Blüten",
            "🌟 Esoterik: Symbol für Reinheit, spirituelles Erwachen und göttliche Weiblichkeit",
            "Starkes Kronen-Chakra"
        ],
        "example_image": "https://picsum.photos/id/312/600/400"
    },
    "cornflower": {
        "name": "Kornblume (Centaurea cyanus)",
        "info": [
            "🌼 Leuchtend blau",
            "🌟 Esoterik: Pflanze der Wahrheit, Treue und geistigen Klarheit",
            "Unterstützt die Kommunikation mit der geistigen Welt"
        ],
        "example_image": "https://picsum.photos/id/1015/600/400"
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
        
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        buf.seek(0)
        
        col1, col2 = st.columns([3, 1])
        with col1:
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
                            p = plant_db[key]
                            st.markdown(f"<h3>{p['name']}</h3>", unsafe_allow_html=True)
                            for item in p["info"]:
                                st.markdown(f"• {item}")
                            
                            st.subheader("📸 Beispielfoto")
                            st.image(p["example_image"], use_column_width=True)
                        else:
                            st.info("Diese Pflanze wird bald mit mehr esoterischen Infos ergänzt.")
                    except:
                        st.error("Fehler bei der Analyse.")
        
        with col2:
            st.download_button(
                label="📥 Foto speichern",
                data=buf,
                file_name="plantify_foto.jpg",
                mime="image/jpeg"
            )

with tab2:
    search_term = st.text_input("🔍 Nach einer Pflanze suchen...", placeholder="Rose, Lavendel, Lilie...")
    if search_term:
        matches = [v for k, v in plant_db.items() if search_term.lower() in k or search_term.lower() in v["name"].lower()]
        if matches:
            for m in matches:
                st.markdown(f"""
                <div class="plant-card">
                    <h3>{m['name']}</h3>
                    <ul>{"".join(f"<li>{item}</li>" for item in m['info'])}</ul>
                    <img src="{m['example_image']}" class="example-img" width="100%">
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Keine Treffer gefunden.")

with st.sidebar:
    st.markdown("### Über Plantify")
    st.write("KI-Erkennung • Praktische Infos • Tiefe Esoterik & Symbolik")

st.caption("🌱 Viel Freude beim Entdecken der magischen Pflanzenwelt!")
