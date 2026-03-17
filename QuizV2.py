import streamlit as st
import time
import random
import base64
import streamlit.components.v1 as components

# --- IMPORT DES QUESTIONS ---
from questions_data import data as questions_pool

# --- Configuration de la page ---
st.set_page_config(page_title="Quiz Nature", page_icon="", layout="centered")

# --- FONCTION POUR BACKGROUND GIF DEPUIS UN LIEN WEB ---
def set_web_gif_background(gif_url):
    css_style = f"""
    <style>
    .stApp {{
        /* On met directement ton lien URL ici ! */
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("{gif_url}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}
    h1, h2, h3, p, .stMarkdown, .stMetricLabel, .stMetricValue {{
        color: white !important;
        text-shadow: 2px 2px 5px black !important;
    }}
    .stButton button {{
        border: 2px solid white !important;
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
    }}
    .stButton button:hover {{
        background-color: rgba(255, 255, 255, 0.3) !important;
    }}
    </style>
    """
    st.markdown(css_style, unsafe_allow_html=True)

# --- Initialisation de la Session ---
if "etape" not in st.session_state:
    st.session_state.etape = "MENU"
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.locked = False
    st.session_state.questions_jeu = []

# --- FONCTIONS DE JEU ---
def lancer_partie(difficulte):
    st.session_state.difficulte_choisie = difficulte
    
    if difficulte == "Facile":
        st.session_state.temps_limite = 45
    elif difficulte == "Normal":
        st.session_state.temps_limite = 30
    else:
        st.session_state.temps_limite = 15

    pool = questions_pool[difficulte]
    st.session_state.questions_jeu = random.sample(pool, min(len(pool), 20))
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.etape = "QUIZ"
    st.session_state.locked = False
    st.session_state.q_index = -1 

def reset_jeu():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- INTERFACE PRINCIPALE ---

# 0. APPLICATION DU BACKGROUND GIF WEB
if "difficulte_choisie" in st.session_state and st.session_state.etape != "MENU":
    if st.session_state.difficulte_choisie == "Facile":
        set_web_gif_background("https://giffiles.alphacoders.com/972/9729.gif") 
    elif st.session_state.difficulte_choisie == "Normal":
        set_web_gif_background("https://giffiles.alphacoders.com/178/17823.gif")
    elif st.session_state.difficulte_choisie == "Difficile":
        set_web_gif_background("https://wallpaperaccess.com/full/20457670.gif")
else:
    # Fond par défaut pour le Menu
    set_web_gif_background("https://i.pinimg.com/originals/e3/c5/0e/e3c50e7b1996478539e5cb76c8ba12ae.gif")

# 1. ÉCRAN DE MENU
if st.session_state.etape == "MENU":
    st.title("Quiz Nature")
    st.subheader("Choisissez votre niveau de difficulté :")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("FACILE (45s)", use_container_width=True):
            lancer_partie("Facile")
            st.rerun()
    with col2:
        if st.button("NORMAL (30s)", use_container_width=True):
            lancer_partie("Normal")
            st.rerun()
    with col3:
        if st.button("DIFFICILE (15s)", use_container_width=True):
            lancer_partie("Difficile")
            st.rerun()

