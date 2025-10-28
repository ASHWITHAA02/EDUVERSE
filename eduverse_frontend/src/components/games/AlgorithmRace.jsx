import { useState, useEffect } from "react";

const AlgorithmRace = ({ onComplete }) => {
  const [currentChallenge, setCurrentChallenge] = useState(0);
  const [userCode, setUserCode] = useState("");
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(300);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameEnded, setGameEnded] = useState(false);
  const [feedback, setFeedback] = useState("");

  const challenges = [
    {
      title: "Binary Search",
      description: "Implement binary search algorithm",
      hint: "Use divide and conquer approach",
      starter: "function binarySearch(arr, target) {\n  // Your code here\n}",
    },
    {
      title: "Bubble Sort",
      description: "Implement bubble sort algorithm",
      hint: "Compare adjacent elements and swap",
      starter: "function bubbleSort(arr) {\n  // Your code here\n}",
    },
    {
      title: "Fibonacci",
      description: "Calculate nth Fibonacci number",
      hint: "Use recursion or iteration",
      starter: "function fibonacci(n) {\n  // Your code here\n}",
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
    setUserCode(challenges[0].starter);
  };

  const submitSolution = () => {
    if (userCode.includes("return") && userCode.length > 50) {
      setScore(score + 250);
      setFeedback("✅ Algorithm implemented! Moving to next challenge...");
      
      setTimeout(() => {
        if (currentChallenge < challenges.length - 1) {
          setCurrentChallenge(currentChallenge + 1);
          setUserCode(challenges[currentChallenge + 1].starter);
          setFeedback("");
        } else {
          endGame();
        }
      }, 1500);
    } else {
      setFeedback("❌ Implementation incomplete. Keep coding!");
    }
  };

  const endGame = () => {
    setGameEnded(true);
    onComplete(score);
  };

  if (!gameStarted) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">🏁</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Algorithm Race
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Implement algorithms as fast as you can!
        </p>
        <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 mb-6">
          <h3 className="font-bold text-gray-800 dark:text-white mb-2">How to Play:</h3>
          <ul className="text-left text-gray-600 dark:text-gray-300 space-y-1">
            <li>• Implement {challenges.length} algorithms</li>
            <li>• Each algorithm: +250 points</li>
            <li>• Time limit: 5 minutes</li>
            <li>• Use hints if needed</li>
          </ul>
        </div>
        <button
          onClick={startGame}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all"
        >
          Start Race
        </button>
      </div>
    );
  }

  if (gameEnded) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Race Complete!
        </h2>
        <div className="text-5xl font-bold text-blue-600 dark:text-blue-400 mb-6">
          {score} points
        </div>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Algorithms completed: {currentChallenge + 1}/{challenges.length}
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

  const challenge = challenges[currentChallenge];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
            {challenge.title}
          </h2>
          <p className="text-gray-600 dark:text-gray-400">{challenge.description}</p>
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

      <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 mb-4">
        <p className="text-gray-800 dark:text-white">
          💡 Hint: {challenge.hint}
        </p>
      </div>

      <textarea
        value={userCode}
        onChange={(e) => setUserCode(e.target.value)}
        className="w-full h-64 p-4 bg-gray-900 text-green-400 font-mono text-sm rounded-lg border-2 border-gray-700 focus:border-blue-500 focus:outline-none mb-4"
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
        onClick={submitSolution}
        className="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white py-3 rounded-xl font-bold hover:shadow-lg transform hover:scale-105 transition-all"
      >
        Submit Algorithm
      </button>
    </div>
  );
};

export default AlgorithmRace;