import streamlit as st
from PIL import Image
from transformers import pipeline

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

# ====================== EINHEITLICHE PFLANZEN-DATENBANK ======================
plant_db = {
    "daisy": {
        "name": "Gänseblümchen (Bellis perennis)",
        "info": [
            "🌼 Blüht fast ganzjährig",
            "Essbar (Blüten und Blätter)",
            "Bienenmagnet",
            "Liebt sonnige Wiesen",
            "Sehr robust und trittfest"
        ]
    },
    "rose": {
        "name": "Rose (Rosa)",
        "info": [
            "🌹 Symbol der Liebe",
            "Über 300 Arten weltweit",
            "Blütezeit: Juni bis September",
            "Braucht sonnigen Standort und nährstoffreichen Boden",
            "Esoterische Bedeutung: Liebe, Herzenergie, Harmonie"
        ]
    },
    "sunflower": {
        "name": "Sonnenblume (Helianthus annuus)",
        "info": [
            "🌻 Dreht sich mit der Sonne",
            "Bis 3 Meter hoch",
            "Liefert Öl und essbare Kerne",
            "Blütezeit: Juli bis Oktober",
            "Esoterische Bedeutung: Lebenskraft, Optimismus, Erfolg"
        ]
    },
    "tulip": {
        "name": "Tulpe (Tulipa)",
        "info": [
            "🌷 Beliebte Frühlingsblume",
            "Blüht März bis Mai",
            "Viele Farben und Sorten",
            "Zwiebelpflanze"
        ]
    },
    "lavender": {
        "name": "Lavendel (Lavandula)",
        "info": [
            "💜 Beruhigender Duft",
            "Essbar",
            "Blütezeit: Juni bis August",
            "Liebt volle Sonne und trockenen Boden",
            "Esoterische Bedeutung: Reinigung, innere Ruhe, Schutz"
        ]
    },
    "marigold": {
        "name": "Ringelblume (Calendula officinalis)",
        "info": [
            "🌼 Essbar und heilend",
            "Blütezeit: Mai bis Oktober",
            "Gute Bodenverbesserer",
            "Esoterische Bedeutung: Heilung, Schutz, positive Transformation"
        ]
    },
    "chamomile": {
        "name": "Kamille (Matricaria chamomilla)",
        "info": [
            "🌼 Berühmter Heiltee",
            "Essbar",
            "Blütezeit: Mai bis September",
            "Esoterische Bedeutung: Frieden, Gelassenheit, Regeneration"
        ]
    },
    "dandelion": {
        "name": "Löwenzahn (Taraxacum officinale)",
        "info": [
            "🌼 Voll essbar (Blätter, Blüten, Wurzeln)",
            "Blütezeit: April bis Juni",
            "Sehr anspruchslos",
            "Esoterische Bedeutung: Wunscherfüllung, Freiheit"
        ]
    },
    "violet": {
        "name": "Veilchen (Viola)",
        "info": [
            "🌸 Zarte Frühlingsblume",
            "Essbar",
            "Blüht März bis Mai",
            "Esoterische Bedeutung: Bescheidenheit, Intuition"
        ]
    },
    "nasturtium": {
        "name": "Kapuzinerkresse (Tropaeolum majus)",
        "info": [
            "🌺 Essbare Blüten und Blätter (scharf)",
            "Blütezeit: Juni bis Oktober",
            "Schädlingsabwehrend",
            "Esoterische Bedeutung: Mut, Vitalität, Schutz"
        ]
    },
    # Neue erweiterte Einträge
    "narcissus": {"name": "Narzisse", "info": ["Blütezeit: März bis April", "Esoterische Bedeutung: Wiedergeburt, Hoffnung", "Nicht essbar"]},
    "peony": {"name": "Pfingstrose", "info": ["Blütezeit: Mai bis Juni", "Esoterische Bedeutung: Glück, Liebe, Fülle"]},
    "dahlia": {"name": "Dahlie", "info": ["Blütezeit: Juli bis Oktober", "Esoterische Bedeutung: Innere Stärke, Kreativität"]},
    "chrysanthemum": {"name": "Chrysantheme", "info": ["Blütezeit: September bis November", "Esoterische Bedeutung: Langlebigkeit, Weisheit"]},
    "cornflower": {"name": "Kornblume", "info": ["Blütezeit: Juni bis September", "Essbar", "Esoterische Bedeutung: Treue, Wahrheit"]},
    "lily": {"name": "Lilie", "info": ["Blütezeit: Juni bis August", "Esoterische Bedeutung: Reinheit, spirituelles Wachstum"]},
    "iris": {"name": "Iris", "info": ["Blütezeit: Mai bis Juni", "Esoterische Bedeutung: Weisheit, Botschaften der Seele"]},
    "lilac": {"name": "Flieder", "info": ["Blütezeit: April bis Juni", "Esoterische Bedeutung: Erinnerung, Jugend"]},
    "yarrow": {"name": "Schafgarbe", "info": ["Blütezeit: Juni bis September", "Essbar", "Esoterische Bedeutung: Schutz, Heilung"]},
}

st.markdown("<h1>🌿 Plantify</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.25rem;'>Dein Pflanzen-Erkenner mit erweiterten Informationen</p>", unsafe_allow_html=True)

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
                        st.write("Diese Pflanze wird bald mit mehr Details ergänzt.")
                    
                    st.subheader("Weitere mögliche Arten:")
                    for r in results[1:5]:
                        st.write(f"• {r['label']} ({r['score']:.1%})")
                except:
                    st.error("Fehler bei der Analyse. Bitte versuche ein anderes Bild.")

with tab2:
    search_term = st.text_input("🔍 Nach einer Pflanze suchen...", placeholder="Rose, Lavendel, Ringelblume, Narzisse...")
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
    st.write("KI-gestützte Pflanzenerkennung mit praktischen und esoterischen Infos.")

st.caption("🌱 Viel Freude beim Entdecken der Pflanzenwelt!")
