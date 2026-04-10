# src/web/app.py
import os
os.environ['CHROMA_TELEMETRY_OFF'] = 'True'

import streamlit as st
from dotenv import load_dotenv
from src.brain.rag_chain import PDPAChain

load_dotenv()

st.title("🇮🇩 PDPA Knowledge Bot (Local Data)")

if "pdpa_chain" not in st.session_state:
    # api_key = os.getenv("GOOGLE_API_KEY")
    api_key = "AIzaSyBd1uYoF7NgvBVLDrtW3xp1bGsv8-L2fHk"
    # api_key = "AIzaSyAiwGLzoUjuNrDNVRqnCFI74UxIqjcecvo"
    st.session_state.pdpa_chain = PDPAChain(api_key).get_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanyakan tentang UU PDP..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.pdpa_chain.invoke(prompt)
        st.markdown(response["result"])
        st.session_state.messages.append({"role": "assistant", "content": response["result"]})