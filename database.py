import sqlite3

def init_db():
    conn = sqlite3.connect("fitness.db")
    c = conn.cursor()

    # Create table only once
    c.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hrv REAL,
        battery REAL,
        stress REAL,
        sleep REAL,
        goal TEXT,
        equipment TEXT,
        workout TEXT
    );
    """)

    conn.commit()
    conn.close()
    print("✅ fitness.db initialized.")

if __name__ == "__main__":
    init_db()
