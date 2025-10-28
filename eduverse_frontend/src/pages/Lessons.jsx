import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../services/api";
import { FaPlay, FaClock, FaTrophy, FaCheckCircle } from "react-icons/fa";

const Lessons = () => {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCourseAndLessons();
  }, [courseId]);

  const fetchCourseAndLessons = async () => {
    try {
      const [courseRes, lessonsRes] = await Promise.all([
        api.get(`/courses/${courseId}`),
        api.get(`/lessons/course/${courseId}`),
      ]);
      setCourse(courseRes.data);
      setLessons(lessonsRes.data);
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
      <div className="max-w-5xl mx-auto">
        {/* Course Header */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8">
          <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">
            {course?.title}
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            {course?.description}
          </p>
          <div className="flex items-center gap-6 text-sm">
            <span className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
              <FaClock className="text-blue-500" />
              {course?.estimated_hours} hours
            </span>
            <span className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
              <FaTrophy className="text-yellow-500" />
              {course?.xp_reward} XP
            </span>
            <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-xs font-semibold">
              {course?.difficulty}
            </span>
          </div>
        </div>

        {/* Lessons List */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">
            📚 Course Lessons
          </h2>
          {lessons.map((lesson, index) => (
            <Link
              key={lesson.id}
              to={`/lesson/${lesson.id}`}
              className="block bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-2xl transform hover:-translate-y-1 transition-all"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 flex-1">
                  <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg">
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-1">
                      {lesson.title}
                    </h3>
                    <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                      {lesson.duration_minutes && (
                        <span className="flex items-center gap-1">
                          <FaClock className="text-blue-500" />
                          {lesson.duration_minutes} min
                        </span>
                      )}
                      {lesson.xp_reward && (
                        <span className="flex items-center gap-1">
                          <FaTrophy className="text-yellow-500" />
                          +{lesson.xp_reward} XP
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <FaPlay className="text-blue-500 text-2xl" />
              </div>
            </Link>
          ))}
        </div>

        {lessons.length === 0 && (
          <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl">
            <p className="text-gray-600 dark:text-gray-400 text-xl">
              No lessons available for this course yet.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Lessons;