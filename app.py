import streamlit as st
import requests

st.title("🤖 JARVIS (Robot à roues & IA)")

# --- CONFIGURATION ---
# Remplace par ton URL ngrok actuelle (pour parler au Raspberry Pi / Ollama)
NGROK_URL = "https://tactile-varnish-cottage.ngrok-free.dev" 

# Remplace par l'adresse IP locale de ton ESP32 (vue dans le moniteur série Arduino)
ESP32_IP = "192.168.10.230"  # <--- METS TON IP ICI

# Fonction pour envoyer l'ordre à l'ESP32
def commander_robot(action):
    try:
        url = f"http://{ESP32_IP}/{action}"
        # On envoie la requête à l'ESP32 avec un court délai d'attente
        requests.get(url, timeout=1)
        st.sidebar.success(action.capitalize() + " !")
    except Exception as e:
        st.sidebar.error(f"Erreur ESP32 : {e}")

# 1. Initialiser l'historique des messages s'il n'existe pas
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Afficher tous les anciens messages stockés
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Zone de saisie pour un nouveau message
if prompt := st.chat_input("Dis quelque chose à ton robot (ex: Avance, Recule, Stop)..."):
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Envoyer la requête à Ollama via ngrok
    with st.chat_message("assistant"):
        with st.spinner("L'IA réfléchit..."):
            try:
                response = requests.post(
                    f"{NGROK_URL}/api/generate",
                    json={
                        "model": "gemma:2b",
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    bot_response = response.json().get("response", "Pas de réponse.")
                    st.markdown(bot_response)
                    
                    # Ajouter la réponse de l'assistant à l'historique
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    
                    # --- ANALYSE DE LA REPONSE POUR BOUGER LE ROBOT ---
                    # On met le texte en minuscules pour faciliter la détection des mots
                    reponse_lower = bot_response.lower()
                    
                    if "avance" in reponse_lower or "avant" in reponse_lower:
                        commander_robot("forward")
                    elif "recule" in reponse_lower or "arriere" in reponse_lower:
                        commander_robot("backward")
                    elif "gauche" in reponse_lower:
                        commander_robot("left")
                    elif "droite" in reponse_lower:
                        commander_robot("right")
                    elif "stop" in reponse_lower or "arrête" in reponse_lower:
                        commander_robot("stop")
                        
                else:
                    st.error(f"Erreur du serveur : {response.status_code}")
            except Exception as e:
                st.error(f"Impossible de joindre le Raspberry Pi : {e}")
