import { useEffect, useState } from "react";
import { useAuthStore } from "../store/authStore";
import api from "../services/api";
import { FaTrophy, FaStar, FaFire, FaMedal } from "react-icons/fa";
import BadgeCard from "../components/BadgeCard";

const Profile = () => {
  const { user } = useAuthStore();
  const [stats, setStats] = useState(null);
  const [badges, setBadges] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      const [statsRes, badgesRes] = await Promise.all([
        api.get("/gamification/stats"),
        api.get("/gamification/badges/user"),
      ]);
      setStats(statsRes.data);
      setBadges(badgesRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
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
      <div className="max-w-6xl mx-auto">
        {/* Profile Header */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8">
          <div className="flex items-center gap-6">
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white w-24 h-24 rounded-full flex items-center justify-center text-4xl font-bold">
              {user?.username.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1">
              <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2">
                {user?.full_name || user?.username}
              </h1>
              <p className="text-gray-600 dark:text-gray-400 mb-4">@{user?.username}</p>
              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2">
                  <FaStar className="text-yellow-500" />
                  <span className="font-bold text-gray-800 dark:text-white">
                    Level {user?.level}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <FaTrophy className="text-blue-500" />
                  <span className="font-bold text-gray-800 dark:text-white">
                    {user?.total_xp} XP
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <FaFire className="text-orange-500" />
                  <span className="font-bold text-gray-800 dark:text-white">
                    {user?.streak_days} day streak
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg text-center">
            <FaTrophy className="text-4xl text-yellow-500 mx-auto mb-2" />
            <p className="text-3xl font-bold text-gray-800 dark:text-white">{user?.total_xp}</p>
            <p className="text-gray-600 dark:text-gray-400">Total XP</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg text-center">
            <FaStar className="text-4xl text-purple-500 mx-auto mb-2" />
            <p className="text-3xl font-bold text-gray-800 dark:text-white">{user?.level}</p>
            <p className="text-gray-600 dark:text-gray-400">Level</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg text-center">
            <FaMedal className="text-4xl text-blue-500 mx-auto mb-2" />
            <p className="text-3xl font-bold text-gray-800 dark:text-white">#{stats?.rank || "N/A"}</p>
            <p className="text-gray-600 dark:text-gray-400">Global Rank</p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg text-center">
            <FaFire className="text-4xl text-orange-500 mx-auto mb-2" />
            <p className="text-3xl font-bold text-gray-800 dark:text-white">{user?.streak_days}</p>
            <p className="text-gray-600 dark:text-gray-400">Day Streak</p>
          </div>
        </div>

        {/* Badges Section */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
          <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">
            🏅 Your Badges ({badges.length})
          </h2>
          {badges.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {badges.map((userBadge) => (
                <BadgeCard key={userBadge.id} badge={userBadge.badge} earned={true} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-600 dark:text-gray-400 text-lg">
                No badges earned yet. Complete lessons and quizzes to earn badges!
              </p>
            </div>
          )}
        </div>

        {/* Account Info */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mt-8">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">
            Account Information
          </h2>
          <div className="space-y-4">
            <div>
              <label className="text-sm text-gray-600 dark:text-gray-400">Email</label>
              <p className="text-lg text-gray-800 dark:text-white">{user?.email}</p>
            </div>
            <div>
              <label className="text-sm text-gray-600 dark:text-gray-400">Username</label>
              <p className="text-lg text-gray-800 dark:text-white">{user?.username}</p>
            </div>
            <div>
              <label className="text-sm text-gray-600 dark:text-gray-400">Member Since</label>
              <p className="text-lg text-gray-800 dark:text-white">
                {new Date(user?.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;