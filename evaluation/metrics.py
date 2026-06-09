import sqlite3

# Connect to database
conn = sqlite3.connect("app.db")

cursor = conn.cursor()

# Calculate overall accuracy
cursor.execute(
    """
    SELECT ROUND(
        100.0 * SUM(is_correct) / COUNT(*),
        2
    )
    FROM evaluation_results
"""
)

accuracy = cursor.fetchone()[0]

print("\n📊 OVERALL ACCURACY")
print(f"Accuracy: {accuracy}%")

# CATEGORY WISE ACCURACY
print("\n📊 CATEGORY-WISE ACCURACY")

cursor.execute(
    """
    SELECT
        question_type,
        ROUND(
            100.0 * SUM(is_correct) / COUNT(*),
            2
        ) AS accuracy
    FROM evaluation_results
    GROUP BY question_type
"""
)

results = cursor.fetchall()

for row in results:
    question_type = row[0]
    accuracy = row[1]

    print(f"{question_type}: {accuracy}%")

# Close DB connection
conn.close()
