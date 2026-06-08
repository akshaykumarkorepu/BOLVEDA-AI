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


# Returns total number of queries stored in the database
def get_total_queries():
    conn = get_connection()
    cursor = conn.cursor()

    # Count all rows inside queries table
    cursor.execute("SELECT COUNT(*) FROM queries")

    # Fetch first value from SQL result
    total = cursor.fetchone()[0]

    conn.close()

    return total


# Returns total uploaded documents
def get_total_documents():
    conn = get_connection()
    cursor = conn.cursor()

    # Count all rows inside documents table
    cursor.execute("SELECT COUNT(*) FROM documents")

    # Fetch first value from SQL result
    total = cursor.fetchone()[0]

    conn.close()

    return total


# Returns average query latency
def get_avg_latency():
    conn = get_connection()
    cursor = conn.cursor()

    # Calculate average latency from queries table
    cursor.execute("SELECT AVG(latency_ms) FROM queries")

    # Fetch average latency value
    avg = cursor.fetchone()[0]

    conn.close()

    return avg if avg else 0


# Returns recent query history
def get_recent_queries(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch latest questions and answers
    cursor.execute(
        """
        SELECT question, answer, timestamp
        FROM queries
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (limit,),
    )

    # Fetch all matching rows
    rows = cursor.fetchall()

    conn.close()

    return rows
