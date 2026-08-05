import streamlit as st
import requests

# Configuration de la page
st.set_page_config(page_title="JARVIS & PiDog", page_icon="🤖")

st.title("🤖 JARVIS (IA du Raspberry Pi)")

# Remplace par ton URL ngrok actuelle exacte (avec le bon .dev ou .app)
NGROK_URL = "https://tactile-varnish-cottage.ngrok-free.dev"

# Initialisation de l'historique des messages dans la session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie du texte pour l'utilisateur
if prompt := st.chat_input("Dis quelque chose à ton PiDog..."):
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Requête vers ton Raspberry Pi via Ngrok et Ollama
    with st.chat_message("assistant"):
        with st.spinner("Réflexion en cours..."):
            try:
                response = requests.post(
                    f"{NGROK_URL}/api/generate",
                    json={
                        "model": "gemma:2b",  # Modifie si tu utilises un autre modèle (ex: llama3.1)
                        "prompt": prompt,
                        "stream": False
                    },
                    headers={"ngrok-skip-browser-warning": "true"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    bot_response = data.get("response", "Réponse vide de l'IA.")
                    st.markdown(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                else:
                    error_msg = f"Erreur du serveur (Code {response.status_code}). Vérifie ton lien Ngrok."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Impossible de joindre le Raspberry Pi : {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
