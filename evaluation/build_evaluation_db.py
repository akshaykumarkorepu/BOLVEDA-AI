import shutil
import os

from evaluation.evaluation_ingest import build_evaluation_db

EVALUATION_DB_PATH = "evaluation/evaluation_chroma_db"


def build():
    # Remove old benchmark database
    if os.path.exists(EVALUATION_DB_PATH):
        shutil.rmtree(EVALUATION_DB_PATH)

    os.makedirs(EVALUATION_DB_PATH, exist_ok=True)

    # Build fresh benchmark database
    build_evaluation_db("evaluation/benchmark_pdf.pdf")

    print("Evaluation database ready.")


if __name__ == "__main__":
    build()
