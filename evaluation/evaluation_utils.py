import string

import sqlite3

from src.rag.rag_pipeline import process_query


def get_full_response(question):
    full_response = ""

    # Run streaming generator
    for chunk, metadata in process_query(question):
        # Collect streamed text chunks
        if chunk:
            full_response += chunk

    return full_response


def evaluate_answer(expected, actual):
    # Common meaningless words
    stopwords = {
        "the",
        "is",
        "a",
        "an",
        "and",
        "of",
        "to",
        "with",
        "using",
        "that",
        "this",
        "it",
        "from",
        "into",
    }

    # Normalize text
    expected = expected.lower().translate(str.maketrans("", "", string.punctuation))

    actual = actual.lower().translate(str.maketrans("", "", string.punctuation))

    # Convert into meaningful word sets
    expected_words = {word for word in expected.split() if word not in stopwords}

    actual_words = {word for word in actual.split() if word not in stopwords}

    # Calculate overlap
    matched_words = expected_words.intersection(actual_words)

    score = len(matched_words) / len(expected_words)

    # Threshold
    if score >= 0.4:
        return 1
    else:
        return 0


def save_evaluation_result(
    expected_answer,
    actual_answer,
    is_correct,
    question_type,
):
    conn = sqlite3.connect("app.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO evaluation_results (
            expected_answer,
            actual_answer,
            is_correct,
            question_type
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            expected_answer,
            actual_answer,
            is_correct,
            question_type,
        ),
    )

    conn.commit()

    conn.close()
