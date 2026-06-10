import json

from evaluation.evaluation_utils import (
    get_full_response,
    evaluate_answer,
    detect_hallucination,
)

from db.db_logger import log_evaluation_result

# Load evaluation dataset
with open("evaluation/evaluation_dataset.json", "r") as f:
    dataset = json.load(f)

# Run evaluation questions
for item in dataset[:5]:
    question = item["question"]
    expected = item["expected_answer"]
    question_type = item["question_type"]

    print("=" * 60)
    print("QUESTION:", question)
    print("TYPE:", question_type)

    # Get actual RAG response + latency + retrieved chunks
    (
        actual_answer,
        generation_time_ms,
        retrieved_chunks,
    ) = get_full_response(question)

    # Evaluate answer quality
    similarity_score, is_correct = evaluate_answer(expected, actual_answer)

    # Detect possible hallucination
    hallucination_detected = detect_hallucination(actual_answer, retrieved_chunks)

    # Log full evaluation analytics
    log_evaluation_result(
        question=question,
        expected_answer=expected,
        actual_answer=actual_answer,
        retrieved_chunks=retrieved_chunks,
        similarity_score=similarity_score,
        is_correct=is_correct,
        hallucination_detected=hallucination_detected,
        question_type=question_type,
        retrieval_time_ms=0,
        generation_time_ms=generation_time_ms,
        chunk_size=1000,
        chunk_overlap=200,
    )

    print("\nEXPECTED ANSWER:")
    print(expected)

    print("\nACTUAL ANSWER:")
    print(actual_answer)

    print("\nEVALUATION RESULT:")

    if is_correct:
        print("✅ CORRECT")
    else:
        print("❌ INCORRECT")

    print("=" * 60)
