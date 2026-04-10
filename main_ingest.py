from src.ingestion.embedder import PDPAEmbedder

if __name__ == "__main__":
    print("Memulai proses embedding dokumen lokal...")
    embedder = PDPAEmbedder()
    embedder.process_local_directory()
    print("Proses selesai. Database vektor telah diperbarui di folder 'vector_db/'")