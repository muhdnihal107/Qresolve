from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # Small, fast, and good

def get_embedding(text: str) -> list:
    return model.encode(text).tolist()
