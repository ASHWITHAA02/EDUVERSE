import { useState, useEffect } from "react";
import { FaCode, FaCheckCircle, FaTimesCircle } from "react-icons/fa";

const CodingChallenge = ({ onComplete }) => {
  const [currentChallenge, setCurrentChallenge] = useState(0);
  const [userCode, setUserCode] = useState("");
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes
  const [gameStarted, setGameStarted] = useState(false);
  const [gameEnded, setGameEnded] = useState(false);
  const [feedback, setFeedback] = useState("");

  const challenges = [
    {
      title: "Reverse a String",
      description: "Write a function that reverses a string",
      starterCode: "function reverseString(str) {\n  // Your code here\n}",
      testCases: [
        { input: "hello", expected: "olleh" },
        { input: "world", expected: "dlrow" },
      ],
      solution: "function reverseString(str) {\n  return str.split('').reverse().join('');\n}",
    },
    {
      title: "Find Maximum",
      description: "Write a function that finds the maximum number in an array",
      starterCode: "function findMax(arr) {\n  // Your code here\n}",
      testCases: [
        { input: [1, 5, 3, 9, 2], expected: 9 },
        { input: [10, 20, 5], expected: 20 },
      ],
      solution: "function findMax(arr) {\n  return Math.max(...arr);\n}",
    },
    {
      title: "Sum Array",
      description: "Write a function that sums all numbers in an array",
      starterCode: "function sumArray(arr) {\n  // Your code here\n}",
      testCases: [
        { input: [1, 2, 3, 4], expected: 10 },
        { input: [5, 10, 15], expected: 30 },
      ],
      solution: "function sumArray(arr) {\n  return arr.reduce((a, b) => a + b, 0);\n}",
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
    setUserCode(challenges[0].starterCode);
  };

  const checkSolution = () => {
    try {
      // Simple check: compare with solution (in real app, would run test cases)
      const challenge = challenges[currentChallenge];
      const isCorrect = userCode.trim().includes("return") && userCode.length > 20;
      
      if (isCorrect) {
        setScore(score + 100);
        setFeedback("✅ Correct! Moving to next challenge...");
        
        setTimeout(() => {
          if (currentChallenge < challenges.length - 1) {
            setCurrentChallenge(currentChallenge + 1);
            setUserCode(challenges[currentChallenge + 1].starterCode);
            setFeedback("");
          } else {
            endGame();
          }
        }, 1500);
      } else {
        setFeedback("❌ Not quite right. Try again!");
      }
    } catch (err) {
      setFeedback("❌ Syntax error in your code!");
    }
  };

  const skipChallenge = () => {
    if (currentChallenge < challenges.length - 1) {
      setCurrentChallenge(currentChallenge + 1);
      setUserCode(challenges[currentChallenge + 1].starterCode);
      setFeedback("");
    } else {
      endGame();
    }
  };

  const endGame = () => {
    setGameEnded(true);
    onComplete(score);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  if (!gameStarted) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">💻</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Coding Challenge
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Solve coding problems as fast as you can!
        </p>
        <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 mb-6">
          <h3 className="font-bold text-gray-800 dark:text-white mb-2">How to Play:</h3>
          <ul className="text-left text-gray-600 dark:text-gray-300 space-y-1">
            <li>• Complete {challenges.length} coding challenges</li>
            <li>• Each correct solution: +100 points</li>
            <li>• Time limit: 5 minutes</li>
            <li>• Write clean, working code</li>
          </ul>
        </div>
        <button
          onClick={startGame}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all"
        >
          Start Challenge
        </button>
      </div>
    );
  }

  if (gameEnded) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Challenge Complete!
        </h2>
        <div className="text-5xl font-bold text-blue-600 dark:text-blue-400 mb-6">
          {score} points
        </div>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          You completed {currentChallenge + 1} out of {challenges.length} challenges!
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
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
            Challenge {currentChallenge + 1}/{challenges.length}
          </h2>
          <p className="text-gray-600 dark:text-gray-400">{challenge.title}</p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
            {formatTime(timeLeft)}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Score: {score}
          </div>
        </div>
      </div>

      {/* Challenge Description */}
      <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 mb-4">
        <p className="text-gray-800 dark:text-white font-semibold">
          {challenge.description}
        </p>
      </div>

      {/* Code Editor */}
      <div className="mb-4">
        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
          Your Solution:
        </label>
        <textarea
          value={userCode}
          onChange={(e) => setUserCode(e.target.value)}
          className="w-full h-64 p-4 bg-gray-900 text-green-400 font-mono text-sm rounded-lg border-2 border-gray-700 focus:border-blue-500 focus:outline-none"
          spellCheck="false"
        />
      </div>

      {/* Feedback */}
      {feedback && (
        <div className={`p-4 rounded-lg mb-4 ${
          feedback.includes("✅") 
            ? "bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200" 
            : "bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200"
        }`}>
          {feedback}
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-4">
        <button
          onClick={checkSolution}
          className="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 text-white py-3 rounded-xl font-bold hover:shadow-lg transform hover:scale-105 transition-all"
        >
          <FaCheckCircle className="inline mr-2" />
          Submit Solution
        </button>
        <button
          onClick={skipChallenge}
          className="bg-gray-300 dark:bg-gray-700 text-gray-800 dark:text-white px-6 py-3 rounded-xl font-bold hover:shadow-lg transition-all"
        >
          Skip
        </button>
      </div>

      {/* Hint */}
      <div className="mt-4 text-center">
        <button
          onClick={() => alert(`Hint: ${challenge.solution}`)}
          className="text-blue-600 dark:text-blue-400 hover:underline text-sm"
        >
          💡 Show Solution (for learning)
        </button>
      </div>
    </div>
  );
};

export default CodingChallenge;