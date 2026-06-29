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
    return pipeline(
        "image-classification",
        model="microsoft/resnet-50",
        device=-1
    )

classifier = load_classifier()

# Pflanzen-Datenbank
plant_db = {
    "daisy": {"name": "Gänseblümchen (Bellis perennis)", "info": ["🌼 Blüht fast ganzjährig", "Essbar", "Bienenmagnet", "🌟 Esoterik: Unschuld, Neuanfang"]},
    "rose": {"name": "Rose (Rosa)", "info": ["🌹 Symbol der Liebe", "🌟 Esoterik: Herz-Chakra, bedingungslose Liebe"]},
    "sunflower": {"name": "Sonnenblume", "info": ["🌻 Folgt der Sonne", "🌟 Esoterik: Lebenskraft, Optimismus"]},
    "lavender": {"name": "Lavendel", "info": ["💜 Beruhigender Duft", "🌟 Esoterik: Reinigung, innere Ruhe"]},
    "lily": {"name": "Lilie", "info": ["⚪ Elegante Blüten", "🌟 Esoterik: Reinheit, spirituelles Erwachen"]},
}

st.markdown("<h1>🌿 Plantify</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.25rem;'>Dein Pflanzen-Erkenner</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📸 Bild hochladen", "🔍 Pflanze suchen"])

with tab1:
    uploaded_file = st.file_uploader("Pflanzenfoto hochladen", type=['jpg', 'jpeg', 'png', 'webp'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
        
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        buf.seek(0)
        
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
                    else:
                        st.info("Diese Pflanze wird bald mit mehr Details ergänzt.")
                except:
                    st.error("Fehler bei der Analyse.")
        
        st.download_button("📥 Foto speichern", data=buf, file_name="plantify_foto.jpg", mime="image/jpeg")

with tab2:
    search_term = st.text_input("🔍 Nach einer Pflanze suchen...", placeholder="Rose, Lavendel...")
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

st.caption("🌱 Viel Freude beim Entdecken der magischen Pflanzenwelt!")
