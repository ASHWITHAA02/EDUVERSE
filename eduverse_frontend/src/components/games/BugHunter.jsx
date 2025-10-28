import { useState, useEffect } from "react";

const BugHunter = ({ onComplete }) => {
  const [currentBug, setCurrentBug] = useState(0);
  const [selectedLine, setSelectedLine] = useState(null);
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(240);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameEnded, setGameEnded] = useState(false);
  const [feedback, setFeedback] = useState("");

  const bugs = [
    {
      code: [
        "function calculateTotal(items) {",
        "  let total = 0;",
        "  for (let i = 0; i <= items.length; i++) {",
        "    total += items[i].price;",
        "  }",
        "  return total;",
        "}",
      ],
      bugLine: 2,
      explanation: "Array index out of bounds - should be i < items.length",
    },
    {
      code: [
        "const user = {",
        "  name: 'John',",
        "  age: 25",
        "};",
        "console.log(user.Name);",
      ],
      bugLine: 4,
      explanation: "Property name is case-sensitive - should be user.name",
    },
    {
      code: [
        "function divide(a, b) {",
        "  return a / b;",
        "}",
        "const result = divide(10, 0);",
      ],
      bugLine: 1,
      explanation: "No check for division by zero",
    },
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

  const checkAnswer = () => {
    const bug = bugs[currentBug];
    if (selectedLine === bug.bugLine) {
      setScore(score + 200);
      setFeedback(`✅ Correct! ${bug.explanation}`);
      
      setTimeout(() => {
        if (currentBug < bugs.length - 1) {
          setCurrentBug(currentBug + 1);
          setSelectedLine(null);
          setFeedback("");
        } else {
          endGame();
        }
      }, 2000);
    } else {
      setFeedback("❌ Wrong line! Try again.");
      setTimeout(() => setFeedback(""), 1500);
    }
  };

  const endGame = () => {
    setGameEnded(true);
    onComplete(score);
  };

  if (!gameStarted) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">🐛</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Bug Hunter
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Find and identify bugs in the code!
        </p>
        <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 mb-6">
          <h3 className="font-bold text-gray-800 dark:text-white mb-2">How to Play:</h3>
          <ul className="text-left text-gray-600 dark:text-gray-300 space-y-1">
            <li>• Click on the line with the bug</li>
            <li>• Each bug found: +200 points</li>
            <li>• Time limit: 4 minutes</li>
            <li>• Read the code carefully!</li>
          </ul>
        </div>
        <button
          onClick={startGame}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all"
        >
          Start Hunting
        </button>
      </div>
    );
  }

  if (gameEnded) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Hunt Complete!
        </h2>
        <div className="text-5xl font-bold text-blue-600 dark:text-blue-400 mb-6">
          {score} points
        </div>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Bugs found: {currentBug + 1}/{bugs.length}
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

  const bug = bugs[currentBug];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
            Bug {currentBug + 1}/{bugs.length}
          </h2>
          <p className="text-gray-600 dark:text-gray-400">Click the buggy line</p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
            {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, "0")}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Score: {score}
          </div>
        </div>
      </div>

      <div className="bg-gray-900 rounded-lg p-4 mb-4">
        {bug.code.map((line, index) => (
          <div
            key={index}
            onClick={() => setSelectedLine(index)}
            className={`font-mono text-sm py-2 px-3 cursor-pointer rounded transition-all ${
              selectedLine === index
                ? "bg-yellow-500 text-gray-900"
                : "text-green-400 hover:bg-gray-800"
            }`}
          >
            <span className="text-gray-500 mr-4">{index + 1}</span>
            {line}
          </div>
        ))}
      </div>

      {feedback && (
        <div className={`p-4 rounded-lg mb-4 ${
          feedback.includes("✅")
            ? "bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200"
            : "bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200"
        }`}>
          {feedback}
        </div>
      )}

      <button
        onClick={checkAnswer}
        disabled={selectedLine === null}
        className="w-full bg-gradient-to-r from-red-500 to-pink-600 text-white py-3 rounded-xl font-bold hover:shadow-lg transform hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Report Bug
      </button>
    </div>
  );
};

export default BugHunter;