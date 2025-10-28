import { useState, useEffect } from "react";

const SyntaxPuzzle = ({ onComplete }) => {
  const [currentPuzzle, setCurrentPuzzle] = useState(0);
  const [userAnswer, setUserAnswer] = useState("");
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(180);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameEnded, setGameEnded] = useState(false);
  const [feedback, setFeedback] = useState("");

  const puzzles = [
    {
      broken: "function greet(name {\n  console.log('Hello' + name);\n}",
      fixed: "function greet(name) {\n  console.log('Hello ' + name);\n}",
      errors: ["Missing closing parenthesis", "Missing space in string"],
    },
    {
      broken: "const arr = [1, 2, 3\nconst sum = arr.reduce((a, b) => a + b);",
      fixed: "const arr = [1, 2, 3];\nconst sum = arr.reduce((a, b) => a + b);",
      errors: ["Missing closing bracket", "Missing semicolon"],
    },
    {
      broken: "if (x > 5 {\n  return true\n}",
      fixed: "if (x > 5) {\n  return true;\n}",
      errors: ["Missing closing parenthesis", "Missing semicolon"],
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
    setUserAnswer(puzzles[0].broken);
  };

  const checkAnswer = () => {
    const puzzle = puzzles[currentPuzzle];
    if (userAnswer.trim() === puzzle.fixed.trim()) {
      setScore(score + 150);
      setFeedback("✅ Perfect! All syntax errors fixed!");
      
      setTimeout(() => {
        if (currentPuzzle < puzzles.length - 1) {
          setCurrentPuzzle(currentPuzzle + 1);
          setUserAnswer(puzzles[currentPuzzle + 1].broken);
          setFeedback("");
        } else {
          endGame();
        }
      }, 1500);
    } else {
      setFeedback("❌ Not quite right. Check the errors list!");
    }
  };

  const endGame = () => {
    setGameEnded(true);
    onComplete(score);
  };

  if (!gameStarted) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">🧩</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Syntax Puzzle
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Fix the syntax errors in the code!
        </p>
        <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 mb-6">
          <h3 className="font-bold text-gray-800 dark:text-white mb-2">How to Play:</h3>
          <ul className="text-left text-gray-600 dark:text-gray-300 space-y-1">
            <li>• Fix all syntax errors in the code</li>
            <li>• Each puzzle: +150 points</li>
            <li>• Time limit: 3 minutes</li>
            <li>• Read the error hints carefully</li>
          </ul>
        </div>
        <button
          onClick={startGame}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all"
        >
          Start Puzzle
        </button>
      </div>
    );
  }

  if (gameEnded) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Puzzle Complete!
        </h2>
        <div className="text-5xl font-bold text-blue-600 dark:text-blue-400 mb-6">
          {score} points
        </div>
        <button
          onClick={() => window.location.reload()}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all"
        >
          Play Again
        </button>
      </div>
    );
  }

  const puzzle = puzzles[currentPuzzle];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
            Puzzle {currentPuzzle + 1}/{puzzles.length}
          </h2>
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

      <div className="bg-red-50 dark:bg-red-900 rounded-lg p-4 mb-4">
        <h3 className="font-bold text-red-800 dark:text-red-200 mb-2">Errors Found:</h3>
        <ul className="text-red-700 dark:text-red-300 space-y-1">
          {puzzle.errors.map((error, i) => (
            <li key={i}>• {error}</li>
          ))}
        </ul>
      </div>

      <textarea
        value={userAnswer}
        onChange={(e) => setUserAnswer(e.target.value)}
        className="w-full h-48 p-4 bg-gray-900 text-green-400 font-mono text-sm rounded-lg border-2 border-gray-700 focus:border-blue-500 focus:outline-none mb-4"
        spellCheck="false"
      />

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
        className="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white py-3 rounded-xl font-bold hover:shadow-lg transform hover:scale-105 transition-all"
      >
        Check Solution
      </button>
    </div>
  );
};

export default SyntaxPuzzle;