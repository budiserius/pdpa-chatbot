# src/brain/rag_chain.py
import os
os.environ['CHROMA_TELEMETRY_OFF'] = 'True'

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings

class PDPAChain:
    def __init__(self, api_key, vector_dir="vector_db"):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.vectorstore = Chroma(
            persist_directory=vector_dir, 
            embedding_function=embeddings
        )
        
        # Gunakan nama model yang valid untuk API (gemini-1.5-flash)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=api_key,
            temperature=0
        )

    def get_chain(self):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
        )