# 🎓 EduVerse - AI-Powered Learning Platform

An intelligent e-learning platform with AI chatbot assistance, adaptive learning, gamification, and comprehensive course content.

## ✨ Features

- 🤖 **AI Chatbot** - Context-aware assistant using Google Gemini AI
- 📚 **Rich Course Content** - 5 comprehensive Python lessons (200-400 lines each)
- 🎥 **Video Integration** - YouTube videos embedded in all lessons
- ✅ **Progress Tracking** - Mark lessons as complete, track your journey
- 🎯 **Interactive Quizzes** - 8 questions with instant feedback
- 🏆 **Gamification** - Earn badges and achievements
- 📊 **Adaptive Learning** - Personalized learning paths
- 🔐 **User Authentication** - Secure registration and login

## 🚀 Getting Started

### Choose Your Path:

#### 🏠 Run Locally (Development/Personal Use)
```powershell
cd "C:\Users\Ashwithaa SK\Desktop\EduVerse"
.\start_project.ps1
```
Then visit: http://localhost:5173

📖 **Full Guide:** [HOW_TO_RUN_LOCALLY.md](HOW_TO_RUN_LOCALLY.md)

#### ☁️ Deploy to Cloud (Production)
Deploy to ByteXL.app for public access

📖 **Full Guide:** [BYTEXL_DEPLOYMENT.md](BYTEXL_DEPLOYMENT.md)

## 📋 Quick Reference

| What | Where |
|------|-------|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Database** | PostgreSQL (localhost:5432) |

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **Google Gemini AI** - AI chatbot integration
- **JWT** - Secure authentication

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **React Router** - Navigation
- **Axios** - HTTP client

## 📁 Project Structure

```
EduVerse/
├── eduverse_backend/          # FastAPI backend
│   ├── routes/               # API endpoints
│   ├── models/               # Database models
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # Business logic
│   ├── main.py              # Application entry
│   ├── database.py          # Database config
│   ├── create_tables.py     # Create DB tables
│   ├── seed_data.py         # Seed initial data
│   └── .env                 # Environment variables
│
├── eduverse_frontend/         # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── App.jsx          # Main app component
│   └── package.json
│
└── Documentation/
    ├── QUICK_START.md           # Quick start guide
    ├── HOW_TO_RUN_LOCALLY.md    # Local setup guide
    ├── BYTEXL_DEPLOYMENT.md     # ByteXL deployment
    ├── DEPLOYMENT_GUIDE.md      # General deployment
    └── SETUP_INSTRUCTIONS.md    # Initial setup
```

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Start here!
- **[HOW_TO_RUN_LOCALLY.md](HOW_TO_RUN_LOCALLY.md)** - Run on your computer
- **[BYTEXL_DEPLOYMENT.md](BYTEXL_DEPLOYMENT.md)** - Deploy to ByteXL.app
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - General deployment info
- **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Initial setup steps

## 🎯 Course Content

### Python Programming Course
1. **Introduction to Python** (200+ lines)
   - History, features, installation, first program
   - YouTube tutorial included

2. **Data Types and Variables** (300+ lines)
   - Numbers, strings, lists, dictionaries, type conversion
   - YouTube tutorial included

3. **Control Flow** (400+ lines)
   - If statements, loops, break/continue, nested structures
   - YouTube tutorial included

4. **Functions and Modules** (350+ lines)
   - Function definition, parameters, return values, modules
   - YouTube tutorial included

5. **Object-Oriented Programming** (400+ lines)
   - Classes, objects, inheritance, polymorphism
   - YouTube tutorial included

### Quiz
- 8 comprehensive questions
- 4 options per question
- Instant feedback
- Score tracking

## 🔧 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/eduverse
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GEMINI_API_KEY=your-gemini-api-key
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

## 🧪 Testing

### Test Locally
1. Start the application: `.\start_project.ps1`
2. Visit http://localhost:5173
3. Register a new account
4. Browse courses and lessons
5. Test AI chatbot
6. Complete a lesson
7. Take the quiz

### Test API
Visit http://localhost:8000/docs for interactive API documentation

## 🐛 Troubleshooting

### Port Already in Use
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- Verify database exists

### Frontend Can't Connect
- Ensure backend is running on port 8000
- Check CORS settings in main.py
- Verify API_URL in frontend

See documentation files for more troubleshooting tips.

## 📊 Database Schema

- **Users** - User accounts and authentication
- **Courses** - Course information
- **Lessons** - Lesson content with YouTube videos
- **Quizzes** - Quiz questions and options
- **Progress** - User progress tracking
- **Badges** - Gamification achievements
- **Chat** - AI chatbot conversation history

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Environment variable protection
- SQL injection prevention (SQLAlchemy ORM)

## 🚀 Deployment Options

1. **Local Development** - Run on your machine
2. **ByteXL.app** - Cloud deployment (recommended)
3. **Docker** - Containerized deployment
4. **Traditional Hosting** - VPS/dedicated server

## 📞 Support

- Check documentation files first
- Review API docs at /docs endpoint
- Check application logs
- Test locally before deploying

## 📝 License

This project is for educational purposes.

## 🎉 Credits

- **Backend:** FastAPI, SQLAlchemy, Google Gemini AI
- **Frontend:** React, Vite
- **Database:** PostgreSQL
- **AI:** Google Gemini API

---

**Ready to learn? Start with [QUICK_START.md](QUICK_START.md)! 🚀**