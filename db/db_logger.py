import sqlite3
from datetime import datetime


def get_connection():
    return sqlite3.connect("app.db")


def log_document(filename, chunk_count):
    conn = get_connection()
    cursor = conn.cursor()

    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
    INSERT INTO documents (filename, upload_time, chunk_count)
    VALUES (?, ?, ?)
    """,
        (filename, upload_time, chunk_count),
    )

    conn.commit()
    conn.close()

    print(f"Document logged: {filename}")
