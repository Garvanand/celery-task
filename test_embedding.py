from app.services.embedding_service import EmbeddingService

def test_embedding():
    embedding_service = EmbeddingService()
    
    # Test text
    text = "This is a test document. It contains multiple sentences. We want to see how the embedding service works."
    
    # Generate embedding
    embedding = embedding_service.generate_embeddings([text])
    print("\nEmbedding (first 5 dimensions):")
    print(embedding[0][:5])

if __name__ == "__main__":
    test_embedding() 