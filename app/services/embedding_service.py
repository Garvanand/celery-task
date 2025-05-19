import numpy as np
import torch
from typing import List
from transformers import AutoTokenizer, AutoModel

class EmbeddingService:
    def __init__(self):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        # Tokenize texts
        encoded_input = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
        
        # Generate embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
            
        # Mean pooling
        token_embeddings = model_output[0]
        attention_mask = encoded_input['attention_mask']
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
        return embeddings.numpy()
        
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        embeddings = self.generate_embeddings([text])
        return embeddings[0].tolist() 