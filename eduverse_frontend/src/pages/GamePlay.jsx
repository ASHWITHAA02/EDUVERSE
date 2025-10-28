import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import CodingChallenge from "../components/games/CodingChallenge";
import MemoryMatch from "../components/games/MemoryMatch";
import SpeedTyping from "../components/games/SpeedTyping";
import SyntaxPuzzle from "../components/games/SyntaxPuzzle";
import BugHunter from "../components/games/BugHunter";
import AlgorithmRace from "../components/games/AlgorithmRace";

const GamePlay = () => {
  const { gameName } = useParams();
  const navigate = useNavigate();
  const [gameInfo, setGameInfo] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGameData();
  }, [gameName]);

  const fetchGameData = async () => {
    try {
      const [gameRes, leaderboardRes] = await Promise.all([
        api.get(`/games/game/${gameName}`),
        api.get(`/games/leaderboard/${gameName}`),
      ]);
      setGameInfo(gameRes.data);
      setLeaderboard(leaderboardRes.data);
    } catch (err) {
      console.error("Error fetching game data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleGameComplete = async (score) => {
    try {
      const response = await api.post("/games/submit-score", {
        game_name: gameName,
        score: score,
      });
      
      alert(`🎉 Game Complete!\n\nScore: ${score}\nXP Earned: ${response.data.xp_earned}\n\nGreat job!`);
      
      // Refresh leaderboard
      fetchGameData();
    } catch (err) {
      console.error("Error submitting score:", err);
      alert("Failed to submit score. Please try again.");
    }
  };

  const renderGame = () => {
    const gameComponents = {
      coding_challenge: CodingChallenge,
      memory_match: MemoryMatch,
      speed_typing: SpeedTyping,
      syntax_puzzle: SyntaxPuzzle,
      bug_hunter: BugHunter,
      algorithm_race: AlgorithmRace,
    };

    const GameComponent = gameComponents[gameName];
    
    if (!GameComponent) {
      return (
        <div className="text-center py-12">
          <p className="text-xl text-gray-600 dark:text-gray-400">
            Game not found
          </p>
        </div>
      );
    }

    return <GameComponent onComplete={handleGameComplete} gameInfo={gameInfo} />;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-purple-900 dark:to-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <button
            onClick={() => navigate("/games")}
            className="bg-white dark:bg-gray-800 px-4 py-2 rounded-lg shadow hover:shadow-lg transition-all"
          >
            ← Back to Games
          </button>
          <h1 className="text-3xl font-bold text-gray-800 dark:text-white">
            {gameInfo?.display_name}
          </h1>
          <div className="w-32"></div> {/* Spacer for centering */}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Game Area */}
          <div className="lg:col-span-2">
            {renderGame()}
          </div>

          {/* Leaderboard Sidebar */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 h-fit">
            <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
              🏆 Leaderboard
            </h2>
            <div className="space-y-3">
              {leaderboard.map((entry, index) => (
                <div
                  key={index}
                  className={`flex items-center justify-between p-3 rounded-lg ${
                    index === 0
                      ? "bg-gradient-to-r from-yellow-400 to-yellow-500 text-white"
                      : index === 1
                      ? "bg-gradient-to-r from-gray-300 to-gray-400 text-gray-800"
                      : index === 2
                      ? "bg-gradient-to-r from-orange-400 to-orange-500 text-white"
                      : "bg-gray-100 dark:bg-gray-700"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="font-bold text-lg">#{index + 1}</span>
                    <div>
                      <p className="font-semibold">{entry.username}</p>
                      <p className="text-sm opacity-80">
                        {new Date(entry.played_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-lg">{entry.score}</p>
                    <p className="text-sm opacity-80">+{entry.xp_earned} XP</p>
                  </div>
                </div>
              ))}
              {leaderboard.length === 0 && (
                <p className="text-center text-gray-500 dark:text-gray-400 py-8">
                  No scores yet. Be the first!
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GamePlay;