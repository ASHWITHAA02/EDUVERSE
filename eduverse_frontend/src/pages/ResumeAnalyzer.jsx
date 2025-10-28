import { useState, useEffect } from "react";
import api from "../services/api";
import { FaUpload, FaFileAlt, FaTrash, FaChartBar } from "react-icons/fa";

const ResumeAnalyzer = () => {
  const [analyses, setAnalyses] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalyses();
  }, []);

  const fetchAnalyses = async () => {
    try {
      const response = await api.get("/resume/my-analyses");
      setAnalyses(response.data);
    } catch (err) {
      console.error("Error fetching analyses:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      setSelectedFile(file);
    } else {
      alert("Please select a PDF file");
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await api.post("/resume/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      
      alert("Resume analyzed successfully!");
      setSelectedFile(null);
      setSelectedAnalysis(response.data);
      fetchAnalyses();
    } catch (err) {
      console.error("Error uploading resume:", err);
      alert("Failed to analyze resume. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (analysisId) => {
    if (!confirm("Delete this analysis?")) return;

    try {
      await api.delete(`/resume/${analysisId}`);
      fetchAnalyses();
      if (selectedAnalysis?.id === analysisId) {
        setSelectedAnalysis(null);
      }
    } catch (err) {
      console.error("Error deleting analysis:", err);
      alert("Failed to delete analysis");
    }
  };

  const viewAnalysis = async (analysisId) => {
    try {
      const response = await api.get(`/resume/${analysisId}`);
      setSelectedAnalysis(response.data);
    } catch (err) {
      console.error("Error fetching analysis:", err);
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
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-800 dark:text-white mb-4">
            📄 AI Resume Analyzer
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Get AI-powered insights on your resume
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Upload Section */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 mb-6">
              <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">
                Upload Resume
              </h2>
              
              <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-8 text-center mb-4">
                <FaUpload className="text-5xl text-gray-400 mx-auto mb-4" />
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="resume-upload"
                />
                <label
                  htmlFor="resume-upload"
                  className="cursor-pointer bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-all inline-block"
                >
                  Choose PDF File
                </label>
                {selectedFile && (
                  <p className="mt-4 text-gray-600 dark:text-gray-400">
                    Selected: {selectedFile.name}
                  </p>
                )}
              </div>

              <button
                onClick={handleUpload}
                disabled={!selectedFile || uploading}
                className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-xl font-bold hover:shadow-lg transform hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {uploading ? "Analyzing..." : "Analyze Resume"}
              </button>
            </div>

            {/* Previous Analyses */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
              <h2 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
                Previous Analyses
              </h2>
              <div className="space-y-3">
                {analyses.map((analysis) => (
                  <div
                    key={analysis.id}
                    className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg hover:shadow-md transition-all"
                  >
                    <div
                      className="flex-1 cursor-pointer"
                      onClick={() => viewAnalysis(analysis.id)}
                    >
                      <p className="font-semibold text-gray-800 dark:text-white">
                        Analysis #{analysis.id}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {new Date(analysis.analyzed_at).toLocaleDateString()}
                      </p>
                      <p className="text-sm font-bold text-blue-600 dark:text-blue-400">
                        Score: {analysis.overall_score}/100
                      </p>
                    </div>
                    <button
                      onClick={() => handleDelete(analysis.id)}
                      className="text-red-500 hover:text-red-700 p-2"
                    >
                      <FaTrash />
                    </button>
                  </div>
                ))}
                {analyses.length === 0 && (
                  <p className="text-center text-gray-500 dark:text-gray-400 py-4">
                    No analyses yet
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Analysis Results */}
          <div className="lg:col-span-2">
            {selectedAnalysis ? (
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
                <h2 className="text-3xl font-bold text-gray-800 dark:text-white mb-6">
                  Analysis Results
                </h2>

                {/* Overall Score */}
                <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl p-6 mb-6 text-center">
                  <p className="text-lg mb-2">Overall Score</p>
                  <p className="text-6xl font-bold">{selectedAnalysis.overall_score}</p>
                  <p className="text-xl mt-2">out of 100</p>
                </div>

                {/* Skills Found */}
                <div className="mb-6">
                  <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-3 flex items-center gap-2">
                    ✅ Skills Found
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedAnalysis.skills_found.map((skill, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full text-sm font-semibold"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Skills Missing */}
                <div className="mb-6">
                  <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-3 flex items-center gap-2">
                    ⚠️ Skills to Add
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedAnalysis.skills_missing.map((skill, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 rounded-full text-sm font-semibold"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Job Titles */}
                <div className="mb-6">
                  <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-3 flex items-center gap-2">
                    💼 Suggested Job Titles
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {selectedAnalysis.job_titles.map((title, index) => (
                      <div
                        key={index}
                        className="p-3 bg-blue-50 dark:bg-blue-900 rounded-lg"
                      >
                        <p className="font-semibold text-gray-800 dark:text-white">
                          {title}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Improvements */}
                <div>
                  <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-3 flex items-center gap-2">
                    💡 Improvement Suggestions
                  </h3>
                  <div className="space-y-3">
                    {selectedAnalysis.improvements.map((improvement, index) => (
                      <div
                        key={index}
                        className="p-4 bg-purple-50 dark:bg-purple-900 rounded-lg"
                      >
                        <p className="text-gray-800 dark:text-white">
                          {index + 1}. {improvement}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-12 text-center">
                <FaFileAlt className="text-6xl text-gray-400 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">
                  No Analysis Selected
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Upload a resume or select a previous analysis to view results
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeAnalyzer;