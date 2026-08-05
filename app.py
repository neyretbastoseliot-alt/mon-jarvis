import streamlit as st
import requests

st.title("🤖 JARVIS (Interface IA)")

# URL ngrok pour communiquer avec ton Raspberry Pi / Ollama
NGROK_URL = "https://tactile-varnish-cottage.ngrok-free.dev"

# Initialiser l'historique des messages s'il n'existe pas
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher les anciens messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie pour discuter avec l'IA
if prompt := st.chat_input("Écris ton message ici..."):
    # Ajouter le message utilisateur à l'historique
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
                else:
                    st.error(f"Erreur du serveur : {response.status_code}")
            except Exception as e:
                st.error(f"Impossible de joindre le serveur : {e}")
