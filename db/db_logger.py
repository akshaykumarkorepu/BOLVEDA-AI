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
def log_query(chat_id, question, answer, latency_ms):
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
            chat_id,
            question,
            answer,
            latency_ms,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            chat_id,
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


# Returns recent chat sessions
def get_recent_chats(limit=10):
    conn = get_connection()

    cursor = conn.cursor()

    # Fetch first question from each chat session
    cursor.execute(
        """
       SELECT
           q1.chat_id,
           q1.question,
           MAX(q1.timestamp)
       FROM queries q1
       WHERE q1.id = (
           SELECT MIN(q2.id)
           FROM queries q2
           WHERE q2.chat_id = q1.chat_id
       )
       GROUP BY q1.chat_id
       ORDER BY MAX(q1.timestamp) DESC
       LIMIT ?
       """,
        (limit,),
    )

    # Fetch all matching chat sessions
    rows = cursor.fetchall()

    conn.close()

    return rows


# Returns all messages from a specific chat session
def get_chat_messages(chat_id):
    conn = get_connection()

    cursor = conn.cursor()

    # Fetch all questions and answers from selected chat
    cursor.execute(
        """
        SELECT question, answer, timestamp
        FROM queries
        WHERE chat_id = ?
        ORDER BY timestamp ASC
        """,
        (chat_id,),
    )

    # Fetch all conversation rows
    rows = cursor.fetchall()

    conn.close()

    return rows


# Logs benchmark evaluation results into evaluation_results table
def log_evaluation_result(
    question,
    expected_answer,
    actual_answer,
    retrieved_chunks,
    similarity_score,
    is_correct,
    hallucination_detected,
    question_type,
    retrieval_time_ms,
    generation_time_ms,
    chunk_size,
    chunk_overlap,
):
    # Open database connection
    conn = get_connection()

    # Cursor executes SQL commands
    cursor = conn.cursor()

    # Current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert evaluation result into database
    cursor.execute(
        """
        INSERT INTO evaluation_results (
            question,
            expected_answer,
            actual_answer,
            retrieved_chunks,
            similarity_score,
            is_correct,
            hallucination_detected,
            question_type,
            retrieval_time_ms,
            generation_time_ms,
            chunk_size,
            chunk_overlap,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            question,
            expected_answer,
            actual_answer,
            retrieved_chunks,
            similarity_score,
            is_correct,
            hallucination_detected,
            question_type,
            retrieval_time_ms,
            generation_time_ms,
            chunk_size,
            chunk_overlap,
            timestamp,
        ),
    )

    # Save changes permanently
    conn.commit()

    # Close database connection safely
    conn.close()

    print(f"Evaluation logged: {question}")
