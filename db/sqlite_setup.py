import sqlite3

conn = sqlite3.connect("app.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    upload_time TEXT NOT NULL,
    chunk_count INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    latency_ms REAL NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES documents(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS evaluation_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_id INTEGER,
    expected_answer TEXT NOT NULL,
    actual_answer TEXT NOT NULL,
    is_correct INTEGER NOT NULL,
    FOREIGN KEY (query_id) REFERENCES queries(id)
)
""")

conn.commit()

conn.close()

print("Database and tables created successfully!")
