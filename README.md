# AI Documentation Assistant

A chatbot that answers product-documentation questions using semantic search instead of keyword matching. Ask a question in plain English ("how do I turn on two-factor auth?") and it finds the most relevant doc and gives you the actual answer, instead of making you dig through a help center.

Built as a way to explore retrieval-based NLP (RAG-style search, not full generative AI) with a real frontend on top — a docs site with a floating chat widget, similar to the support bots you see on most SaaS products.

## What it does

- Frontend is a small documentation website with a handful of articles (account setup, billing, 2FA, API keys, etc.)
- A chat widget sits in the bottom-right corner, like Intercom/Drift-style support widgets
- Click any article to read it, or click "Ask the assistant about this" to have the chatbot answer questions about it directly
- Behind the scenes, the backend embeds the question and every document using `sentence-transformers`, ranks documents by cosine similarity, and returns the best match — with a relevance threshold so it doesn't confidently return garbage when nothing actually matches
- Basic small-talk handling (greetings, vague input) get a normal reply instead of being run through the search

## How it works

1. Documents live in MongoDB, seeded from `seed_documents.py`
2. On startup, `vector_store.py` loads every document and pre-computes sentence embeddings using the `multi-qa-MiniLM-L6-cos-v1` model
3. When a question comes in, it's embedded the same way and compared against every stored embedding using cosine similarity
4. Matches below a similarity threshold are dropped — if nothing is relevant, the assistant says so instead of returning the closest (but wrong) answer
5. The top match's full document content is returned as the answer, not just a fragment

This is retrieval, not generation — there's no LLM writing new text, it's finding and returning the right existing content. That's a deliberate scope choice to keep the project runnable without needing paid API keys.

## Tech stack

**Backend:** Python, Flask, MongoDB, sentence-transformers, PyTorch
**Frontend:** React (Create React App), Axios

## Project structure

```
ai/
├── app.py                 # Main Flask app (the one that actually runs) — /ask endpoint
├── vector_store.py         # Embedding + similarity search logic
├── seed_documents.py       # Populates MongoDB with sample documentation
├── mongo_utils.py          # Mongo connection helper
├── main.py                 # Earlier draft version, kept for reference
├── rag_assistant.py        # Experiment with HuggingFace's full RAG model — not wired into the live app
├── requirements.txt
└── doc-assistant-ui/
    ├── src/
    │   ├── App.js           # Chat widget + layout
    │   ├── DocsPage.js       # The documentation site itself
    │   └── App.css
    └── package.json
```

## Running it locally

You'll need Python 3.10+, Node.js, and MongoDB running locally (or a connection string swapped into `mongo_utils.py` / `vector_store.py` if you're using Atlas).

**Backend:**
```bash
cd ai
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python seed_documents.py       # loads sample docs into MongoDB
python app.py                  # runs on http://127.0.0.1:5000
```

**Frontend** (separate terminal):
```bash
cd ai/doc-assistant-ui
npm install
npm start                      # runs on http://localhost:3000
```

Open `http://localhost:3000` and the docs site should load with the chat widget in the corner.

## Known limitations

- Documents are seeded sample data, not a real product's docs — swap in real content by editing `seed_documents.py`
- Search only covers 8 topics right now; scaling to a larger doc set would need better chunking than the current sentence-split approach
- No generation step — answers are retrieved verbatim from the source doc, not paraphrased or synthesized
- Not currently deployed anywhere; running locally only for now

## Possible next steps

- Add an actual generation layer (OpenAI/Anthropic API) so answers are synthesized from retrieved context instead of shown verbatim
- Deploy backend to Render/Railway with MongoDB Atlas, frontend to Vercel/Netlify
- Support uploading real documents (PDF/markdown) instead of hardcoded seed data
