"""
Quick Reset and Reseed Database Script (No Confirmation)
"""

from database import engine, Base
from seed_data import seed_database
import sys

def reset_database():
    """Drop all tables and recreate them"""
    try:
        print("\n🗑️  Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped successfully!")
        
        print("\n📦 Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        print("\n🌱 Seeding database with fresh data...")
        seed_database()
        print("\n✅ Database reset and reseeded successfully!")
        print("\n📊 Your database now has:")
        print("   - 4 Courses (Python, React, Data Science, Machine Learning)")
        print("   - 14 Lessons (5 Python + 3 React + 3 Data Science + 3 ML)")
        print("   - 1 Quiz with 8 questions")
        print("   - 4 Badges")
        print("\n🎉 You're all set! Restart the server to see changes!")
        
    except Exception as e:
        print(f"\n❌ Error resetting database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    reset_database()