import json

from evaluation.evaluation_utils import (
    get_full_response,
    evaluate_answer,
    save_evaluation_result,
)

# Load evaluation dataset
with open("evaluation/evaluation_dataset.json", "r") as f:
    dataset = json.load(f)

# Run evaluation questions
for item in dataset:
    question = item["question"]
    expected = item["expected_answer"]
    question_type = item["question_type"]

    print("=" * 60)
    print("QUESTION:", question)
    print("TYPE:", question_type)

    # Get actual RAG response
    actual_answer = get_full_response(question)

    # Evaluate correctness
    is_correct = evaluate_answer(expected, actual_answer)

    # Save evaluation result into SQLite
    save_evaluation_result(
        expected,
        actual_answer,
        is_correct,
        question_type,
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
