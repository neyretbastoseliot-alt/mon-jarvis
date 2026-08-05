import streamlit as st
from google import genai

st.set_page_config(page_title="JARVIS AI", page_icon="🤖")
st.title("🤖 Mon Assistant JARVIS")

# Récupération sécurisée de la clé API depuis Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ La clé API Gemini n'est pas configurée dans les paramètres !")
else:
    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Discute avec JARVIS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Réflexion..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                    )
                    answer = response.text
                except Exception as e:
                    answer = f"Erreur : {e}"

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})