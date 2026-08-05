import streamlit as st
import requests

st.set_page_config(page_title="JARVIS", page_icon="🤖")
st.title("🤖 JARVIS  (IA du Raspberry Pi)")

# Remplace par ton adresse ngrok actuelle (sans /api/generate à la fin de la variable)
NGROK_URL = "https://tactile-varnish-cottage.ngrok-free.dev"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Dis quelque chose à ton PiDog..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Le PiDog réfléchit sur le Raspberry Pi..."):
            try:
                response = requests.post(
                    f"{NGROK_URL}/api/generate",
                    json={
                        "model": "llama3", 
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    answer = response.json().get("response", "Erreur de réponse de l'IA.")
                else:
                    answer = f"Erreur du serveur (Code {response.status_code}). Vérifie ton lien Ngrok."
            except Exception as e:
                answer = f"Impossible de joindre le Raspberry Pi : {e}"
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
