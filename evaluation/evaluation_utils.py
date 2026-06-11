import time
import string

from evaluation.evaluation_rag_pipeline import (
    process_evaluation_query,
)


def get_full_response(question):
    # Start timing
    start_time = time.time()

    full_response = ""

    retrieved_chunks = ""

    generation_time_ms = 0

    # Run streaming generator
    for chunk, metadata in process_evaluation_query(question):
        # Collect streamed chunks
        if chunk:
            full_response += chunk

        # Capture final metadata
        if metadata:
            retrieved_chunks = metadata.get("retrieved_chunks", "")

    # End timing
    end_time = time.time()

    # Convert seconds → milliseconds
    generation_time_ms = (end_time - start_time) * 1000

    return (
        full_response,
        generation_time_ms,
        retrieved_chunks,
    )


def evaluate_answer(expected, actual):
    # Prevent empty evaluation
    if not expected or not actual:
        return 0, 0

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

    # Prevent division by zero
    if len(expected_words) == 0:
        return 0, 0

    # Calculate overlap
    matched_words = expected_words.intersection(actual_words)

    similarity_score = len(matched_words) / len(expected_words)

    # Threshold for correctness
    if similarity_score >= 0.4:
        is_correct = 1
    else:
        is_correct = 0

    return similarity_score, is_correct


def detect_hallucination(actual_answer, retrieved_chunks):
    # Normalize text
    actual = actual_answer.lower()

    retrieved = retrieved_chunks.lower()

    # Split into words
    actual_words = set(actual.split())

    retrieved_words = set(retrieved.split())

    # Count overlap
    overlap = actual_words.intersection(retrieved_words)

    # Avoid division by zero
    if len(actual_words) == 0:
        return 0

    grounding_score = len(overlap) / len(actual_words)

    # Heuristic threshold
    if grounding_score < 0.30:
        return 1

    return 0
