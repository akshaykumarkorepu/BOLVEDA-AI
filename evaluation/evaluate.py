import json

from evaluation.build_evaluation_db import build

from evaluation.evaluation_utils import (
    get_full_response,
    evaluate_answer,
    detect_hallucination,
)

from db.db_logger import log_evaluation_result

# Build fresh evaluation database
build()

# Load evaluation dataset safely
try:
    with open(
        "evaluation/evaluation_dataset.json",
        "r",
    ) as f:
        dataset = json.load(f)

except Exception:
    print("Failed to load evaluation dataset.")

    exit()


# Prevent empty evaluation dataset
if not dataset:
    print("No evaluation data found.")

    exit()


# Track total correct answers
correct_answers = 0


# Run evaluation questions
for item in dataset:
    try:
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

        # Track correct answers
        if is_correct:
            correct_answers += 1

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

    except Exception as e:
        print(f"Evaluation failed: {e}")


# Final evaluation summary
print("\nFINAL RESULTS")

print(f"Correct Answers: {correct_answers}/{len(dataset)}")
