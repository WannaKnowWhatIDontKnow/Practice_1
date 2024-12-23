import React, { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const [verbs, setVerbs] = useState([]); // 동사 목록
  const [selectedVerb, setSelectedVerb] = useState(null); // 선택된 동사
  const [examples, setExamples] = useState([]); // 예문 목록
  const [currentExampleIndex, setCurrentExampleIndex] = useState(0); // 현재 예문 인덱스
  const [userInput, setUserInput] = useState(''); // 사용자 입력
  const [feedback, setFeedback] = useState(''); // 피드백 메시지
  const [completed, setCompleted] = useState(false); // 완료 여부

  const appRef = useRef(null); // 키보드 이벤트를 감지할 요소 참조

  // ✅ 동사 목록 가져오기
  useEffect(() => {
    fetch("http://localhost:8000/verbs")
      .then((res) => res.json())
      .then((data) => setVerbs(data))
      .catch((error) => console.error("Error fetching verbs:", error));
  }, []);

  // ✅ 특정 동사의 예문 가져오기
  const fetchExamples = (verb) => {
    fetch(`http://localhost:8000/examples/${verb}`)
      .then((res) => res.json())
      .then((data) => {
        setSelectedVerb(verb);
        setExamples(data);
        setCurrentExampleIndex(0);
        setUserInput('');
        setFeedback('');
        setCompleted(false);
      })
      .catch((error) => console.error("Error fetching examples:", error));
  };

  // ✅ 문장 확인
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
          setFeedback("정답입니다!");
          if (currentExampleIndex + 1 < examples.length) {
            setTimeout(() => {
              setCurrentExampleIndex(currentExampleIndex + 1);
              setUserInput('');
              setFeedback('');
            }, 1000);
          } else {
            setCompleted(true);
            setFeedback("모든 예문이 완료되었습니다!");
          }
        } else {
          setFeedback("틀렸습니다. 다시 시도해주세요.");
        }
      })
      .catch((error) => console.error("Error checking sentence:", error));
  };

  // ✅ Enter 키로 동작 구분
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // 기본 Enter 동작 방지

      if (completed) {
        // ✅ 완료 페이지에서는 홈으로 돌아가기
        setSelectedVerb(null);
        setCompleted(false);
      } else {
        // ✅ 예문 제출
        handleCheckSentence();
      }
    }
  };

  // ✅ 페이지가 로드될 때 포커스를 강제 설정
  useEffect(() => {
    if (appRef.current) {
      appRef.current.focus();
    }
  }, [completed]); // completed 상태가 변경될 때마다 포커스 설정

  // ✅ 입력값 업데이트
  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  return (
    <div
      ref={appRef}
      className="app-container"
      onKeyDown={handleKeyDown}
      tabIndex={0} // 포커스를 받을 수 있도록 설정
    >
      <header className="header">English Learning App</header>

      {!selectedVerb ? (
        <div className="main-page">
          <h2>원하는 동사 선택</h2>
          <div className="verbs-container">
            {verbs.map((verb) => (
              <button
                key={verb.id}
                onClick={() => fetchExamples(verb.verb)}
                className="verb-button"
              >
                {verb.verb}
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
                  onKeyDown={handleKeyDown} // ✅ Enter 키 이벤트 추가
                  className="typing-field"
                  placeholder="여기에 입력하세요..."
                />
                <button onClick={handleCheckSentence} className="action-button">
                  제출
                </button>
              </div>
              <p className="feedback">{feedback}</p>
            </>
          ) : (
            <>
              <h3>모든 예문이 완료되었습니다!</h3>
              <button
                onClick={() => {
                  setSelectedVerb(null);
                  setCompleted(false);
                }}
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
