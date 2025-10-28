import { useEffect, useState } from "react";
import api from "../services/api";
import { FaTrophy, FaMedal, FaStar } from "react-icons/fa";

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const res = await api.get("/gamification/leaderboard?limit=20");
      setLeaderboard(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getRankIcon = (rank) => {
    switch (rank) {
      case 1:
        return <FaTrophy className="text-yellow-500 text-3xl" />;
      case 2:
        return <FaMedal className="text-gray-400 text-3xl" />;
      case 3:
        return <FaMedal className="text-orange-600 text-3xl" />;
      default:
        return <span className="text-2xl font-bold text-gray-500">#{rank}</span>;
    }
  };

  const getRankBg = (rank) => {
    switch (rank) {
      case 1:
        return "bg-gradient-to-r from-yellow-100 to-orange-100 dark:from-yellow-900/30 dark:to-orange-900/30 border-yellow-400";
      case 2:
        return "bg-gradient-to-r from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-700 border-gray-400";
      case 3:
        return "bg-gradient-to-r from-orange-100 to-red-100 dark:from-orange-900/30 dark:to-red-900/30 border-orange-600";
      default:
        return "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700";
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-purple-900 dark:to-gray-900 p-6">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            🏆 Leaderboard
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            See how you rank against other learners!
          </p>
        </div>

        {/* Top 3 Podium */}
        {leaderboard.length >= 3 && (
          <div className="grid grid-cols-3 gap-4 mb-8">
            {/* 2nd Place */}
            <div className="flex flex-col items-center pt-12">
              <div className="bg-gradient-to-r from-gray-300 to-gray-400 text-white w-20 h-20 rounded-full flex items-center justify-center text-3xl font-bold mb-2">
                {leaderboard[1]?.username.charAt(0).toUpperCase()}
              </div>
              <FaMedal className="text-gray-400 text-4xl mb-2" />
              <h3 className="font-bold text-gray-800 dark:text-white">{leaderboard[1]?.username}</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">{leaderboard[1]?.total_xp} XP</p>
            </div>

            {/* 1st Place */}
            <div className="flex flex-col items-center">
              <div className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white w-24 h-24 rounded-full flex items-center justify-center text-4xl font-bold mb-2">
                {leaderboard[0]?.username.charAt(0).toUpperCase()}
              </div>
              <FaTrophy className="text-yellow-500 text-5xl mb-2" />
              <h3 className="font-bold text-xl text-gray-800 dark:text-white">{leaderboard[0]?.username}</h3>
              <p className="text-gray-600 dark:text-gray-400">{leaderboard[0]?.total_xp} XP</p>
            </div>

            {/* 3rd Place */}
            <div className="flex flex-col items-center pt-16">
              <div className="bg-gradient-to-r from-orange-400 to-red-500 text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mb-2">
                {leaderboard[2]?.username.charAt(0).toUpperCase()}
              </div>
              <FaMedal className="text-orange-600 text-3xl mb-2" />
              <h3 className="font-bold text-gray-800 dark:text-white">{leaderboard[2]?.username}</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">{leaderboard[2]?.total_xp} XP</p>
            </div>
          </div>
        )}

        {/* Full Leaderboard */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
          <div className="p-6 bg-gradient-to-r from-blue-500 to-purple-600">
            <h2 className="text-2xl font-bold text-white">Rankings</h2>
          </div>
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {leaderboard.map((user) => (
              <div
                key={user.rank}
                className={`p-4 flex items-center justify-between border-l-4 ${getRankBg(user.rank)}`}
              >
                <div className="flex items-center gap-4">
                  <div className="w-16 flex justify-center">
                    {getRankIcon(user.rank)}
                  </div>
                  <div>
                    <h3 className="font-bold text-lg text-gray-800 dark:text-white">
                      {user.username}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Level {user.level} • {user.streak_days} day streak 🔥
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                    {user.total_xp}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">XP</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {leaderboard.length === 0 && (
          <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
            <p className="text-gray-600 dark:text-gray-400 text-xl">
              No rankings available yet. Be the first to earn XP!
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Leaderboard;