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

# ====================== ERWEITERTE PFLANZEN-DATENBANK ======================
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
    }
flowers.extend([
    {
        "name": "Tulpe",
        "edible": True,
        "blooming_period": "April bis Mai",
        "requirements": "Sonnig bis halbschattig, lockerer Boden",
        "esoteric_meaning": "Neuanfang, Wohlstand, Frühlingsenergie"
    },
    {
        "name": "Narzisse",
        "edible": False,
        "blooming_period": "März bis April",
        "requirements": "Sonnig bis halbschattig, durchlässiger Boden",
        "esoteric_meaning": "Wiedergeburt, Hoffnung, Erneuerung"
    },
    {
        "name": "Pfingstrose",
        "edible": Teilweise,
        "blooming_period": "Mai bis Juni",
        "requirements": "Sonnig, nährstoffreicher Boden",
        "esoteric_meaning": "Glück, Liebe, Fülle"
    },
    {
        "name": "Dahlie",
        "edible": False,
        "blooming_period": "Juli bis Oktober",
        "requirements": "Sonnig, nährstoffreicher Boden, regelmäßiges Gießen",
        "esoteric_meaning": "Innere Stärke, Würde, Kreativität"
    },
    {
        "name": "Chrysantheme",
        "edible": Teilweise,
        "blooming_period": "September bis November",
        "requirements": "Sonnig, humusreicher Boden",
        "esoteric_meaning": "Langlebigkeit, Weisheit, Schutz"
    },
    {
        "name": "Mohn",
        "edible": Teilweise,
        "blooming_period": "Mai bis Juli",
        "requirements": "Viel Sonne, trockener Boden",
        "esoteric_meaning": "Träume, Transformation, Vergänglichkeit"
    },
    {
        "name": "Kornblume",
        "edible": True,
        "blooming_period": "Juni bis September",
        "requirements": "Sonniger Standort, mäßig trockener Boden",
        "esoteric_meaning": "Treue, Wahrheit, geistige Klarheit"
    },
    {
        "name": "Aster",
        "edible": False,
        "blooming_period": "August bis Oktober",
        "requirements": "Sonnig bis halbschattig",
        "esoteric_meaning": "Geduld, Vertrauen, Sternenenergie"
    },
    {
        "name": "Cosmea",
        "edible": Teilweise,
        "blooming_period": "Juni bis Oktober",
        "requirements": "Sonnig, durchlässiger Boden",
        "esoteric_meaning": "Harmonie, kosmische Ordnung"
    },
    {
        "name": "Geranie",
        "edible": False,
        "blooming_period": "Mai bis Oktober",
        "requirements": "Sonnig, regelmäßige Bewässerung",
        "esoteric_meaning": "Schutz, Stabilität, Erdung"
    },
    {
        "name": "Petunie",
        "edible": False,
        "blooming_period": "Mai bis Oktober",
        "requirements": "Viel Sonne, nährstoffreicher Boden",
        "esoteric_meaning": "Emotionale Heilung, Harmonie"
    },
    {
        "name": "Begonie",
        "edible": False,
        "blooming_period": "Juni bis Oktober",
        "requirements": "Halbschatten, feuchter Boden",
        "esoteric_meaning": "Vorsicht, Balance, Schutz"
    },
    {
        "name": "Fuchsie",
        "edible": True,
        "blooming_period": "Juni bis Oktober",
        "requirements": "Halbschatten, gleichmäßige Feuchtigkeit",
        "esoteric_meaning": "Eleganz, Anmut, Feenenergie"
    },
    {
        "name": "Lilie",
        "edible": False,
        "blooming_period": "Juni bis August",
        "requirements": "Sonnig bis halbschattig",
        "esoteric_meaning": "Reinheit, spirituelles Wachstum"
    },
    {
        "name": "Iris",
        "edible": False,
        "blooming_period": "Mai bis Juni",
        "requirements": "Sonniger Standort, durchlässiger Boden",
        "esoteric_meaning": "Botschaften der Seele, Weisheit"
    },
    {
        "name": "Magnolie",
        "edible": Teilweise,
        "blooming_period": "März bis Mai",
        "requirements": "Sonnig bis halbschattig, humusreicher Boden",
        "esoteric_meaning": "Würde, Schönheit, Mondkraft"
    },
    {
        "name": "Flieder",
        "edible": True,
        "blooming_period": "April bis Juni",
        "requirements": "Sonnig, nährstoffreicher Boden",
        "esoteric_meaning": "Erinnerung, Jugend, spirituelle Öffnung"
    },
    {
        "name": "Gänseblümchen",
        "edible": True,
        "blooming_period": "März bis Oktober",
        "requirements": "Sonnig bis halbschattig",
        "esoteric_meaning": "Unschuld, Freude, Kindlichkeit"
    },
    {
        "name": "Schafgarbe",
        "edible": True,
        "blooming_period": "Juni bis September",
        "requirements": "Sonnig, trockener Boden",
        "esoteric_meaning": "Schutz, Heilung, Mut"
    },
    {
        "name": "Borretsch",
        "edible": True,
        "blooming_period": "Juni bis September",
        "requirements": "Sonnig, lockerer Boden",
        "esoteric_meaning": "Mut, Zuversicht, Herzensstärke"
    }
])
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
                except Exception as e:
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
            st.info("Keine Treffer gefunden. Versuche andere Begriffe oder versuche die einzahl.")

with st.sidebar:
    st.markdown("### Über Plantify")
    st.write("KI-gestützte Pflanzenerkennung mit praktischen und kosmischen Infos.")
    st.caption("")

st.caption("🌱 Viel Freude beim Entdecken der Pflanzenwelt!")
