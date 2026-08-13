import React, { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);

  const handleAsk = async () => {
    const res = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    setResponse(data);
  };

  return (
    <div className="container">
      <h1>📄 Doc Assistant</h1>

      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something..."
      />

      <button onClick={handleAsk}>Ask</button>

      {response && (
        <div className="response-box">
          <h2>💬 Response:</h2>
          <p>{response.matched_content}</p>
          <p className="source">📚 From: {response.matched_title}</p>
        </div>
      )}
    </div>
  );
}

export default App;
