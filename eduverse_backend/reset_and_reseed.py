"""
Reset and Reseed Database Script
This script will drop all tables and recreate them with fresh seed data.
"""

from database import engine, Base
from seed_data import seed_database
import sys

def reset_database():
    """Drop all tables and recreate them"""
    try:
        print("⚠️  WARNING: This will delete ALL data in the database!")
        response = input("Are you sure you want to continue? (yes/no): ")
        
        if response.lower() != 'yes':
            print("❌ Operation cancelled.")
            sys.exit(0)
        
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
        print("\n🎉 You're all set! Start the server and enjoy!")
        
    except Exception as e:
        print(f"\n❌ Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_database()