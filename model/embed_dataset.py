import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
import os

# Load the dataset
dataset_path = 'dataset/Medicine_Details.csv'
df = pd.read_csv(dataset_path)

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Combine relevant columns to create the text to be embedded
df['text'] = df.apply(lambda row: f"Medicine Name: {row['Medicine Name']}, Composition: {row['Composition']}, Uses: {row['Uses']}, Side Effects: {row['Side_effects']}", axis=1)

# Generate embeddings for the dataset
corpus_embeddings = model.encode(df['text'], convert_to_tensor=True)

# Create model directory if it doesn't exist
model_dir = 'model'
os.makedirs(model_dir, exist_ok=True)

# Save embeddings and corresponding text in the model directory
torch.save(corpus_embeddings, os.path.join(model_dir, 'corpus_embeddings.pt'))
df.to_csv(os.path.join(model_dir, 'embedded_dataset.csv'), index=False)
