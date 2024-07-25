import React, { useState } from "react";
import { BASE_URL } from "@/config/constants";

const KnowledgeAdder: React.FC = () => {
  const [text, setText] = useState<string>("");

  async function handleSubmit() {
    console.log(text);
    await fetch(BASE_URL + "/addKnowledge", {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        document: text,
      }),
    });
    setText(""); // Clear the text after submitting
  }

  return (
    <div className="knowledge-adder">
      <textarea
        className="knowledge-input"
        placeholder="Paste your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button className="submit-button" onClick={handleSubmit}>
        Submit
      </button>
    </div>
  );
};

export default KnowledgeAdder;
