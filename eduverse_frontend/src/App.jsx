import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useAuthStore } from "./store/authStore";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Courses from "./pages/Courses";
import Lessons from "./pages/Lessons";
import LessonDetail from "./pages/LessonDetail";
import Quiz from "./pages/Quiz";
import Leaderboard from "./pages/Leaderboard";
import Profile from "./pages/Profile";
import Games from "./pages/Games";
import GamePlay from "./pages/GamePlay";
import ResumeAnalyzer from "./pages/ResumeAnalyzer";
import Feedback from "./pages/Feedback";
import Assessment from "./pages/Assessment";
import Chatbot from "./components/Chatbot";

function App() {
  const { user } = useAuthStore();

  return (
    <Router>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/dashboard" />} />
          <Route path="/register" element={!user ? <Register /> : <Navigate to="/dashboard" />} />
          <Route path="/dashboard" element={user ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/lessons/:courseId" element={<Lessons />} />
          <Route path="/lesson/:lessonId" element={user ? <LessonDetail /> : <Navigate to="/login" />} />
          <Route path="/quiz/:quizId" element={user ? <Quiz /> : <Navigate to="/login" />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/profile" element={user ? <Profile /> : <Navigate to="/login" />} />
          <Route path="/games" element={user ? <Games /> : <Navigate to="/login" />} />
          <Route path="/game/:gameName" element={user ? <GamePlay /> : <Navigate to="/login" />} />
          <Route path="/resume" element={user ? <ResumeAnalyzer /> : <Navigate to="/login" />} />
          <Route path="/feedback" element={user ? <Feedback /> : <Navigate to="/login" />} />
          <Route path="/assessment/:courseId" element={user ? <Assessment /> : <Navigate to="/login" />} />
        </Routes>
        {user && <Chatbot />}
      </div>
    </Router>
  );
}

export default App;