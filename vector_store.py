# vector_store.py
from sentence_transformers import SentenceTransformer, util
from pymongo import MongoClient
import re

model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

client = MongoClient("mongodb://localhost:27017/")
collection = client["doc_assistant"]["documents"]

SIMILARITY_THRESHOLD = 0.35


def preprocess_document(doc):
    text = f"{doc.get('title', '')}. {doc.get('description', '')}. {doc.get('content', '')}"
    text = re.sub(r'#*', '', text).replace("\n", " ").strip()
    sentences = [sent.strip() for sent in text.split('.') if sent.strip()]
    return sentences


def load_and_embed_documents():
    chunks = []
    docs = list(collection.find())

    for doc in docs:
        sentences = preprocess_document(doc)
        for sentence in sentences:
            embedding = model.encode(sentence, convert_to_tensor=True)
            chunks.append({
                "sentence": sentence,
                "embedding": embedding,
                "source_title": doc.get("title", "Untitled"),
                "full_content": doc.get("content", ""),
                "author": doc.get("author", "Unknown"),
                "tags": doc.get("tags", [])
            })
    return chunks


document_chunks = load_and_embed_documents()


def search_similar_sentences(query, top_k=3):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scored = []

    for chunk in document_chunks:
        score = util.cos_sim(query_embedding, chunk["embedding"]).item()
        scored.append((score, chunk))

    scored.sort(reverse=True, key=lambda x: x[0])

    
    seen_titles = set()
    top_results = []
    for score, chunk in scored:
        if score < SIMILARITY_THRESHOLD:
            break
        if chunk["source_title"] in seen_titles:
            continue
        seen_titles.add(chunk["source_title"])
        top_results.append((score, chunk))
        if len(top_results) >= top_k:
            break

    return [{
        "score": round(score, 4),
        
        "answer": chunk["full_content"],
        "source_title": chunk["source_title"],
        "author": chunk["author"],
        "tags": chunk["tags"]
    } for score, chunk in top_results]