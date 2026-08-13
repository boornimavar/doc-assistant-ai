from datasets import Dataset
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

documents = [
    "How to reset password?",
    "What is Retrieval-Augmented Generation (RAG)?",
    "How does FAISS work for document retrieval?",
    "What is the best model for QA tasks?"
]

model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = model.encode(documents)

embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)  
index.add(np.array(embeddings)) 

faiss.write_index(index, "document_index.index")

dataset = Dataset.from_dict({"documents": documents, "embeddings": embeddings.tolist()})

dataset.save_to_disk("my_dataset")
