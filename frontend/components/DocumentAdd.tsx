import React, { useState } from "react";

interface Props {
  onSubmit: (text: string) => void;
}

const DocumentAdd: React.FC<Props> = ({ onSubmit }) => {
  const [text, setText] = useState<string>("");

  const handleChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(event.target.value);
  };

  const handleSubmit = () => {
    onSubmit(text);
    setText("");
  };

  return (
    <div className="document-add">
      <textarea
        className="document-add-input"
        value={text}
        onChange={handleChange}
        placeholder="Paste your text here..."
      />
      <br />
      <div className="document-add-footer">
        <button className="document-add-submit" onClick={handleSubmit}>
          Submit
        </button>
      </div>
    </div>
  );
};

export default DocumentAdd;
