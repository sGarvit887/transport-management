import sqlite3

def setup_database():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
       CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    dob TEXT NOT NULL,
    mobile TEXT NOT NULL,
    admission_number TEXT UNIQUE NOT NULL,
    pickup_location TEXT,
    drop_location TEXT
);

        
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")
