import React from 'react';

const TextOutput = ({ text }) => {
  const renderText = () => {
    if (typeof text === 'object') {
      return <pre>{JSON.stringify(text, null, 2)}</pre>; // Safely render object
    }
    return text; // Render plain string
  };

  return (
    <div className="alert alert-primary mt-4" role="alert">
      <strong>Answer:</strong> {renderText()}
    </div>
  );
};

export default TextOutput;
