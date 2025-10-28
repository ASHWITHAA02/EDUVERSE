import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import { FaClock, FaTrophy, FaCheckCircle } from "react-icons/fa";

const Quiz = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetchQuiz();
  }, [quizId]);

  const fetchQuiz = async () => {
    try {
      const res = await api.get(`/quizzes/${quizId}`);
      setQuiz(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, optionId) => {
    setAnswers({ ...answers, [questionId]: optionId });
  };

  const submitQuiz = async () => {
    if (Object.keys(answers).length < quiz.questions.length) {
      alert("Please answer all questions before submitting!");
      return;
    }

    setSubmitting(true);
    try {
      const res = await api.post("/quiz-submissions/submit", {
        quiz_id: parseInt(quizId),
        answers: answers,
        time_taken_minutes: 10,
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to submit quiz");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
      </div>
    );
  }

  if (result) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-purple-900 dark:to-gray-900 p-6 flex items-center justify-center">
        <div className="max-w-2xl w-full bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 text-center">
          <div className={`text-6xl mb-4 ${result.passed ? "text-green-500" : "text-red-500"}`}>
            {result.passed ? "🎉" : "😔"}
          </div>
          <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-4">
            {result.passed ? "Congratulations!" : "Keep Trying!"}
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-6">
            You scored {result.score.toFixed(1)}%
          </p>
          <div className="bg-gray-100 dark:bg-gray-700 rounded-xl p-6 mb-6">
            <div className="grid grid-cols-2 gap-4 text-left">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Points Earned</p>
                <p className="text-2xl font-bold text-blue-600">{result.earned_points}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Points</p>
                <p className="text-2xl font-bold text-purple-600">{result.total_points}</p>
              </div>
            </div>
          </div>
          {result.passed && (
            <div className="bg-gradient-to-r from-yellow-100 to-orange-100 dark:from-yellow-900/30 dark:to-orange-900/30 p-4 rounded-xl mb-6">
              <p className="text-lg font-bold text-gray-800 dark:text-white">
                <FaTrophy className="inline text-yellow-500 mr-2" />
                You earned {result.xp_earned} XP!
              </p>
            </div>
          )}
          <button
            onClick={() => navigate(-1)}
            className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-3 rounded-xl font-bold hover:shadow-lg transform hover:scale-105 transition-all"
          >
            Back to Lesson
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-purple-900 dark:to-gray-900 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Quiz Header */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-6">
          <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">
            {quiz?.title}
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            {quiz?.description}
          </p>
          <div className="flex items-center gap-6 text-sm">
            <span className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
              <FaClock className="text-blue-500" />
              {quiz?.time_limit_minutes} minutes
            </span>
            <span className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
              <FaTrophy className="text-yellow-500" />
              {quiz?.xp_reward} XP
            </span>
            <span className="text-gray-600 dark:text-gray-400">
              🎯 Passing Score: {quiz?.passing_score}%
            </span>
          </div>
        </div>

        {/* Questions */}
        <div className="space-y-6">
          {quiz?.questions.map((question, qIndex) => (
            <div key={question.id} className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
              <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
                {qIndex + 1}. {question.question_text}
              </h3>
              <div className="space-y-3">
                {question.options.map((option) => (
                  <button
                    key={option.id}
                    onClick={() => handleAnswerSelect(question.id, option.id)}
                    className={`w-full text-left p-4 rounded-xl border-2 transition-all ${
                      answers[question.id] === option.id
                        ? "border-blue-500 bg-blue-50 dark:bg-blue-900/30"
                        : "border-gray-200 dark:border-gray-700 hover:border-blue-300"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                          answers[question.id] === option.id
                            ? "border-blue-500 bg-blue-500"
                            : "border-gray-300 dark:border-gray-600"
                        }`}
                      >
                        {answers[question.id] === option.id && (
                          <FaCheckCircle className="text-white text-sm" />
                        )}
                      </div>
                      <span className="text-gray-800 dark:text-white">{option.option_text}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Submit Button */}
        <button
          onClick={submitQuiz}
          disabled={submitting}
          className="w-full mt-6 bg-gradient-to-r from-green-500 to-emerald-600 text-white py-4 rounded-xl font-bold text-lg hover:shadow-2xl transform hover:scale-105 transition-all disabled:opacity-50"
        >
          {submitting ? "Submitting..." : "Submit Quiz"}
        </button>
      </div>
    </div>
  );
};

export default Quiz;