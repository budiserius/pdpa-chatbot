# PDPA Chatbot

Personal Data Protection Act Chatbot

## Latar Belakang

Kesadaran akan perlindungan data pribadi masyarakat indonesia masih tinggi. Banyak orang belum mengetahui batasan batasan ataupun regulasi yang ada terkait hal ini. Hal tersebut menyebabkan beberapa pelanggaran penggunaan data pribadi yang cukup serius. Dengan adanya bot ini, diharapkan dapat memfasilitasi orang orang yang curious dan dapat meningkatkan awareness terkait perlindungan data pribadi.

## Folder Structure

```plaintext
pdpa-chatbot/
├── .env                    # Variabel sensitif (API Keys, Client Secrets)
├── .gitignore              # Mengecualikan venv/, .env, dan __pycache__/
├── requirements.txt        # Daftar dependensi library
├── README.md               # Dokumentasi proyek dan cara install
├── data/                   # STAGING AREA: Folder lokal untuk simpan PDF hasil download
│   └── raw/                # Dokumen asli dari Microsoft Graph/Lokal
├── vector_db/              # Database vektor yang sudah dipersistenkan (misal: ChromaDB)
├── notebooks/              # Untuk riset dan eksperimen (Jupyter Notebooks)
├── src/                    # KODE SUMBER UTAMA
│   ├── __init__.py
│   ├── ingestion/          # PIPELINE: Dari Dokumen ke Vektor
│   │   ├── __init__.py
│   │   ├── graph_client.py # Logika khusus Microsoft Graph API
│   │   └── embedder.py     # Logika Text Splitting & Embedding
│   ├── brain/              # LOGIKA AI & ORCHESTRATOR
│   │   ├── __init__.py
│   │   └── rag_chain.py    # Konfigurasi LangChain (QA Chain)
│   └── web/                # USER INTERFACE
│       ├── __init__.py
│       └── app.py          # Entry point utama Streamlit
└── tests/                  # Unit testing (opsional namun profesional)
```
