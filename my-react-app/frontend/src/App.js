
import React, { useState, useEffect } from "react";
import "./App.css";

const quotes = [
  "마음이 고요하면 모든 것이 명확해진다.",
  "현재에 집중하라. 그것이 최고의 순간이다.",
  "작은 일에도 마음을 다하면 큰 결과를 얻는다.",
  "천천히, 그러나 꾸준히 나아가라.",
  "깨어있는 마음이 더 나은 선택을 만든다."
];

function App() {
  const [verbs, setVerbs] = useState([]);
  const [selectedVerb, setSelectedVerb] = useState(null);
  const [examples, setExamples] = useState([]);
  const [currentExampleIndex, setCurrentExampleIndex] = useState(0);
  const [repeatCount, setRepeatCount] = useState(1);
  const [currentRepeat, setCurrentRepeat] = useState(0);
  const [userInput, setUserInput] = useState("");
  const [feedback, setFeedback] = useState("");
  const [completed, setCompleted] = useState(false);
  const [currentQuote, setCurrentQuote] = useState("");

  //To fetch the verb list
  useEffect(() => {
    fetch("http://localhost:8000/verbs")
      .then((res) => res.json())
      .then((data) => setVerbs(data));
  }, []);

  //To fetch the examples for the verbs
  const fetchExamples = (verb) => {
    fetch(`http://localhost:8000/examples/${verb}`)
      .then((res) => res.json())
      .then((data) => {
        setSelectedVerb(verb);
        setExamples(data);
        setCurrentExampleIndex(0);
        setCurrentRepeat(0);
        setUserInput("");
        setFeedback("");
        setCompleted(false);
        setCurrentQuote(quotes[Math.floor(Math.random() * quotes.length)]);
      });
  };

  //To check if the answer is right
  const handleCheckSentence = () => {
    const currentExample = examples[currentExampleIndex];
    fetch("http://localhost:8000/check_sentence", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_input: userInput,
        correct_sentence: currentExample.english,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.is_correct) {
          if (currentRepeat + 1 < repeatCount) {
            setCurrentRepeat(currentRepeat + 1);
            setUserInput("");
            setFeedback("정답입니다! 반복해주세요.");
          } else if (currentExampleIndex + 1 < examples.length) {
            setCurrentExampleIndex(currentExampleIndex + 1);
            setCurrentRepeat(0);
            setUserInput("");
            setFeedback("정답입니다! 다음 예문으로 넘어갑니다.");
            setCurrentQuote(quotes[Math.floor(Math.random() * quotes.length)]);
          } else {
            setCompleted(true);
            setFeedback("");
          }
        } else {
          setFeedback("틀렸습니다. 다시 시도해주세요.");
        }
      });
  };

  // 📚 입력 필드 업데이트
  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  // 📚 Enter 키로 이벤트 처리
  useEffect(() => {
    const handleGlobalKeyDown = (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        if (completed) {
          setSelectedVerb(null); // 홈으로 돌아가기
        } else {
          handleCheckSentence(); // 문장 확인
        }
      }
    };

    window.addEventListener("keydown", handleGlobalKeyDown);

    return () => {
      window.removeEventListener("keydown", handleGlobalKeyDown);
    };
  }, [completed, handleCheckSentence]);

  return (
    <div className="app-container">
      <header className="header">English Learning App</header>

      {!selectedVerb ? (
        <div className="main-page">
          <h2>원하는 동사 선택</h2>
          <div className="verbs-container">
            {verbs.map((verb) => (
              <button
                key={verb}
                onClick={() => fetchExamples(verb)}
                className="verb-button"
              >
                {verb}
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="practice-page">
          {!completed ? (
            <>
              <h3>Examples for: {selectedVerb}</h3>
              <p>
                {examples[currentExampleIndex]?.english} (
                {examples[currentExampleIndex]?.korean})
              </p>
              <div className="input-container">
                <textarea
                  value={userInput}
                  onChange={handleInputChange}
                  className="typing-field"
                  placeholder="여기에 입력하세요..."
                />
                <button onClick={handleCheckSentence} className="action-button">
                  제출
                </button>
              </div>
              <div className="quote">{currentQuote}</div>
              <p>{feedback}</p>
            </>
          ) : (
            <>
              <h3>모든 예문이 완료되었습니다!</h3>
              <button
                onClick={() => setSelectedVerb(null)}
                className="action-button"
              >
                홈으로 돌아가기
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}


export default App;
