import { useEffect, useState } from "react";
import { useAuthStore } from "../store/authStore";
import { Link } from "react-router-dom";
import api from "../services/api";
import { FaTrophy, FaStar, FaFire, FaBook } from "react-icons/fa";
import ProgressBar from "../components/ProgressBar";
import BadgeCard from "../components/BadgeCard";

const Dashboard = () => {
  const { user } = useAuthStore();
  const [stats, setStats] = useState(null);
  const [badges, setBadges] = useState([]);
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
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
      <div className="max-w-7xl mx-auto">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2">
            Welcome back, {user?.username}! 👋
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Continue your learning journey
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">Total XP</p>
                <p className="text-3xl font-bold text-blue-600">{user?.total_xp || 0}</p>
              </div>
              <FaStar className="text-4xl text-yellow-500" />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">Level</p>
                <p className="text-3xl font-bold text-purple-600">{user?.level || 1}</p>
              </div>
              <FaTrophy className="text-4xl text-purple-500" />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">Streak</p>
                <p className="text-3xl font-bold text-orange-600">{user?.streak_days || 0} days</p>
              </div>
              <FaFire className="text-4xl text-orange-500" />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">Rank</p>
                <p className="text-3xl font-bold text-green-600">#{stats?.rank || "N/A"}</p>
              </div>
              <FaBook className="text-4xl text-green-500" />
            </div>
          </div>
        </div>

        {/* Badges Section */}
        <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg mb-8">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">
            Your Badges ({badges.length})
          </h2>
          {badges.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {badges.map((userBadge) => (
                <BadgeCard key={userBadge.id} badge={userBadge.badge} earned={true} />
              ))}
            </div>
          ) : (
            <p className="text-gray-600 dark:text-gray-400">
              No badges earned yet. Complete lessons and quizzes to earn badges!
            </p>
          )}
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            to="/courses"
            className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6 rounded-xl shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all"
          >
            <h3 className="text-xl font-bold mb-2">Browse Courses</h3>
            <p>Explore our wide range of courses</p>
          </Link>

          <Link
            to="/leaderboard"
            className="bg-gradient-to-r from-purple-500 to-pink-600 text-white p-6 rounded-xl shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all"
          >
            <h3 className="text-xl font-bold mb-2">Leaderboard</h3>
            <p>See how you rank against others</p>
          </Link>

          <Link
            to="/profile"
            className="bg-gradient-to-r from-pink-500 to-orange-600 text-white p-6 rounded-xl shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all"
          >
            <h3 className="text-xl font-bold mb-2">Your Profile</h3>
            <p>View and edit your profile</p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;