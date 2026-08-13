from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
from pymongo import MongoClient
import torch

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client["doc_assistant"]
collection = db["documents"]

model = SentenceTransformer('all-MiniLM-L6-v2')


@app.route('/')
def home():
    return "<h1>hey</h1>"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')

    # Get all documents
    docs = list(collection.find())
    if not docs:
        return jsonify({"error": "No documents found."})

    # Combine content for embedding
    contents = [doc.get("content", "") for doc in docs]
    doc_embeddings = model.encode(contents, convert_to_tensor=True)
    query_embedding = model.encode(question, convert_to_tensor=True)

    # Similarity check
    cos_scores = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]
    top_idx = torch.argmax(cos_scores).item()

    best_doc = docs[top_idx]
    response = {
        "matched_title": best_doc.get("title"),
        "matched_content": best_doc.get("content"),
        "similarity_score": float(cos_scores[top_idx])
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
