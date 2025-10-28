import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import ReactMarkdown from "react-markdown";
import { FaTrophy, FaCheckCircle, FaLightbulb, FaSpinner } from "react-icons/fa";

const LessonDetail = () => {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [aiSummary, setAiSummary] = useState(null);
  const [generatingSummary, setGeneratingSummary] = useState(false);
  const [showSummary, setShowSummary] = useState(false);

  useEffect(() => {
    fetchLessonData();
  }, [lessonId]);

  const fetchLessonData = async () => {
    try {
      const [lessonRes, quizzesRes] = await Promise.all([
        api.get(`/lessons/${lessonId}`),
        api.get(`/quizzes/lesson/${lessonId}`),
      ]);
      setLesson(lessonRes.data);
      setQuizzes(quizzesRes.data);
      
      // Check if AI summary already exists
      if (lessonRes.data.ai_summary) {
        setAiSummary(lessonRes.data.ai_summary);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generateAISummary = async () => {
    setGeneratingSummary(true);
    try {
      const response = await api.post(`/lessons/${lessonId}/generate-summary`);
      setAiSummary(response.data.summary);
      setShowSummary(true);
      alert("AI Summary generated successfully! ✨");
    } catch (err) {
      console.error(err);
      alert("Failed to generate AI summary. Please try again.");
    } finally {
      setGeneratingSummary(false);
    }
  };

  const completeLesson = async () => {
    setCompleting(true);
    try {
      await api.post("/progress/lesson/complete", {
        lesson_id: parseInt(lessonId),
        time_spent_minutes: 30,
      });
      alert(`Lesson completed! You earned ${lesson.xp_reward} XP! 🎉`);
    } catch (err) {
      console.error(err);
      alert("Failed to complete lesson");
    } finally {
      setCompleting(false);
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
      <div className="max-w-4xl mx-auto">
        {/* Lesson Header */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-6">
          <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">
            {lesson?.title}
          </h1>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-2 text-yellow-600 dark:text-yellow-400 font-semibold">
              <FaTrophy />
              +{lesson?.xp_reward} XP
            </span>
            {lesson?.duration_minutes && (
              <span className="text-gray-600 dark:text-gray-400">
                ⏱️ {lesson.duration_minutes} minutes
              </span>
            )}
          </div>
        </div>

        {/* Video Player */}
        {lesson?.video_url && (
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mb-6">
            <div className="aspect-video bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center">
              <iframe
                src={lesson.video_url}
                className="w-full h-full rounded-lg"
                allowFullScreen
              ></iframe>
            </div>
          </div>
        )}

        {/* Lesson Content */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-6">
          <div className="prose dark:prose-invert max-w-none">
            <ReactMarkdown>{lesson?.content || "No content available"}</ReactMarkdown>
          </div>
        </div>

        {/* AI Summary Section */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-gray-800 dark:text-white flex items-center gap-2">
              <FaLightbulb className="text-yellow-500" />
              AI Lesson Summary
            </h2>
            <button
              onClick={aiSummary ? () => setShowSummary(!showSummary) : generateAISummary}
              disabled={generatingSummary}
              className="bg-gradient-to-r from-purple-500 to-pink-600 text-white px-4 py-2 rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 flex items-center gap-2"
            >
              {generatingSummary ? (
                <>
                  <FaSpinner className="animate-spin" />
                  Generating...
                </>
              ) : aiSummary ? (
                showSummary ? "Hide Summary" : "Show Summary"
              ) : (
                "Generate AI Summary"
              )}
            </button>
          </div>
          
          {showSummary && aiSummary && (
            <div className="bg-purple-50 dark:bg-purple-900 rounded-lg p-6">
              <div className="prose dark:prose-invert max-w-none">
                <ReactMarkdown>{aiSummary}</ReactMarkdown>
              </div>
            </div>
          )}
          
          {!aiSummary && !generatingSummary && (
            <p className="text-gray-600 dark:text-gray-400 text-center py-4">
              Click "Generate AI Summary" to get a concise summary of this lesson using AI
            </p>
          )}
        </div>

        {/* Complete Lesson Button */}
        <button
          onClick={completeLesson}
          disabled={completing}
          className="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white py-4 rounded-xl font-bold text-lg hover:shadow-2xl transform hover:scale-105 transition-all disabled:opacity-50 mb-6"
        >
          {completing ? "Completing..." : (
            <>
              <FaCheckCircle className="inline mr-2" />
              Mark as Complete
            </>
          )}
        </button>

        {/* Quizzes */}
        {quizzes.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
            <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">
              📝 Practice Quizzes
            </h2>
            <div className="space-y-3">
              {quizzes.map((quiz) => (
                <button
                  key={quiz.id}
                  onClick={() => navigate(`/quiz/${quiz.id}`)}
                  className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 rounded-xl hover:shadow-lg transform hover:scale-105 transition-all text-left"
                >
                  <h3 className="font-bold text-lg mb-1">{quiz.title}</h3>
                  <p className="text-sm text-blue-100">{quiz.description}</p>
                  <div className="flex items-center gap-4 mt-2 text-sm">
                    <span>⏱️ {quiz.time_limit_minutes} min</span>
                    <span>🎯 Passing: {quiz.passing_score}%</span>
                    <span>🏆 +{quiz.xp_reward} XP</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LessonDetail;