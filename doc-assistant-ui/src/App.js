import React, { useState } from "react";
import axios from "axios";
import DocsPage from "./DocsPage";
import "./App.css";

function Chatbot({ isOpen, setIsOpen, pendingQuestion, onPendingHandled }) {
  const [userInput, setUserInput] = useState("");
  const [chatHistory, setChatHistory] = useState([
    {
      message:
        "Hi! I'm the Doc Assistant. Ask me anything about setting up your " +
        "account, billing, security, API keys, team invites, or exporting data.",
      sender: "bot",
    },
  ]);

  const sendQuestion = async (question) => {
    const newHistory = [...chatHistory, { message: question, sender: "user" }];
    setChatHistory(newHistory);
    setUserInput("");

    try {
      const response = await axios.post("http://localhost:5000/ask", {
        question,
      });

      const matches = response.data.matches || [];

      if (response.data.reply) {
        setChatHistory([
          ...newHistory,
          { message: response.data.reply, sender: "bot" },
        ]);
      } else if (matches.length === 0) {
        setChatHistory([
          ...newHistory,
          { message: "No relevant answer found.", sender: "bot" },
        ]);
      } else {
        setChatHistory([...newHistory, { message: matches[0], sender: "bot" }]);
      }
    } catch (error) {
      console.error("Error fetching data from API:", error);
      setChatHistory([
        ...newHistory,
        { message: "Sorry, something went wrong!", sender: "bot" },
      ]);
    }
  };

  const handleSendMessage = () => {
    if (userInput.trim()) {
      sendQuestion(userInput);
    }
  };

  React.useEffect(() => {
    if (pendingQuestion) {
      sendQuestion(pendingQuestion);
      onPendingHandled();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pendingQuestion]);

  return (
    <div className="widget-root">
      {isOpen && (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <span>Doc Assistant</span>
            <button className="close-btn" onClick={() => setIsOpen(false)}>
              ✕
            </button>
          </div>

          <div className="chatbox">
            {chatHistory.map((chat, index) => (
              <div
                key={index}
                className={`message ${chat.sender === "bot" ? "bot" : "user"}`}
              >
                {typeof chat.message === "string" ? (
                  chat.message
                ) : (
                  <div className="answer">
                    <h3>{chat.message.title}</h3>
                    <p>{chat.message.content}</p>
                    {chat.message.author && (
                      <span className="answer-source">
                        {chat.message.author}
                      </span>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="input-row">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
              placeholder="Ask me something..."
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        </div>
      )}

      <button className="launcher-btn" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? "✕" : "💬"}
      </button>
    </div>
  );
}

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [pendingQuestion, setPendingQuestion] = useState(null);

  const handleAskAbout = (articleTitle) => {
    setIsOpen(true);
    setPendingQuestion(`Tell me about: ${articleTitle}`);
  };

  return (
    <>
      <DocsPage onAskAbout={handleAskAbout} />
      <Chatbot
        isOpen={isOpen}
        setIsOpen={setIsOpen}
        pendingQuestion={pendingQuestion}
        onPendingHandled={() => setPendingQuestion(null)}
      />
    </>
  );
}

export default App;
