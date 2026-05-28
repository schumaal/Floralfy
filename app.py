import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification, AutoImageProcessor
import requests
import json
from io import BytesIO

# ====================== KONFIGURATION ======================
st.set_page_config(
    page_title="🌿 Plantify - Pflanzen Erkenner",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hugging Face Model
MODEL_NAME = "dtech-NN-team-3/flower-classifier"

# CSS für grünes, pflanzliches Design
st.markdown("""
<style>
    .main {
        background-color: #f0f7f0;
    }
    .stApp {
        background-image: 
            linear-gradient(rgba(46, 125, 50, 0.1), rgba(46, 125, 50, 0.1)),
            url('https://picsum.photos/id/1015/1920/1080');
        background-size: cover;
        background-attachment: fixed;
    }
    h1, h2, h3 {
        color: #1b5e20;
        font-family: 'Segoe UI', sans-serif;
    }
    .plant-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(27, 94, 32, 0.1);
        border: 1px solid #81c784;
    }
</style>
""", unsafe_allow_html=True)

# ====================== MODEL LADEN ======================
@st.cache_resource
def load_model():
    processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    return processor, model

processor, model = load_model()

# ====================== PFLANZEN DATENBANK (Beispiel) ======================
plant_info = {
    "daisy": {
        "name": "Gänseblümchen (Bellis perennis)",
        "deutsch": "Gänseblümchen",
        "info": [
            "🌼 Symbol für Unschuld und Neuanfang",
            "Blüht von März bis Oktober",
            "Essbar – Blüten und Blätter",
            "Liebt sonnige Wiesen",
            "Wichtige Bienen- und Schmetterlingspflanze"
        ]
    },
    "rose": {
        "name": "Rose (Rosa)",
        "deutsch": "Rose",
        "info": [
            "🌹 Die Königin der Blumen",
            "Über 300 Arten weltweit",
            "Symbol für Liebe und Schönheit",
            "Braucht viel Sonne und nährstoffreichen Boden",
            "Viele Sorten duften intensiv"
        ]
    },
    # Weitere Arten kannst du hier ergänzen...
}

# ====================== HAUPTAPP ======================
st.title("🌿 **Plantify** – Dein Pflanzen-Erkenner")
st.markdown("**Lade ein Bild hoch oder suche eine Pflanze**")

# Tabs
tab1, tab2 = st.tabs(["📸 Bild hochladen", "🔍 Pflanze suchen"])

with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        uploaded_file = st.file_uploader("Pflanzenfoto hochladen", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
            
            if st.button("🌱 Pflanze erkennen", type="primary"):
                with st.spinner("Analysiere Bild mit KI..."):
                    # Vorverarbeitung
                    inputs = processor(images=image, return_tensors="pt")
                    
                    # Vorhersage
                    with torch.no_grad():
                        outputs = model(**inputs)
                        logits = outputs.logits
                        predicted_class_idx = logits.argmax(-1).item()
                        predicted_label = model.config.id2label[predicted_class_idx]
                        confidence = torch.softmax(logits, dim=-1)[0][predicted_class_idx].item()
                    
                    st.success(f"**Erkannt:** {predicted_label}")
                    st.info(f"**Konfidenz:** {confidence:.1%}")
                    
                    # Info anzeigen
                    key = predicted_label.lower().split()[0]  # z.B. "daisy"
                    if key in plant_info:
                        info = plant_info[key]
                        st.markdown(f"### {info['name']}")
                        for bullet in info["info"]:
                            st.markdown(f"- {bullet}")
                    else:
                        st.markdown(f"### {predicted_label}")
                        st.write("Schöne Pflanze! Mehr Infos werden bald hinzugefügt.")

with tab2:
    search_term = st.text_input("🔍 Nach einer Pflanze suchen...", placeholder="z.B. Rose, Tulpe, Sonnenblume...")
    
    if search_term:
        results = [p for p in plant_info.values() if search_term.lower() in p["name"].lower() or 
                  search_term.lower() in p["deutsch"].lower()]
        
        if results:
            for p in results:
                st.markdown(f"""
                <div class="plant-card">
                    <h3>{p['name']}</h3>
                    <ul>
                    {''.join([f'<li>{item}</li>' for item in p['info']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Keine passenden Pflanzen gefunden. Versuche andere Begriffe.")

# Sidebar
with st.sidebar:
    st.image("https://picsum.photos/id/1015/300/200", use_column_width=True)
    st.markdown("### 🌱 Über Plantify")
    st.write("""
    KI-basierte Pflanzenerkennung mit dem Modell von **dtech-NN-team-3**.
    
    **Funktionen:**
    - Foto-Upload + KI-Erkennung
    - Pflanzen-Suche
    - Wissenswertes in Stichpunkten
    """)
    
    st.markdown("---")
    st.caption("Made with ❤️ für Pflanzenliebhaber")

# Footer
st.markdown("---")
st.markdown("**Hinweis:** Das Modell erkennt hauptsächlich Blumen. Für beste Ergebnisse klare Fotos von Blüten verwenden.")
