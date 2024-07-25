import { BASE_URL } from "@/config/constants";
import React, { useState, useEffect, useRef } from "react";
import { trackPromise } from "react-promise-tracker";
import BouncingDots from "./BouncingDots";
import ErrorPopup from "./ErrorPopup";
import MarkdownMessage from "./MarkdownMessage";

export interface Message {
  persona: string;
  message: string;
}

const ChatWindow = () => {
  const [userInput, setUserInput] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [backendError, setBackendError] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const chatWindowRef = useRef<HTMLDivElement>(null);

  const handleUserInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setUserInput(event.target.value);
  };

  const handleSendMessage = () => {
    if (userInput) {
      // Add user's message to state
      setMessages([...messages, { persona: "user", message: userInput }]);
      setUserInput("");
      // Set loading state to true
      setLoading(true);
      // generate responses
      generateSystemResponse(userInput);
    }
  };

  const generateSystemResponse = (userInput: string) => {
    const streamRequest = async (userInput: string) => {
      const response = await fetch(BASE_URL + "/getKnowledge", {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          q: userInput,
        }),
      });

      if (!response.ok) {
        handleErrorOccured();
        throw new Error("Request failed");
      }
      if (response.body == null) return;
      const reader = response.body.getReader();
      let receivedText = "";

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        const textChunk = new TextDecoder("utf-8").decode(value);
        receivedText += textChunk;
        setMessages((prevMessages) => [
          ...prevMessages.slice(0, -1),
          { ...prevMessages[prevMessages.length - 1], message: receivedText },
        ]);
      }
      // Set loading state to false after the response is received
      setLoading(false);
    };

    trackPromise(streamRequest(userInput)).catch((error) => {
      console.error("Error:", error);
      setLoading(false);
    });

    // Add placeholder for system message
    setMessages((prevMessages) => [
      ...prevMessages,
      { persona: "system", message: "" },
    ]);
  };

  const handleErrorOccured = () => {
    setBackendError(true);
  };

  const handleErrorIgnore = () => {
    setBackendError(false);
  };
  const handleErrorReset = () => {
    setBackendError(false);
    reset();
  };

  function reset() {
    setMessages([]);
    setUserInput("");
  }

  return (
    <div className="chat-container">
      <div className="reset-button-container">
        <button
          className="reset-button message system-message"
          onClick={reset}
        >
          Reset Q&A
        </button>
      </div>
      <div className="chat-window" ref={chatWindowRef}>
        <div className="chat-content">
          <div className="message-list">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.persona}-message`}>
                {msg.message === "" && loading ? (
                  <BouncingDots />
                ) : (
                  <MarkdownMessage message={msg.message} />
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="input-container">
        <textarea
          className="message-input"
          placeholder="Ask your question here..."
          value={userInput}
          onChange={handleUserInput}
          onKeyDown={(event) => {
            if (event.keyCode === 13 && !event.shiftKey) {
              event.preventDefault();
              handleSendMessage();
            }
          }}
          disabled={loading}
        />
        <button className="send-button" onClick={handleSendMessage}>
          Send
        </button>
      </div>
      <ErrorPopup
        error={backendError}
        onIgnore={handleErrorIgnore}
        onReset={handleErrorReset}
      />
    </div>
  );
};

export default ChatWindow;
