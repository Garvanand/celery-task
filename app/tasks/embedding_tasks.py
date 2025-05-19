from ..core.celery_app import celery_app
from ..services.file_processor import FileProcessor
from ..services.embedding_service import EmbeddingService
from typing import Dict, List, Any
import tempfile
import os

@celery_app.task(name="process_file_and_generate_embeddings")
def process_file_and_generate_embeddings(file_content: bytes, filename: str) -> Dict[str, Any]:
    """Process file and generate embeddings"""
    try:
        file_processor = FileProcessor()
        embedding_service = EmbeddingService()        
        mime_type = file_processor.validate_file_type(file_content)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file.flush()
            with open(temp_file.name, 'rb') as f:
                text = file_processor.process_file(f, mime_type)
        
        os.unlink(temp_file.name)        
        chunks = file_processor.chunk_text(text)
        embeddings = embedding_service.generate_embeddings(chunks)
        
        return {
            "status": "success",
            "filename": filename,
            "chunks": chunks,
            "embeddings": embeddings,
            "num_chunks": len(chunks)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "filename": filename,
            "error": str(e)
        } 