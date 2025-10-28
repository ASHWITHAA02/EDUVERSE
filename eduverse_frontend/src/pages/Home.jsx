import { Link } from "react-router-dom";
import { FaRocket, FaBrain, FaTrophy, FaUsers } from "react-icons/fa";

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-500 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-6xl font-bold mb-6 animate-fade-in">
              Welcome to EduVerse 🎓
            </h1>
            <p className="text-2xl mb-8 text-blue-100">
              AI-Enhanced Learning Management System
            </p>
            <p className="text-xl mb-10 max-w-3xl mx-auto">
              Experience personalized learning with AI-powered recommendations,
              interactive quizzes, and gamified progress tracking.
            </p>
            <div className="flex gap-4 justify-center">
              <Link
                to="/register"
                className="px-8 py-4 bg-white text-blue-600 rounded-full font-bold text-lg hover:shadow-2xl transform hover:scale-105 transition-all"
              >
                Get Started Free
              </Link>
              <Link
                to="/courses"
                className="px-8 py-4 bg-transparent border-2 border-white text-white rounded-full font-bold text-lg hover:bg-white hover:text-blue-600 transition-all"
              >
                Explore Courses
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-center mb-12 text-gray-800 dark:text-white">
            Why Choose EduVerse?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center p-6 rounded-xl bg-blue-50 dark:bg-gray-800 hover:shadow-xl transition">
              <FaBrain className="text-5xl text-blue-500 mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2 text-gray-800 dark:text-white">
                AI-Powered Learning
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Get personalized recommendations based on your performance
              </p>
            </div>

            <div className="text-center p-6 rounded-xl bg-purple-50 dark:bg-gray-800 hover:shadow-xl transition">
              <FaTrophy className="text-5xl text-purple-500 mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2 text-gray-800 dark:text-white">
                Gamification
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Earn XP, badges, and climb the leaderboard
              </p>
            </div>

            <div className="text-center p-6 rounded-xl bg-pink-50 dark:bg-gray-800 hover:shadow-xl transition">
              <FaRocket className="text-5xl text-pink-500 mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2 text-gray-800 dark:text-white">
                Interactive Quizzes
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Test your knowledge with AI-generated quizzes
              </p>
            </div>

            <div className="text-center p-6 rounded-xl bg-green-50 dark:bg-gray-800 hover:shadow-xl transition">
              <FaUsers className="text-5xl text-green-500 mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2 text-gray-800 dark:text-white">
                Community Learning
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Learn together and compete with peers
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-500 to-purple-600 text-white">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-4xl font-bold mb-6">Ready to Start Learning?</h2>
          <p className="text-xl mb-8">
            Join thousands of students already learning on EduVerse
          </p>
          <Link
            to="/register"
            className="px-10 py-4 bg-white text-blue-600 rounded-full font-bold text-lg hover:shadow-2xl transform hover:scale-105 transition-all inline-block"
          >
            Create Free Account
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;