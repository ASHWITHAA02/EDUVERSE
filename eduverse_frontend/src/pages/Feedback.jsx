import { useState, useEffect } from "react";
import api from "../services/api";
import { FaStar, FaTrash, FaPaperPlane } from "react-icons/fa";

const Feedback = () => {
  const [feedbacks, setFeedbacks] = useState([]);
  const [category, setCategory] = useState("general");
  const [rating, setRating] = useState(5);
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMyFeedback();
  }, []);

  const fetchMyFeedback = async () => {
    try {
      const response = await api.get("/feedback/my-feedback");
      setFeedbacks(response.data);
    } catch (err) {
      console.error("Error fetching feedback:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!message.trim()) {
      alert("Please enter your feedback message");
      return;
    }

    setSubmitting(true);
    try {
      await api.post("/feedback/submit", {
        category,
        rating,
        message: message.trim(),
      });
      
      alert("Thank you for your feedback! 🎉");
      setMessage("");
      setCategory("general");
      setRating(5);
      fetchMyFeedback();
    } catch (err) {
      console.error("Error submitting feedback:", err);
      alert("Failed to submit feedback. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (feedbackId) => {
    if (!confirm("Delete this feedback?")) return;

    try {
      await api.delete(`/feedback/${feedbackId}`);
      fetchMyFeedback();
    } catch (err) {
      console.error("Error deleting feedback:", err);
      alert("Failed to delete feedback");
    }
  };

  const getCategoryColor = (cat) => {
    const colors = {
      bug: "bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200",
      feature: "bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200",
      improvement: "bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200",
      general: "bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200",
    };
    return colors[cat] || colors.general;
  };

  const getCategoryIcon = (cat) => {
    const icons = {
      bug: "🐛",
      feature: "✨",
      improvement: "💡",
      general: "💬",
    };
    return icons[cat] || icons.general;
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
          <h1 className="text-5xl font-bold text-gray-800 dark:text-white mb-4">
            💬 Feedback
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Help us improve EduVerse with your feedback
          </p>
        </div>

        {/* Feedback Form */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">
            Submit Feedback
          </h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Category */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Category
              </label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {["bug", "feature", "improvement", "general"].map((cat) => (
                  <button
                    key={cat}
                    type="button"
                    onClick={() => setCategory(cat)}
                    className={`p-3 rounded-lg font-semibold transition-all ${
                      category === cat
                        ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg"
                        : "bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white hover:shadow-md"
                    }`}
                  >
                    {getCategoryIcon(cat)} {cat.charAt(0).toUpperCase() + cat.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {/* Rating */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Rating
              </label>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    className="text-4xl transition-all transform hover:scale-110"
                  >
                    <FaStar
                      className={star <= rating ? "text-yellow-500" : "text-gray-300 dark:text-gray-600"}
                    />
                  </button>
                ))}
                <span className="ml-4 text-2xl font-bold text-gray-800 dark:text-white">
                  {rating}/5
                </span>
              </div>
            </div>

            {/* Message */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Your Feedback
              </label>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="w-full h-32 p-4 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:border-blue-500 focus:outline-none bg-white dark:bg-gray-700 text-gray-800 dark:text-white"
                placeholder="Tell us what you think..."
                required
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 rounded-xl font-bold text-lg hover:shadow-lg transform hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? "Submitting..." : (
                <>
                  <FaPaperPlane className="inline mr-2" />
                  Submit Feedback
                </>
              )}
            </button>
          </form>
        </div>

        {/* My Feedback */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">
            My Feedback History
          </h2>
          
          <div className="space-y-4">
            {feedbacks.map((feedback) => (
              <div
                key={feedback.id}
                className="border-2 border-gray-200 dark:border-gray-700 rounded-xl p-6 hover:shadow-lg transition-all"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getCategoryColor(feedback.category)}`}>
                      {getCategoryIcon(feedback.category)} {feedback.category}
                    </span>
                    <div className="flex gap-1">
                      {[...Array(5)].map((_, i) => (
                        <FaStar
                          key={i}
                          className={`text-sm ${
                            i < feedback.rating ? "text-yellow-500" : "text-gray-300 dark:text-gray-600"
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                  <button
                    onClick={() => handleDelete(feedback.id)}
                    className="text-red-500 hover:text-red-700 p-2"
                  >
                    <FaTrash />
                  </button>
                </div>
                
                <p className="text-gray-800 dark:text-white mb-3">
                  {feedback.message}
                </p>
                
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Submitted on {new Date(feedback.created_at).toLocaleDateString()} at{" "}
                  {new Date(feedback.created_at).toLocaleTimeString()}
                </p>
              </div>
            ))}
            
            {feedbacks.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-500 dark:text-gray-400 text-lg">
                  No feedback submitted yet
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Feedback;