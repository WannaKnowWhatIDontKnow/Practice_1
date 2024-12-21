### Frontend (React.js)
// frontend/src/App.js
import React, { useState, useEffect } from 'react';

function App() {
  const [verbs, setVerbs] = useState([]);
  const [selectedVerb, setSelectedVerb] = useState(null);
  const [examples, setExamples] = useState([]);
  const [currentExample, setCurrentExample] = useState(null);
  const [userInput, setUserInput] = useState('');
  const [feedback, setFeedback] = useState('');

  useEffect(() => {
    fetch('/verbs')
      .then((res) => res.json())
      .then((data) => setVerbs(data));
  }, []);

  const fetchExamples = (verb) => {
    fetch(`/examples/${verb}`)
      .then((res) => res.json())
      .then((data) => {
        setExamples(data);
        setCurrentExample(data[0]); // Set the first example
      });
  };

  const handleCheckSentence = () => {
    fetch('/check_sentence', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_input: userInput,
        correct_sentence: currentExample.english,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setFeedback(data.is_correct ? 'Correct!' : 'Try again.');
      });
  };

  return (
    <div>
      <h1>English Learning App</h1>
      <h2>Select a verb</h2>
      <ul>
        {verbs.map((verb) => (
          <li key={verb} onClick={() => fetchExamples(verb)}>
            {verb}
          </li>
        ))}
      </ul>

      {selectedVerb && (
        <div>
          <h3>Examples for: {selectedVerb}</h3>
          {currentExample && (
            <div>
              <p>{currentExample.english}</p>
              <p>{currentExample.korean}</p>
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
              />
              <button onClick={handleCheckSentence}>Submit</button>
              <p>{feedback}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
