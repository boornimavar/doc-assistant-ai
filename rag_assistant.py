from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration
from datasets import load_from_disk
import faiss
import torch

dataset = load_from_disk("my_dataset")

index = faiss.read_index("document_index.index")

tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
model_rag = RagSequenceForGeneration.from_pretrained("facebook/rag-token-nq")

retriever = RagRetriever.from_pretrained(
    "facebook/rag-token-nq", 
    index_name="custom", 
    passages_path="my_dataset",
    index=index
)

def rag_assistant(query):
    inputs = tokenizer(query, return_tensors="pt")
    question_embeds = model_rag.encode_question(inputs['input_ids'])
    top_docs = retriever.get_top_docs(question_embeds, top_k=3)
    context_input = tokenizer.prepare_seq2seq_batch(src_texts=[query] + top_docs, return_tensors="pt")
    generated_ids = model_rag.generate(input_ids=context_input["input_ids"], num_beams=4, max_length=200)
    answer = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    return answer

query = "How can I reset my password?"
answer = rag_assistant(query)

print(f"Query: {query}")
print(f"Answer: {answer}")
