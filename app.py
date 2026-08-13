
from flask import Flask, request, jsonify
from flask_cors import CORS
from vector_store import search_similar_sentences

app = Flask(__name__)
CORS(app)


GREETINGS = {"hi", "hii", "hey", "hello", "yo", "sup", "wassup", "wth", "what"}


def is_small_talk(text):
    cleaned = text.strip().lower().rstrip("?!. ")
    return cleaned in GREETINGS or len(cleaned) <= 2


@app.route("/")
def home():
    return "Doc Assistant AI is running!"


@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided."}), 400

    if is_small_talk(question):
        return jsonify({
            "reply": "Hey! I'm the Doc Assistant — ask me something about "
                      "account setup, billing, security, API keys, team "
                      "invites, or data exports and I'll pull up the answer.",
            "matches": []
        })

    results = search_similar_sentences(question)

    if not results:
        return jsonify({
            "reply": "I couldn't find anything relevant to that in the docs. "
                      "Try asking about account setup, billing, 2FA, API keys, "
                      "team invites, or data exports.",
            "matches": []
        })

    response = []
    for doc in results:
        response.append({
            "title": doc.get("source_title", "Untitled"),
            "content": doc.get("answer", ""),
            "score": doc.get("score", 0),
            "tags": doc.get("tags", []),
            "author": doc.get("author", "Unknown")
        })

    return jsonify({"matches": response})


if __name__ == "__main__":
    app.run(debug=True)