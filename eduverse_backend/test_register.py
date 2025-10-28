from database import get_db
from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_registration():
    db = next(get_db())
    
    try:
        # Check if user exists
        existing = db.query(User).filter(User.email == "testuser@example.com").first()
        if existing:
            print(f"User already exists: {existing.username}")
            db.delete(existing)
            db.commit()
            print("Deleted existing user")
        
        # Create new user
        hashed_password = pwd_context.hash("password123")
        new_user = User(
            username="testuser",
            email="testuser@example.com",
            hashed_password=hashed_password,
            full_name="Test User"
        )
        
        print(f"Creating user: {new_user.username}")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"✅ User created successfully!")
        print(f"   ID: {new_user.id}")
        print(f"   Username: {new_user.username}")
        print(f"   Email: {new_user.email}")
        print(f"   Full Name: {new_user.full_name}")
        print(f"   Total XP: {new_user.total_xp}")
        print(f"   Level: {new_user.level}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_registration()