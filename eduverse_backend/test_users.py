from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text('SELECT id, username, email, created_at FROM users ORDER BY id DESC LIMIT 5'))
    users = result.fetchall()
    
    if users:
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Created: {user[3]}")
    else:
        print("No users found in database")