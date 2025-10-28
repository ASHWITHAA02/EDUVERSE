import { useState, useEffect } from "react";

const MemoryMatch = ({ onComplete }) => {
  const [cards, setCards] = useState([]);
  const [flipped, setFlipped] = useState([]);
  const [matched, setMatched] = useState([]);
  const [moves, setMoves] = useState(0);
  const [score, setScore] = useState(0);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameEnded, setGameEnded] = useState(false);
  const [timeLeft, setTimeLeft] = useState(120); // 2 minutes

  const concepts = [
    { id: 1, term: "HTML", match: "Markup" },
    { id: 2, term: "CSS", match: "Styling" },
    { id: 3, term: "JS", match: "Logic" },
    { id: 4, term: "React", match: "Library" },
    { id: 5, term: "API", match: "Interface" },
    { id: 6, term: "DB", match: "Storage" },
    { id: 7, term: "Git", match: "Version" },
    { id: 8, term: "JSON", match: "Data" },
  ];

  useEffect(() => {
    if (gameStarted && !gameEnded && timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0 && !gameEnded) {
      endGame();
    }
  }, [timeLeft, gameStarted, gameEnded]);

  useEffect(() => {
    if (matched.length === concepts.length * 2 && gameStarted) {
      endGame();
    }
  }, [matched]);

  const startGame = () => {
    const cardPairs = concepts.flatMap(c => [
      { id: `${c.id}-term`, value: c.term, pairId: c.id },
      { id: `${c.id}-match`, value: c.match, pairId: c.id },
    ]);
    setCards(cardPairs.sort(() => Math.random() - 0.5));
    setGameStarted(true);
  };

  const handleCardClick = (card) => {
    if (flipped.length === 2 || flipped.includes(card.id) || matched.includes(card.id)) {
      return;
    }

    const newFlipped = [...flipped, card.id];
    setFlipped(newFlipped);

    if (newFlipped.length === 2) {
      setMoves(moves + 1);
      const [first, second] = newFlipped.map(id => cards.find(c => c.id === id));
      
      if (first.pairId === second.pairId) {
        setMatched([...matched, first.id, second.id]);
        setScore(score + 50);
        setFlipped([]);
      } else {
        setTimeout(() => setFlipped([]), 1000);
      }
    }
  };

  const endGame = () => {
    setGameEnded(true);
    const finalScore = score + (timeLeft * 2); // Bonus for time remaining
    onComplete(finalScore);
  };

  if (!gameStarted) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">🧠</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Memory Match
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Match programming concepts with their descriptions!
        </p>
        <div className="bg-blue-50 dark:bg-blue-900 rounded-lg p-4 mb-6">
          <h3 className="font-bold text-gray-800 dark:text-white mb-2">How to Play:</h3>
          <ul className="text-left text-gray-600 dark:text-gray-300 space-y-1">
            <li>• Match {concepts.length} pairs of cards</li>
            <li>• Each match: +50 points</li>
            <li>• Time bonus: +2 points per second remaining</li>
            <li>• Time limit: 2 minutes</li>
          </ul>
        </div>
        <button
          onClick={startGame}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all"
        >
          Start Game
        </button>
      </div>
    );
  }

  if (gameEnded) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 text-center">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
          Game Complete!
        </h2>
        <div className="text-5xl font-bold text-blue-600 dark:text-blue-400 mb-6">
          {score + (timeLeft * 2)} points
        </div>
        <p className="text-gray-600 dark:text-gray-300 mb-2">
          Matches: {matched.length / 2}/{concepts.length}
        </p>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Moves: {moves}
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

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white">Memory Match</h2>
          <p className="text-gray-600 dark:text-gray-400">Moves: {moves}</p>
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

      {/* Cards Grid */}
      <div className="grid grid-cols-4 gap-4">
        {cards.map((card) => {
          const isFlipped = flipped.includes(card.id) || matched.includes(card.id);
          const isMatched = matched.includes(card.id);
          
          return (
            <button
              key={card.id}
              onClick={() => handleCardClick(card)}
              className={`aspect-square rounded-xl font-bold text-lg transition-all transform hover:scale-105 ${
                isMatched
                  ? "bg-gradient-to-r from-green-400 to-emerald-500 text-white"
                  : isFlipped
                  ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white"
                  : "bg-gradient-to-r from-gray-300 to-gray-400 dark:from-gray-600 dark:to-gray-700 text-transparent"
              }`}
              disabled={isMatched}
            >
              {isFlipped ? card.value : "?"}
            </button>
          );
        })}
      </div>

      {/* Progress */}
      <div className="mt-6">
        <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
          <span>Progress</span>
          <span>{matched.length / 2}/{concepts.length} pairs</span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
          <div
            className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all"
            style={{ width: `${(matched.length / (concepts.length * 2)) * 100}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default MemoryMatch;