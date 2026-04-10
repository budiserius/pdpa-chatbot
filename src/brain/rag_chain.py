# src/brain/rag_chain.py
import os
os.environ['CHROMA_TELEMETRY_OFF'] = 'True'

from langchain_groq import ChatGroq
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
        
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile" 
        )
        

    def get_chain(self):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3})
        )