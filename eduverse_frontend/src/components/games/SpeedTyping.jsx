import { useState, useEffect } from "react";

const SpeedTyping = ({ onComplete }) => {
  const [currentSnippet, setCurrentSnippet] = useState(0);
  const [userInput, setUserInput] = useState("");
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(60);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameEnded, setGameEnded] = useState(false);
  const [wpm, setWpm] = useState(0);

  const codeSnippets = [
    "const greeting = 'Hello World';",
    "function add(a, b) { return a + b; }",
    "const arr = [1, 2, 3].map(x => x * 2);",
    "if (condition) { console.log('true'); }",
    "for (let i = 0; i < 10; i++) { }",
  ];

  useEffect(() => {
    if (gameStarted && !gameEnded && timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0 && !gameEnded) {
      endGame();
    }
  }, [timeLeft, gameStarted, gameEnded]);

  const startGame = () => {
    setGameStarted(true);
  };

  const handleInputChange = (e) => {
    const input = e.target.value;
    setUserInput(input);

    if (input === codeSnippets[currentSnippet]) {
      const points = codeSnippets[currentSnippet].length * 10;
      setScore(score + points);
      setUserInput("");
      
      if (currentSnippet < codeSnippets.length - 1) {
        setCurrentSnippet(currentSnippet + 1);
      } else {
        setCurrentSnippet(0);
      }
      
      // Calculate WPM
      const wordsTyped = (score + points) / 50;
      const minutesElapsed = (60 - timeLeft) / 60;
      setWpm(Math.round(wordsTyped / minutesElapsed));
    }
  };

  const endGame = () => {
    setGameEnded(true);
    onComplete(score);
  };

  if (!gameStarted) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">⚡</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Speed Typing
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Type code snippets as fast as you can!
        </p>
        <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 mb-6">
          <h3 className="font-bold text-gray-800 dark:text-white mb-2">How to Play:</h3>
          <ul className="text-left text-gray-600 dark:text-gray-300 space-y-1">
            <li>• Type the code exactly as shown</li>
            <li>• Points based on snippet length</li>
            <li>• Time limit: 60 seconds</li>
            <li>• Type fast and accurately!</li>
          </ul>
        </div>
        <button
          onClick={startGame}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all"
        >
          Start Typing
        </button>
      </div>
    );
  }

  if (gameEnded) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Time's Up!
        </h2>
        <div className="text-5xl font-bold text-blue-600 dark:text-blue-400 mb-6">
          {score} points
        </div>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          WPM: {wpm}
        </p>
        <button
          onClick={() => window.location.reload()}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all"
        >
          Play Again
        </button>
      </div>
    );
  }

  const snippet = codeSnippets[currentSnippet];
  const isCorrect = snippet.startsWith(userInput);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white">Speed Typing</h2>
        <div className="text-right">
          <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
            {timeLeft}s
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Score: {score}
          </div>
        </div>
      </div>

      <div className="bg-gray-900 rounded-lg p-6 mb-4">
        <p className="text-green-400 font-mono text-xl mb-4">{snippet}</p>
      </div>

      <input
        type="text"
        value={userInput}
        onChange={handleInputChange}
        className={`w-full p-4 font-mono text-lg rounded-lg border-2 ${
          isCorrect
            ? "border-green-500 bg-green-50 dark:bg-green-900"
            : userInput.length > 0
            ? "border-red-500 bg-red-50 dark:bg-red-900"
            : "border-gray-300 dark:border-gray-600"
        } focus:outline-none`}
        placeholder="Start typing..."
        autoFocus
      />

      <div className="mt-4 text-center text-gray-600 dark:text-gray-400">
        WPM: {wpm} | Accuracy: {userInput.length > 0 ? Math.round((userInput.split('').filter((c, i) => c === snippet[i]).length / userInput.length) * 100) : 100}%
      </div>
    </div>
  );
};

export default SpeedTyping;