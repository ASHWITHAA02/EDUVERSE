from sqlalchemy import text
from database import SessionLocal, engine
from seed_data import seed_database

def reset_and_seed():
    """Drop all data and reseed the database"""
    db = SessionLocal()
    
    try:
        print("Dropping all existing data...")
        
        # Delete all data in correct order (respecting foreign keys)
        db.execute(text("DELETE FROM chat_messages"))
        db.execute(text("DELETE FROM quiz_attempts"))
        db.execute(text("DELETE FROM lesson_progress"))
        db.execute(text("DELETE FROM quiz_options"))
        db.execute(text("DELETE FROM quiz_questions"))
        db.execute(text("DELETE FROM quizzes"))
        db.execute(text("DELETE FROM lessons"))
        db.execute(text("DELETE FROM courses"))
        db.execute(text("DELETE FROM badges"))
        db.execute(text("DELETE FROM users"))
        
        db.commit()
        print("✅ All data cleared!")
        
    except Exception as e:
        print(f"Error clearing data: {e}")
        db.rollback()
    finally:
        db.close()
    
    # Now seed with new data
    print("\nSeeding database with enhanced content...")
    seed_database()

if __name__ == "__main__":
    reset_and_seed()