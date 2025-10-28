import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { FaGamepad, FaTrophy, FaClock, FaFire } from "react-icons/fa";

const Games = () => {
  const navigate = useNavigate();
  const [games, setGames] = useState([]);
  const [myScores, setMyScores] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGamesData();
  }, []);

  const fetchGamesData = async () => {
    try {
      // Always fetch games list (public endpoint)
      const gamesRes = await api.get("/games/list");
      setGames(gamesRes.data);
      
      // Try to fetch user-specific data (protected endpoints)
      try {
        const [scoresRes, statsRes] = await Promise.all([
          api.get("/games/my-scores"),
          api.get("/games/stats"),
        ]);
        setMyScores(scoresRes.data);
        setStats(statsRes.data);
      } catch (authErr) {
        console.log("User not authenticated, showing games only");
        // Set default stats for non-authenticated users
        setStats({
          total_games_played: 0,
          total_xp_earned: 0,
          best_score: 0,
          average_score: 0
        });
      }
    } catch (err) {
      console.error("Error fetching games:", err);
      alert("Failed to load games. Please refresh the page.");
    } finally {
      setLoading(false);
    }
  };

  const getGameIcon = (gameName) => {
    const icons = {
      "coding_challenge": "💻",
      "memory_match": "🧠",
      "speed_typing": "⚡",
      "syntax_puzzle": "🧩",
      "bug_hunter": "🐛",
      "algorithm_race": "🏁",
    };
    return icons[gameName] || "🎮";
  };

  const getMyBestScore = (gameName) => {
    const gameScores = myScores.filter(s => s.game_name === gameName);
    if (gameScores.length === 0) return null;
    return Math.max(...gameScores.map(s => s.score));
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
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-800 dark:text-white mb-4">
            🎮 Educational Games
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Learn while having fun! Earn XP and compete with others
          </p>
        </div>

        {/* Stats Overview */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-100 text-sm">Games Played</p>
                  <p className="text-3xl font-bold">{stats.total_games_played}</p>
                </div>
                <FaGamepad className="text-4xl text-blue-200" />
              </div>
            </div>
            <div className="bg-gradient-to-r from-yellow-500 to-yellow-600 text-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-yellow-100 text-sm">Total XP Earned</p>
                  <p className="text-3xl font-bold">{stats.total_xp_earned}</p>
                </div>
                <FaTrophy className="text-4xl text-yellow-200" />
              </div>
            </div>
            <div className="bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-100 text-sm">Best Score</p>
                  <p className="text-3xl font-bold">{stats.best_score}</p>
                </div>
                <FaFire className="text-4xl text-green-200" />
              </div>
            </div>
            <div className="bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-xl p-6 shadow-lg">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-100 text-sm">Avg Score</p>
                  <p className="text-3xl font-bold">{stats.average_score.toFixed(0)}</p>
                </div>
                <FaClock className="text-4xl text-purple-200" />
              </div>
            </div>
          </div>
        )}

        {/* Games Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {games.map((game) => {
            const bestScore = getMyBestScore(game.name);
            return (
              <div
                key={game.name}
                className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden hover:shadow-2xl transform hover:-translate-y-2 transition-all cursor-pointer"
                onClick={() => navigate(`/game/${game.name}`)}
              >
                {/* Game Header */}
                <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-6 text-white">
                  <div className="text-6xl mb-3 text-center">
                    {getGameIcon(game.name)}
                  </div>
                  <h3 className="text-2xl font-bold text-center mb-2">
                    {game.display_name}
                  </h3>
                  <p className="text-purple-100 text-center text-sm">
                    {game.description}
                  </p>
                </div>

                {/* Game Info */}
                <div className="p-6">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600 dark:text-gray-400">XP Multiplier</span>
                      <span className="font-bold text-yellow-600 dark:text-yellow-400">
                        {game.xp_multiplier}x
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Difficulty</span>
                      <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-xs font-semibold">
                        {game.difficulty}
                      </span>
                    </div>
                    {bestScore !== null && (
                      <div className="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-gray-700">
                        <span className="text-gray-600 dark:text-gray-400">Your Best</span>
                        <span className="font-bold text-green-600 dark:text-green-400 flex items-center gap-1">
                          <FaTrophy className="text-yellow-500" />
                          {bestScore}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Play Button */}
                  <button className="w-full mt-6 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-xl font-bold hover:shadow-lg transform hover:scale-105 transition-all">
                    Play Now
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* Recent Scores */}
        {myScores.length > 0 && (
          <div className="mt-12 bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
            <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">
              📊 Your Recent Scores
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <th className="text-left py-3 px-4 text-gray-600 dark:text-gray-400">Game</th>
                    <th className="text-left py-3 px-4 text-gray-600 dark:text-gray-400">Score</th>
                    <th className="text-left py-3 px-4 text-gray-600 dark:text-gray-400">XP Earned</th>
                    <th className="text-left py-3 px-4 text-gray-600 dark:text-gray-400">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {myScores.slice(0, 10).map((score, index) => (
                    <tr key={index} className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="py-3 px-4">
                        <span className="flex items-center gap-2">
                          <span>{getGameIcon(score.game_name)}</span>
                          <span className="font-semibold text-gray-800 dark:text-white">
                            {games.find(g => g.name === score.game_name)?.display_name}
                          </span>
                        </span>
                      </td>
                      <td className="py-3 px-4 font-bold text-blue-600 dark:text-blue-400">
                        {score.score}
                      </td>
                      <td className="py-3 px-4 font-bold text-yellow-600 dark:text-yellow-400">
                        +{score.xp_earned} XP
                      </td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-400">
                        {new Date(score.played_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Games;