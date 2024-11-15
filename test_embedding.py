from sentence_transformers import SentenceTransformer

model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
def get_embedding(data):
   """Generates vector embeddings for the given data."""
   embedding = model.encode(data)
   return embedding.tolist()

data = [
   "Titanic: The story of the 1912 sinking of the largest luxury liner ever built",
   "The Lion King: Lion cub and future king Simba searches for his identity",
   "Avatar: A marine is dispatched to the moon Pandora on a unique mission"
]

# Ingest data into Atlas
inserted_doc_count = 0
for text in data:
   embedding = get_embedding(text)
   log_db.insert_log("test", {"text": text, "embedding": embedding}, many=False)
   inserted_doc_count = 0
print(f"Inserted {inserted_doc_count} documents into the 'test' collection.")