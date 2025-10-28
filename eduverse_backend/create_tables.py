from database import engine, Base
from models import user, course, lesson, quiz, progress, badge, chat_message, leaderboard, quiz_attempt

def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

if __name__ == "__main__":
    create_tables()