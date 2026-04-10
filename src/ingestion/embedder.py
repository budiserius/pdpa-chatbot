# src/ingestion/embedder.py
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class PDPAEmbedder:
    def __init__(self, vector_dir="vector_db"):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_dir = vector_dir
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

    def process_local_directory(self, data_dir="data"):
        loader = DirectoryLoader(data_dir, glob="./*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        
        vectorstore = Chroma.from_documents(
            documents=chunks, 
            embedding=self.embeddings, 
            persist_directory=self.vector_dir
        )
        return vectorstore