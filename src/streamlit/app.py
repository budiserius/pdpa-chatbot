# src/streamlit/app.py
import os
import streamlit as st
from dotenv import load_dotenv

os.environ['CHROMA_TELEMETRY_OFF'] = 'True'
load_dotenv()

from src.brain.rag_chain import PDPAChain

# 1. Dictionary Multibahasa
LANG_DICT = {
    "ID": {
        "title": "Indonesia PDPA Chat Bot",
        "caption": "Asisten cerdas untuk regulasi data pribadi Indonesia",
        "sidebar_info": "Chatbot RAG (Retrieval-Augmented Generation) untuk regulasi data pribadi Indonesia.",
        "init_brain": "⏳ Inisialisasi LLM...",
        "welcome": "Halo! Ada yang ingin ditanyakan seputar UU PDP?",
        "input_placeholder": "Tanyakan sesuatu...",
        "searching": "Mencari referensi...",
        "error_key": "⚠️ GROQ_API_KEY tidak ditemukan!",
        "author": "Penulis"
    },
    "EN": {
        "title": "Indonesia PDPA Chat Bot",
        "caption": "Intelligent assistant for Indonesian data privacy regulations",
        "sidebar_info": "A RAG (Retrieval-Augmented Generation) Indonesian data privacy regulations.",
        "init_brain": "⏳ Initializing LLM...",
        "welcome": "Hello! Do you have any questions regarding the PDPA Law?",
        "input_placeholder": "Ask something...",
        "searching": "Searching references...",
        "error_key": "⚠️ GROQ_API_KEY not found!",
        "author": "Author"
    }
}

st.set_page_config(
    page_title="PDPA Chatbot",
    layout="wide"
)

with st.sidebar:
    # Selector Bahasa
    lang_code = st.selectbox("🌐 Language / Bahasa", options=["ID", "EN"])
    t = LANG_DICT[lang_code]
    
    st.title("🛡️ Info Project")
    st.markdown(f"""
    {t['sidebar_info']}
    
    **Tech Stack:**
    - Language: Python 3.12
    - Framework: LangChain
    - LLM: Groq (Llama-3.3-70b-versatile)
    - Embeddings: HuggingFace (sentence-transformers/all-MiniLM-L6-v2)
    - Vector DB: ChromaDB
    - UI: Streamlit
    
    ---
    **{t['author']}:**
    **Muhammad Budi Setiawan**
    
    [![GitHub](https://img.icons8.com/glyph-neue/24/808080/github.png)](https://github.com/mbudisetiawan) [GitHub](https://github.com/budiserius)  
    [![LinkedIn](https://img.icons8.com/color/24/000000/linkedin.png)](https://linkedin.com/in/mbudisetiawan) [LinkedIn](https://linkedin.com/in/mbudis)
    
    *v1.0.0*
    """)

# 3. Custom CSS
st.markdown("""
    <style>
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-family: sans-serif;
        font-size: 12px;
        color: gray;
        opacity: 0.5;
        z-index: 100;
        pointer-events: none;
    }
    </style>
    <div class="watermark">Built by Muhammad Budi Setiawan</div>
    """, unsafe_allow_html=True)

# 4. Main UI
st.title(t["title"])
st.caption(t["caption"])

if "pdpa_chain" not in st.session_state:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error(t["error_key"])
        st.stop()
    
    with st.spinner(t["init_brain"]):
        st.session_state.pdpa_chain = PDPAChain(api_key).get_chain()

# Reset chat jika bahasa diganti agar pesan pertama berubah
if "current_lang" not in st.session_state or st.session_state.current_lang != lang_code:
    st.session_state.current_lang = lang_code
    st.session_state.messages = [{"role": "assistant", "content": t["welcome"]}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Input Logic
if prompt := st.chat_input(t["input_placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner(t["searching"]):
            try:
                # Tambahkan instruksi bahasa ke prompt agar LLM merespon sesuai pilihan
                language_instruction = " Please answer in Indonesian." if lang_code == "ID" else " Please answer in English."
                response = st.session_state.pdpa_chain.invoke({"query": prompt + language_instruction})
                
                answer = response["result"]
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {str(e)}")