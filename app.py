import streamlit as st
import requests

st.set_page_config(page_title="JARVIS PiDog", page_icon="🤖")
st.title("🤖 JARVIS & PiDog (Local Ollama)")

# Historique de conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Parle à ton PiDog..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Le PiDog réfléchit..."):
            try:
                # Appel via le tunnel Ngrok vers ton Raspberry Pi
                response = requests.post(
                    "https://tactile-varnish-cottage.ngrok-free.app/api/generate",
                    json={
                        "model": "llama3", 
                        "prompt": prompt,
                        "stream": False
                    }
                )
                answer = response.json().get("response", "Erreur de réponse d'Ollama")
            except Exception as e:
                answer = f"Erreur de connexion à Ollama : {e}"
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
