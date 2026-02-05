import streamlit as st
import time

# --- Configuration de la page ---
st.set_page_config(page_title="Nature Quiz Pro", page_icon="🌿", layout="centered")

# --- Nos questions ---
questions = [
    {"q": "Quel est l'arbre fruitier le plus répandu en Guadeloupe ?", "options": ["Bananier", "Cocotier", "Manguier", "Goyavier"], "r": "Bananier"},
    {"q": "Quel est le volatile le plus rapide ?", "options": ["Faucon pèlerin", "Martinet noir", "Aigle royal", "Hirondelle"], "r": "Faucon pèlerin"},
    {"q": "Quel est l'animal le plus répandu en Guadeloupe ?", "options": ["Être humain", "Anolis (lézard)", "Moustique", "Rat"], "r": "Être humain"},
    {"q": "Combien y a-t-il de plages dans le monde ?", "options": ["Impossible à déterminer précisément", "Plusieurs dizaines de milliers", "Plus de 100 000", "Plusieurs centaines de milliers"], "r": "Impossible à déterminer précisément"},
    {"q": "Quel est le plus grand océan de la planète ?", "options": ["Océan Pacifique", "Océan Atlantique", "Océan Indien", "Océan Austral"], "r": "Océan Pacifique"},
    {"q": "Quel gaz est majoritairement responsable de l'effet de serre naturel ?", "options": ["Vapeur d'eau (H2O)", "Dioxyde de carbone (CO2)", "Méthane (CH4)", "Ozone (O3)"], "r": "Vapeur d'eau (H2O)"},
    {"q": "Quel est le biome dominant en Afrique centrale ?", "options": ["Forêt tropicale humide", "Savane tropicale", "Zones humides", "Forêt de montagne"], "r": "Forêt tropicale humide"},
    {"q": "Quel animal possède le plus gros cerveau en proportion de son corps ?", "options": ["Fourmi", "Dauphin", "Corbeau", "Pieuvre"], "r": "Fourmi"},
    {"q": "Comment s'appelle l'étude du comportement animal ?", "options": ["Éthologie", "Psychologie animale", "Sociobiologie", "Neuroéthologie"], "r": "Éthologie"},
    {"q": "Quelle couche de l'atmosphère contient la couche d'ozone ?", "options": ["Stratosphère", "Troposphère", "Mésosphère", "Thermosphère"], "r": "Stratosphère"},
    {"q": "Quel est le fruit le plus riche en sucre ?", "options": ["Datte", "Figue sèche", "Raisin sec", "Banane mûre"], "r": "Datte"}
]

# --- Initialisation des variables de session ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.fini = False

# --- MENU LATÉRAL ---
with st.sidebar:
    st.title("⚙️ Menu")
    st.write(f"**Joueur:** Utilisateur")
    st.write(f"**Score actuel:** {st.session_state.score}")
    st.write(f"**Progression:** {st.session_state.index + 1}/{len(questions)}")
    
    if st.button("🔄 Recommencer le quiz"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.fini = False
        st.rerun()
    
    st.divider()
    st.info("Projet Python : Quiz Nature (Guadeloupe)")

# --- INTERFACE PRINCIPALE ---
st.title("🌿 Quiz Nature & Environnement")

if not st.session_state.fini:
    # Barre de progression en haut
    progress = (st.session_state.index) / len(questions)
    st.progress(progress)
    
    item = questions[st.session_state.index]
    
    st.subheader(f"Question {st.session_state.index + 1}")
    st.markdown(f"#### {item['q']}")

    # Affichage des boutons pour les réponses
    for option in item["options"]:
        if st.button(option, use_container_width=True):
            if option == item["r"]:
                st.success(f"✔️ **Bonne réponse !** ({option})")
                st.session_state.score += 1
            else:
                st.error(f"❌ **Mauvaise réponse...** La réponse était : {item['r']}")
            
            # Attendre un peu pour que le joueur voit le message vert/rouge
            time.sleep(1.5)
            
            # Passer à la question suivante
            if st.session_state.index < len(questions) - 1:
                st.session_state.index += 1
                st.rerun()
            else:
                st.session_state.fini = True
                st.rerun()

else:
    # FIN DU JEU
    st.balloons()
    st.header("🎮 Partie terminée !")
    
    # Calcul du pourcentage pour le message final
    pourcentage = (st.session_state.score / len(questions)) * 100
    
    col1, col2 = st.columns(2)
    col1.metric("Score Final", f"{st.session_state.score} / {len(questions)}")
    col2.metric("Réussite", f"{int(pourcentage)}%")

    if pourcentage == 100:
        st.success("🏆 Incroyable ! Un sans faute !")
    elif pourcentage >= 50:
        st.info("🌿 Bien joué, tu as une bonne culture générale.")
    else:
        st.warning("🍃 Continue d'apprendre, la nature est pleine de surprises !")

    if st.button("Rejouer", type="primary"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.fini = False
        st.rerun()