from src.ingestion.embedder import PDPAEmbedder

if __name__ == "__main__":
    print("INFO: Start embedding document process...")
    embedder = PDPAEmbedder()
    embedder.process_local_directory()
    print("INFO: Vector database has been update in `vector_db/` folder")