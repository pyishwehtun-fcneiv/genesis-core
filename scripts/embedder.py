"""
GENESIS Embedding Module — runs natively inside GitHub Actions runner.
Replaces HF Space sentence-transformers endpoint.
"""
import sys
import json
from sentence_transformers import SentenceTransformer


def generate_embedding(text: str) -> dict:
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        vector = model.encode(text).tolist()
        return {"embedding": vector, "dimensions": len(vector), "status": "success"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}


if __name__ == "__main__":
    input_text = sys.argv[1] if len(sys.argv) > 1 else "test sentence"
    result = generate_embedding(input_text)
    print(json.dumps({"dimensions": result.get("dimensions"), "status": result.get("status")}, indent=2))
