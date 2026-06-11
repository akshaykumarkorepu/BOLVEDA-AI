import sqlite3

# Create/connect to SQLite database file
conn = sqlite3.connect("app.db")

# Cursor executes SQL commands
cursor = conn.cursor()

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
