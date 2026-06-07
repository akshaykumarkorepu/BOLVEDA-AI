import sqlite3
from datetime import datetime


# Creates and returns a connection to app.db
def get_connection():
    return sqlite3.connect("app.db")


# Logs uploaded PDF metadata into the documents table
def log_document(filename, chunk_count):
    # Open database connection
    conn = get_connection()

    # Cursor executes SQL commands
    cursor = conn.cursor()

    # Generate current timestamp
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert document data into SQLite table
    cursor.execute(
        """
    INSERT INTO documents (filename, upload_time, chunk_count)
    VALUES (?, ?, ?)
    """,
        (filename, upload_time, chunk_count),
    )

    # Save changes permanently
    conn.commit()
    # Close database connection safely
    conn.close()

    print(f"Document logged: {filename}")


# Logs user queries and AI responses into the queries table
def log_query(document_id, question, answer, latency_ms):
    # Open database connection
    conn = get_connection()

    # Cursor executes SQL commands
    cursor = conn.cursor()

    # Generate current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert query data into SQLite table
    cursor.execute(
        """
        INSERT INTO queries (
            document_id,
            question,
            answer,
            latency_ms,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            document_id,
            question,
            answer,
            latency_ms,
            timestamp,
        ),
    )

    # Save changes permanently
    conn.commit()

    # Close database connection safely
    conn.close()

    print(f"Query logged: {question}")
