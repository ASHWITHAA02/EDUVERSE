from database import engine
from sqlalchemy import text, inspect

inspector = inspect(engine)

print("Tables in database:")
for table_name in inspector.get_table_names():
    print(f"\n{table_name}:")
    columns = inspector.get_columns(table_name)
    for col in columns:
        nullable = "NULL" if col['nullable'] else "NOT NULL"
        print(f"  - {col['name']}: {col['type']} {nullable}")