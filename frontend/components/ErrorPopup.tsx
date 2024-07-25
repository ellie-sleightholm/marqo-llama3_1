import React from "react";

interface ErrorPopupProps {
  error: boolean;
  onIgnore: () => void;
  onReset: () => void;
}

const ErrorPopup: React.FC<ErrorPopupProps> = ({
  error,
  onIgnore,
  onReset,
}) => {
  if (!error) {
    return null; // Don't render anything if error is false
  }

  return (
    <div className="error-popup">
      <div className="error-popup-content">
        <h2>Error!</h2>
        <p>A backend error occurred. Please try again later.</p>
        <div className="error-popup-buttons">
          <button onClick={onIgnore}>Ignore</button>
          <button onClick={onReset}>Reset</button>
        </div>
      </div>
    </div>
  );
};

export default ErrorPopup;
