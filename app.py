import streamlit as st
from PIL import Image
from transformers import pipeline

st.set_page_config(
    page_title="🌿 Plantify",
    page_icon="🌱",
    layout="wide"
)

# Schönes grünes Design
st.markdown("""
<style>
    .main {background-color: #f0f7f0;}
    h1, h2, h3 {color: #1b5e20;}
    .stButton>button {
        background-color: #4caf50; 
        color: white;
        border-radius: 8px;
    }
    .plant-card {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #81c784;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Stabiles Flower-Modell
@st.cache_resource
def load_classifier():
    return pipeline(
        "image-classification", 
        model="google/vit-base-patch16-224",  # stabiles Modell
        device=-1  # CPU
    )

classifier = load_classifier()

# Pflanzen-Info (erweiterbar)
plant_db = {
    "daisy": {"name": "Gänseblümchen", "info": ["🌼 Blüht fast ganzjährig", "Essbar", "Liebt Sonne", "Bienenfreundlich"]},
    "rose": {"name": "Rose", "info": ["🌹 Königin der Blumen", "Symbol für Liebe", "Viele Duftsorten"]},
    "sunflower": {"name": "Sonnenblume", "info": ["🌻 Folgt der Sonne", "Bis zu 3m hoch", "Ölproduktion"]},
    # Weitere hinzufügen...
}

st.title("🌿 **Plantify** – Pflanzen Erkenner")
st.markdown("**KI erkennt Blumen & Pflanzen**")

tab1, tab2 = st.tabs(["📸 Bild hochladen", "🔍 Suche"])

with tab1:
    uploaded_file = st.file_uploader("Foto hochladen", type=['jpg', 'jpeg', 'png', 'webp'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Dein Foto", use_column_width=True)
        
        if st.button("🌱 Jetzt erkennen", type="primary"):
            with st.spinner("KI analysiert..."):
                results = classifier(image)
                
                top = results[0]
                label = top['label'].lower().replace(" ", "_")
                
                st.success(f"**Erkannt:** {top['label']}")
                st.info(f"**Konfidenz:** {top['score']:.1%}")
                
                # Info anzeigen
                key = next((k for k in plant_db if k in label), None)
                if key:
                    info = plant_db[key]
                    st.markdown(f"### {info['name']}")
                    for item in info["info"]:
                        st.markdown(f"• {item}")
                else:
                    st.write("Mehr Infos zu dieser Art folgen bald.")

with tab2:
    search_term = st.text_input("🔍 Pflanze suchen...", placeholder="z.B. Rose, Daisy, Sonnenblume")
    if search_term:
        matches = [v for k, v in plant_db.items() if search_term.lower() in k or search_term.lower() in v["name"].lower()]
        if matches:
            for m in matches:
                st.markdown(f"""
                <div class="plant-card">
                    <h3>{m['name']}</h3>
                    <ul>{"".join(f"<li>{i}</li>" for i in m['info'])}</ul>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Keine Treffer. Versuche andere Schreibweise.")

with st.sidebar:
    st.markdown("### Über Plantify")
    st.write("Verwendet ein stabiles Vision-Modell von Google.")
    st.caption("Tipp: Klare, gut beleuchtete Fotos funktionieren am besten.")

st.caption("🌱 Viel Spaß beim Entdecken der Pflanzenwelt!")
