import streamlit as st
from PIL import Image
from transformers import pipeline

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
    .stButton>button {background-color: #4caf50; color: white;}
</style>
""", unsafe_allow_html=True)

# Modell laden (mit Pipeline - viel stabiler)
@st.cache_resource
def load_classifier():
    return pipeline(
        "image-classification", 
        model="dtech-NN-team-3/flower-classifier",
        device=-1  # CPU
    )

classifier = load_classifier()

# ====================== APP ======================
st.title("🌿 **Plantify** – Pflanzen Erkenner")
st.markdown("**KI-basierte Blumen- & Pflanzenerkennung**")

tab1, tab2 = st.tabs(["📸 Bild hochladen", "🔍 Pflanze suchen"])

with tab1:
    uploaded_file = st.file_uploader("Pflanzenfoto hochladen", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Hochgeladenes Bild", use_column_width=True)
        
        if st.button("🌱 Pflanze erkennen", type="primary"):
            with st.spinner("KI analysiert das Bild..."):
                results = classifier(image)
                
                # Bestes Ergebnis
                top = results[0]
                st.success(f"**Erkannt:** {top['label']}")
                st.info(f"**Konfidenz:** {top['score']:.1%}")
                
                # Top 5 anzeigen
                st.subheader("Weitere mögliche Treffer:")
                for r in results[:5]:
                    st.write(f"• **{r['label']}** — {r['score']:.1%}")

with tab2:
    search = st.text_input("🔍 Nach Pflanze suchen (z.B. Rose, Daisy, Tulpe)")
    if search:
        st.info("Suche wird bald erweitert mit mehr Infos...")

with st.sidebar:
    st.markdown("### 🌱 Info")
    st.write("Modell: **dtech-NN-team-3/flower-classifier**")
    st.caption("Funktioniert am besten mit klaren Blütenfotos.")

st.caption("Hinweis: Das Modell erkennt vor allem Blumen.")
