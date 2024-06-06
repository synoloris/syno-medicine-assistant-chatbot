import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
import os

print("Starting the embedding process...")

# Load the dataset
dataset_path = 'dataset/Medicine_Details.csv'
print(f"Loading dataset from {dataset_path}...")
df = pd.read_csv(dataset_path)
print(f"Dataset loaded with {len(df)} entries.")

# Initialize the model
print("Initializing the Sentence Transformer model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model initialized.")

# Combine relevant columns to create the text to be embedded
print("Combining relevant columns into a single text column for embedding...")
df['text'] = df.apply(lambda row: f"Medicine Name: {row['Medicine Name']}, Composition: {row['Composition']}, Uses: {row['Uses']}, Side Effects: {row['Side_effects']}", axis=1)
print("Text column created.")

# Generate embeddings for the dataset
print("Generating embeddings for the dataset...")
corpus_embeddings = model.encode(df['text'], convert_to_tensor=True)
print("Embeddings generated.")

# Create model directory if it doesn't exist
model_dir = 'model'
print(f"Checking if model directory {model_dir} exists...")
os.makedirs(model_dir, exist_ok=True)
print(f"Model directory {model_dir} is ready.")

# Save embeddings and corresponding text in the model directory
embeddings_path = os.path.join(model_dir, 'corpus_embeddings.pt')
csv_path = os.path.join(model_dir, 'embedded_dataset.csv')
print(f"Saving embeddings to {embeddings_path}...")
torch.save(corpus_embeddings, embeddings_path)
print("Embeddings saved.")
print(f"Saving embedded dataset to {csv_path}...")
df.to_csv(csv_path, index=False)
print("Embedded dataset saved.")

print("Embedding process completed.")