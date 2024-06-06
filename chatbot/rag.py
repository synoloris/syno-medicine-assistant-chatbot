import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

class MedicineRAG:
    def __init__(self):
        # Load the model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load the embeddings and dataset
        self.corpus_embeddings = torch.load('model/corpus_embeddings.pt')
        self.medicaments = pd.read_csv('model/embedded_dataset.csv')

    def retrieve(self, query):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, self.corpus_embeddings, top_k=3)[0]

        results = []
        for hit in hits:
            row = self.medicaments.iloc[hit['corpus_id']]
            results.append({
                "score": hit['score'],
                "text": row['text']
            })
        return results
