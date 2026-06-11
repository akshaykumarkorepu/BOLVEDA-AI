import sqlite3
from datetime import datetime


# Creates and returns a connection to app.db
def get_connection():
    return sqlite3.connect("app.db")


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
            generation_time_ms,
            chunk_size,
            chunk_overlap,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
