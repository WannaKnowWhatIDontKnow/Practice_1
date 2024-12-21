import React, { useState } from "react";
import "./PracticePage.css"; // CSS 스타일링 파일

function PracticePage() {
  const [userInput, setUserInput] = useState("");

  // 입력값을 상태로 업데이트
  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  return (
    <div className="practice-container">
      <h3>Typing Animation Example</h3>
      {/* 사용자가 입력한 글자들을 하나씩 렌더링 */}
      <div className="typing-display">
        {userInput.split("").map((char, index) => (
          <span key={index} className="animated-char">
            {char}
          </span>
        ))}
        <span className="cursor">|</span>
      </div>
      {/* 입력 필드 */}
      <input
        type="text"
        value={userInput}
        onChange={handleInputChange}
        placeholder="Start typing..."
        className="input-field"
      />
    </div>
  );
}

export default PracticePage;
