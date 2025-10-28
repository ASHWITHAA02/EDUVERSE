from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import (
    auth, 
    courses, 
    lesson_routes, 
    quiz_routes, 
    progress_routes, 
    gamification_routes, 
    chatbot_routes, 
    adaptive_learning_routes, 
    quiz_submission,
    feedback_routes,
    resume_routes,
    assessment_routes,
    games_routes
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduVerse API", version="1.0.0")

# CORS Configuration
# Add your ByteXL frontend URL here when deploying
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        # Add your ByteXL URLs here:
        # "https://bytexl.app/nimbus/43zegqard",
        # "https://*.bytexl.app",  # Allow all ByteXL subdomains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(lesson_routes.router, prefix="/api/lessons", tags=["Lessons"])
app.include_router(quiz_routes.router, prefix="/api/quizzes", tags=["Quizzes"])
app.include_router(quiz_submission.router, prefix="/api/quiz-submissions", tags=["Quiz Submissions"])
app.include_router(progress_routes.router, prefix="/api/progress", tags=["Progress"])
app.include_router(gamification_routes.router, prefix="/api/gamification", tags=["Gamification"])
app.include_router(chatbot_routes.router, prefix="/api/chatbot", tags=["AI Chatbot"])
app.include_router(adaptive_learning_routes.router, prefix="/api/adaptive", tags=["Adaptive Learning"])

# New Feature Routers
app.include_router(feedback_routes.router, prefix="/api/feedback", tags=["User Feedback"])
app.include_router(resume_routes.router, prefix="/api/resume", tags=["Resume Analyzer"])
app.include_router(assessment_routes.router, prefix="/api/assessment", tags=["Pre-Course Assessment"])
app.include_router(games_routes.router, prefix="/api/games", tags=["Educational Games"])

@app.get("/")
def read_root():
    return {"message": "Welcome to EduVerse API! 🎓"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}