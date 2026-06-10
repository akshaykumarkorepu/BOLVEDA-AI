import sqlite3

# Create/connect to SQLite database file
conn = sqlite3.connect("app.db")

# Cursor executes SQL commands
cursor = conn.cursor()

# Create documents table for storing uploaded PDF metadata
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    upload_time TEXT NOT NULL,
    chunk_count INTEGER NOT NULL
)
""")

# Create queries table for storing RAG interactions
cursor.execute("""
CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT NOT NULL,         
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    latency_ms REAL NOT NULL,
    timestamp TEXT NOT NULL
)
""")

# Create evaluation table for future RAG benchmarking/testing
cursor.execute("""
   CREATE TABLE IF NOT EXISTS evaluation_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    expected_answer TEXT NOT NULL,
    actual_answer TEXT NOT NULL,
    retrieved_chunks TEXT,
    similarity_score REAL,
    is_correct INTEGER NOT NULL,
    hallucination_detected INTEGER,
    question_type TEXT NOT NULL,
    retrieval_time_ms REAL,
    generation_time_ms REAL,
    chunk_size INTEGER,
    chunk_overlap INTEGER,
    created_at TEXT NOT NULL
)
""")

# Save all database changes permanently
conn.commit()
# Close database connection safely
conn.close()

print("Database and tables created successfully!")