# 2. ÉCRAN DE QUIZ
elif st.session_state.etape == "QUIZ":
    # --- MISE À JOUR PAR QUESTION ---
    if st.session_state.q_index != st.session_state.index:
        st.session_state.q_index = st.session_state.index
        st.session_state.locked = False
        st.session_state.dernier_choix = None

    item = st.session_state.questions_jeu[st.session_state.index]
    t_limite = st.session_state.temps_limite

    with st.sidebar:
        st.title(f"Niveau : {st.session_state.difficulte_choisie}")
        st.metric("Score", f"{st.session_state.score} / 20")
        st.write(f"Question : {st.session_state.index + 1} / 20")
        st.divider()
        if st.button("Menu Principal"):
            reset_jeu()

    st.progress((st.session_state.index + 1) / 20)

    # --- LE CHRONOMÈTRE ---
    if not st.session_state.locked:
        html_chrono = f"""
        <style>
            body {{ font-family: sans-serif; margin: 0; padding: 0; background-color: transparent; }}
            .text {{ font-size: 20px; font-weight: bold; text-align: center; color: white; text-shadow: 1px 1px 3px black; margin-bottom: 5px; }}
            .bar-bg {{ width: 100%; background-color: rgba(255, 255, 255, 0.3); border-radius: 10px; height: 15px; overflow: hidden; backdrop-filter: blur(5px); }}
            .bar-fill {{ height: 100%; width: 100%; background-color: #28a745; transition: width 1s linear, background-color 0.5s ease; }}
        </style>
        <div>
            <div class="text" id="chrono_text">{t_limite} s</div>
            <div class="bar-bg">
                <div class="bar-fill" id="chrono_bar"></div>
            </div>
        </div>
        <script>
            let timeLeft = {t_limite};
            let totalTime = {t_limite};
            let textEl = document.getElementById("chrono_text");
            let barEl = document.getElementById("chrono_bar");

            let timer = setInterval(function() {{
                timeLeft -= 1;
                if (timeLeft > 0) {{
                    textEl.innerHTML = timeLeft + " s";
                    let pct = (timeLeft / totalTime) * 100;
                    barEl.style.width = pct + "%";
                    
                    if (pct > 50) {{ barEl.style.backgroundColor = "#28a745"; }}
                    else if (pct > 25) {{ barEl.style.backgroundColor = "#ffc107"; }}
                    else {{ barEl.style.backgroundColor = "#dc3545"; }}
                }} else {{
                    clearInterval(timer);
                    textEl.innerHTML = "TEMPS ÉCOULÉ !";
                    barEl.style.width = "0%";
                    let buttons = window.parent.document.querySelectorAll("button");
                    buttons.forEach(b => {{
                        if (b.innerText.includes("Passer la question")) {{ b.click(); }}
                    }});
                }}
            }}, 1000);
        </script>
        """
        components.html(html_chrono, height=75)

    # Zone de la question
    with st.container(border=True):
        st.markdown(f"### {item['q']}")

    # Mélange des options
    opt_key = f"opts_{st.session_state.index}"
    if opt_key not in st.session_state:
        opts = item["options"].copy()
        random.shuffle(opts)
        st.session_state[opt_key] = opts

    # Affichage des réponses
    col_a, col_b = st.columns(2)
    for i, option in enumerate(st.session_state[opt_key]):
        with (col_a if i % 2 == 0 else col_b):
            if st.button(option, use_container_width=True, disabled=st.session_state.locked, key=f"btn_{st.session_state.index}_{option}"):
                st.session_state.locked = True
                st.session_state.dernier_choix = option
                st.rerun()

    # Bouton Passer
    st.write("")
    if st.button("Passer la question", disabled=st.session_state.locked, type="primary"):
        st.session_state.locked = True
        st.session_state.dernier_choix = "TIMEOUT"
        st.rerun()

    # --- RÉSULTAT ---
    temps_pause = 0
    if st.session_state.locked:
        if st.session_state.dernier_choix == "TIMEOUT":
            st.error(f"**Temps écoulé !** La réponse était : {item['r']}")
            temps_pause = 4.0
        else:
            if st.session_state.dernier_choix == item["r"]:
                st.balloons()
                st.success(f"Correct ! (+1 point)")
                temps_pause = 2.0
                if "last_scored" not in st.session_state or st.session_state.last_scored != st.session_state.index:
                    st.session_state.score += 1
                    st.session_state.last_scored = st.session_state.index
            else:
                st.error(f"Faux. La réponse était : {item['r']}")
                temps_pause = 3.0
        
        time.sleep(temps_pause)
        if st.session_state.index < len(st.session_state.questions_jeu) - 1:
            st.session_state.index += 1
            st.session_state.locked = False
            st.rerun()
        else:
            st.session_state.etape = "FIN"
            st.rerun()

# 3. ÉCRAN DE FIN
elif st.session_state.etape == "FIN":
    st.snow()
    st.title("Terminé !")
    st.subheader(f"Difficulté : {st.session_state.difficulte_choisie}")
    
    pourcentage = (st.session_state.score / 20) * 100
    col1, col2 = st.columns(2)
    col1.metric("Score Final", f"{st.session_state.score} / 20")
    col2.metric("Réussite", f"{int(pourcentage)} %")

    if pourcentage == 100:
        st.success("**INCROYABLE !** Un score parfait !")
    elif pourcentage >= 50:
        st.info("**Bravo !** Tu t'es bien débrouillé.")
    else:
        st.warning("**Dommage !** Retente ta chance.")
    
    st.divider()
    if st.button("Rejouer (Menu Principal)", type="primary", use_container_width=True):
        reset_jeu()