import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import { FaCheckCircle, FaTimesCircle, FaLightbulb } from "react-icons/fa";

const Assessment = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuestions();
  }, [courseId]);

  const fetchQuestions = async () => {
    try {
      const response = await api.get(`/assessment/course/${courseId}/questions`);
      setQuestions(response.data.questions);
    } catch (err) {
      console.error("Error fetching questions:", err);
      alert("Failed to load assessment questions");
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionIndex, answer) => {
    setAnswers({
      ...answers,
      [questionIndex]: answer,
    });
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length < questions.length) {
      alert("Please answer all questions before submitting");
      return;
    }

    try {
      const response = await api.post("/assessment/submit", {
        course_id: parseInt(courseId),
        answers: Object.values(answers),
      });
      
      setResult(response.data);
      setSubmitted(true);
    } catch (err) {
      console.error("Error submitting assessment:", err);
      alert("Failed to submit assessment");
    }
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500"></div>
      </div>
    );
  }

  if (submitted && result) {
    const scorePercentage = result.score_percentage;
    const passed = scorePercentage >= 50;

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-purple-900 dark:to-gray-900 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
            {/* Result Header */}
            <div className="text-center mb-8">
              <div className="text-6xl mb-4">
                {passed ? "🎉" : "📚"}
              </div>
              <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">
                Assessment Complete!
              </h1>
              <div className={`text-6xl font-bold mb-4 ${
                scorePercentage >= 80 ? "text-green-600" :
                scorePercentage >= 50 ? "text-yellow-600" :
                "text-red-600"
              }`}>
                {scorePercentage}%
              </div>
              <p className="text-xl text-gray-600 dark:text-gray-300">
                You scored {result.score} out of {result.total_questions} questions
              </p>
              <p className="text-lg text-green-600 dark:text-green-400 mt-2">
                +{result.xp_earned} XP Earned!
              </p>
            </div>

            {/* Recommendations */}
            <div className="bg-blue-50 dark:bg-blue-900 rounded-xl p-6 mb-6">
              <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
                <FaLightbulb className="text-yellow-500" />
                AI Recommendations
              </h2>
              <div className="space-y-3">
                {result.recommendations.map((rec, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <span className="text-blue-600 dark:text-blue-400 font-bold">•</span>
                    <p className="text-gray-800 dark:text-white">{rec}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Focus Areas */}
            {result.focus_areas && result.focus_areas.length > 0 && (
              <div className="bg-yellow-50 dark:bg-yellow-900 rounded-xl p-6 mb-6">
                <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">
                  📌 Focus Areas
                </h2>
                <div className="flex flex-wrap gap-2">
                  {result.focus_areas.map((area, index) => (
                    <span
                      key={index}
                      className="px-4 py-2 bg-yellow-200 dark:bg-yellow-800 text-yellow-900 dark:text-yellow-100 rounded-full font-semibold"
                    >
                      {area}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Action Message */}
            <div className={`rounded-xl p-6 mb-6 ${
              scorePercentage >= 80
                ? "bg-green-50 dark:bg-green-900"
                : scorePercentage >= 50
                ? "bg-blue-50 dark:bg-blue-900"
                : "bg-red-50 dark:bg-red-900"
            }`}>
              <p className={`text-lg font-semibold ${
                scorePercentage >= 80
                  ? "text-green-800 dark:text-green-200"
                  : scorePercentage >= 50
                  ? "text-blue-800 dark:text-blue-200"
                  : "text-red-800 dark:text-red-200"
              }`}>
                {scorePercentage >= 80
                  ? "🌟 Excellent! You can skip the basics and focus on advanced topics."
                  : scorePercentage >= 50
                  ? "👍 Good start! Follow the recommended learning path for best results."
                  : "📖 We recommend reviewing the fundamentals before proceeding."}
              </p>
            </div>

            {/* Actions */}
            <div className="flex gap-4">
              <button
                onClick={() => navigate(`/lessons/${courseId}`)}
                className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all"
              >
                Start Learning
              </button>
              <button
                onClick={() => navigate("/courses")}
                className="flex-1 bg-gray-300 dark:bg-gray-700 text-gray-800 dark:text-white py-4 rounded-xl font-bold text-lg hover:shadow-lg transition-all"
              >
                Back to Courses
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const question = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-purple-900 dark:to-gray-900 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-gray-800 dark:text-white">
              Pre-Course Assessment
            </h1>
            <span className="text-gray-600 dark:text-gray-400">
              Question {currentQuestion + 1} of {questions.length}
            </span>
          </div>
          
          {/* Progress Bar */}
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* Question Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-6">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">
            {typeof question === 'string' ? question : question?.question}
          </h2>

          <div className="space-y-3">
            {["A", "B", "C", "D"].map((option) => {
              const optionText = typeof question === 'object' && question?.options 
                ? question.options[option] 
                : option;
              
              return (
                <button
                  key={option}
                  onClick={() => handleAnswerSelect(currentQuestion, option)}
                  className={`w-full p-4 rounded-xl text-left font-semibold transition-all ${
                    answers[currentQuestion] === option
                      ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg"
                      : "bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white hover:shadow-md"
                  }`}
                >
                  <span className="text-lg font-bold mr-3">{option}.</span>
                  <span className="text-base">{optionText}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex gap-4">
          <button
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            className="px-6 py-3 bg-gray-300 dark:bg-gray-700 text-gray-800 dark:text-white rounded-xl font-bold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          
          <div className="flex-1"></div>

          {currentQuestion < questions.length - 1 ? (
            <button
              onClick={handleNext}
              className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-bold hover:shadow-lg transform hover:scale-105 transition-all"
            >
              Next
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              className="px-8 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-bold hover:shadow-lg transform hover:scale-105 transition-all"
            >
              Submit Assessment
            </button>
          )}
        </div>

        {/* Question Navigator */}
        <div className="mt-6 bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
          <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">
            Question Navigator
          </h3>
          <div className="grid grid-cols-10 gap-2">
            {questions.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentQuestion(index)}
                className={`aspect-square rounded-lg font-bold transition-all ${
                  index === currentQuestion
                    ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white"
                    : answers[index]
                    ? "bg-green-500 text-white"
                    : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white"
                }`}
              >
                {index + 1}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Assessment;