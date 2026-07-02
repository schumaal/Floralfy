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
</style>
""", unsafe_allow_html=True)

# Modell
@st.cache_resource
def load_classifier():
    return pipeline("image-classification", model="microsoft/resnet-50", device=-1)

classifier = load_classifier()

# Session State für eigene Blumen
if 'custom_plants' not in st.session_state:
    st.session_state.custom_plants = {}

# Basis-Datenbank mit viel Esoterik
plant_db = {
    "daisy": {
        "name": "Gänseblümchen (Bellis perennis)",
        "info": [
            "🌼 Blüht fast ganzjährig",
            "Essbar (Blüten und Blätter)",
            "Bienenmagnet",
            "Sehr robust",
            "🌟 Esoterik: Symbol für Unschuld, kindliche Freude und Neuanfang",
            "Verbindet mit dem inneren Kind, fördert Leichtigkeit und emotionale Heilung",
            "Hilft bei der Loslösung von alten Verletzungen"
        ]
    },
    "rose": {
        "name": "Rose (Rosa)",
        "info": [
            "🌹 Symbol der Liebe",
            "Blütezeit: Juni bis September",
            "🌟 Esoterik: Starke Herz-Chakra-Pflanze – bedingungslose Liebe",
            "Steht für Leidenschaft und spirituelle Öffnung des Herzens",
            "Fördert Selbstliebe und heilt Herzschmerz"
        ]
    },
    "sunflower": {
        "name": "Sonnenblume (Helianthus annuus)",
        "info": [
            "🌻 Folgt der Sonne",
            "Bis 3 Meter hoch",
            "🌟 Esoterik: Symbol für Lebensfreude, göttliches Licht und innere Stärke",
            "Stärkt das Solarplexus-Chakra und fördert Manifestation"
        ]
    },
    "lavender": {
        "name": "Lavendel (Lavandula)",
        "info": [
            "💜 Beruhigender Duft",
            "Essbar",
            "🌟 Esoterik: Mächtige Reinigungs- und Schutzpflanze",
            "Beruhigt den Geist, fördert tiefen Schlaf und spirituelle Klarheit"
        ]
    },
    "lily": {
        "name": "Lilie (Lilium)",
        "info": [
            "⚪ Elegante Blüten",
            "🌟 Esoterik: Symbol für Reinheit, spirituelles Erwachen und göttliche Weiblichkeit",
            "Stärkt das Kronen-Chakra"
        ]
    }
}

# Alle Pflanzen
all_plants = {**plant_db, **st.session_state.custom_plants}

st.markdown("<h1>🌿 Plantify</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.25rem;'>Dein erweiterbarer Pflanzen-Erkenner</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📸 Bild hochladen", "🔍 Suche", "➕ Neue Blume hinzufügen"])

with tab1:
    uploaded_file = st.file_uploader("Pflanzenfoto hochladen", type=['jpg', 'jpeg', 'png', 'webp'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
        
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        buf.seek(0)
        
        if st.button("🌱 Jetzt erkennen", type="primary"):
            with st.spinner("KI analysiert..."):
                try:
                    results = classifier(image)
                    top = results[0]
                    st.success(f"**Erkannt:** {top['label']}")
                    st.info(f"**Konfidenz:** {top['score']:.1%}")
                    
                    label_lower = top['label'].lower().replace(" ", "").replace("-", "")
                    key = next((k for k in all_plants if k in label_lower or all_plants[k]["name"].lower() in top['label'].lower()), None)
                    
                    if key:
                        p = all_plants[key]
                        st.markdown(f"<h3>{p['name']}</h3>", unsafe_allow_html=True)
                        for item in p["info"]:
                            st.markdown(f"• {item}")
                    else:
                        st.info("Diese Pflanze ist noch nicht detailliert hinterlegt.")
                except:
                    st.error("Fehler bei der Analyse.")

        st.download_button("📥 Foto speichern", data=buf, file_name="plantify_foto.jpg", mime="image/jpeg")

with tab2:
    search_term = st.text_input("🔍 Nach einer Pflanze suchen...", placeholder="Rose, Lavendel...")
    if search_term:
        matches = [v for k, v in all_plants.items() if search_term.lower() in k or search_term.lower() in v["name"].lower()]
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

with tab3:
    st.subheader("➕ Neue Blume zur Datenbank hinzufügen")
    new_name = st.text_input("Pflanzenname (z.B. Hortensie)")
    new_info = st.text_area("Infos, Esoterik & Facts (eine Zeile pro Punkt)")
    new_photo = st.file_uploader("Beispielfoto hochladen (optional)", type=['jpg', 'jpeg', 'png'])
    
    if st.button("Blume hinzufügen"):
        if new_name:
            info_list = [line.strip() for line in new_info.split("\n") if line.strip()]
            if not info_list:
                info_list = ["Keine weiteren Infos hinterlegt."]
            
            st.session_state.custom_plants[new_name.lower()] = {
                "name": new_name,
                "info": info_list
            }
            st.success(f"✅ **{new_name}** erfolgreich hinzugefügt!")
            st.rerun()
        else:
            st.warning("Bitte einen Namen angeben.")

with st.sidebar:
    st.markdown("### Über Plantify")
    st.write(f"Aktuell **{len(all_plants)}** Pflanzen in der Datenbank")
    st.caption("Wir helfen dir, deinen spirituellen weg mithilfe der Pflanzenwelt zu gehen. Tauche ein in die mystische Welt des Universums! Wir begleiten dich auf deinem spirituellen Weg und öffnen gemeinsam mit dir die Tore zur uralten Weisheit der Pflanzenwelt. Jede Pflanze trägt ihre eigene Energie, ihre eigene Geschichte und eine einzigartige Botschaft in sich – bereit, dich auf deinem persönlichen Pfad zu unterstützen.

Tauche ein in die mystische Verbindung zwischen Erde und Universum, entdecke die Kraft der Elemente und lerne, die Zeichen der Natur bewusster wahrzunehmen. Lass dich von der sanften Weisheit der Pflanzen inspirieren, finde Momente der Achtsamkeit und öffne dein Herz für die Magie, die dich umgibt.

Ob du nach innerer Balance, spiritueller Führung oder einer tieferen Verbindung zu dir selbst und der Natur suchst – diese Reise lädt dich ein, die verborgenen Energien der Pflanzen zu entdecken und ihre heilsame Präsenz in dein Leben zu integrieren.

Das Universum spricht auf vielfältige Weise zu uns. Manchmal genügt es, still zu werden und den Pflanzen zuzuhören.")

st.caption("🌱 Viel Freude beim Entdecken der magischen Pflanzenwelt!")
