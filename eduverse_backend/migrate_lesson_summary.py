"""
Migration script to add ai_summary column to lessons table
"""
from sqlalchemy import text
from database import engine

def migrate():
    """Add ai_summary column to lessons table"""
    
    print("=" * 60)
    print("MIGRATING LESSON TABLE")
    print("=" * 60)
    
    with engine.connect() as conn:
        try:
            # Check if column already exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='lessons' AND column_name='ai_summary'
            """))
            
            if result.fetchone():
                print("✅ Column 'ai_summary' already exists in lessons table")
                return
            
            # Add the column
            print("Adding 'ai_summary' column to lessons table...")
            conn.execute(text("""
                ALTER TABLE lessons 
                ADD COLUMN ai_summary TEXT
            """))
            conn.commit()
            
            print("✅ Successfully added 'ai_summary' column to lessons table")
            print("\n" + "=" * 60)
            print("MIGRATION COMPLETE")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error during migration: {str(e)}")
            conn.rollback()
            raise

if __name__ == "__main__":
    migrate()