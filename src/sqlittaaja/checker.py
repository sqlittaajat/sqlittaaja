import sqlite3
import re
import difflib
from sqlittaaja.extractor import student_info
from typing import Any, List


def init_database(script: str) -> sqlite3.Connection:
    """Initialize a new SQLite database in memory."""

    db = sqlite3.connect(":memory:")
    db.executescript(script)
    return db


def copy_database(db: sqlite3.Connection) -> sqlite3.Connection:
    """Copy database and its contents into a new in-memory database."""

    new_db = sqlite3.connect(":memory:")
    db.backup(new_db)
    return new_db


def exec_fetch(db: sqlite3.Connection, script: str) -> List[Any]:
    """Execute many SQL statements and return results for each one combined."""

    result = []
    for statement in script.split(";"):
        result.extend(db.execute(statement).fetchall())
    return result


def check_exercises(
    init_script: str,
    answer: str,
    exercises: dict[str, str],
    must_contain: list[str],
    must_not_contain: list[str],
) -> dict[str, int]:
    """Check students' exercises."""

    student_scores = {}

    # Initialize the base database for everything.
    base_db = init_database(init_script)

    # Generate information for the correct answer.
    correct_db = copy_database(base_db)
    correct_rows = exec_fetch(correct_db, answer)
    correct_dump = list(correct_db.iterdump())

    # Go through each student one by one.
    for student_name, answer in [
        (student_info(key), exercises[key]) for key in exercises.keys()
    ]:
        student_scores[student_name] = 0
        answer = remove_dot_commands(answer)

        processed_answer = remove_extra_spaces(remove_sql_comments(answer)).lower()

        if not all(word.lower() in processed_answer for word in must_contain):
            continue

        if any(word.lower() in processed_answer for word in must_not_contain):
            continue

        # Copy the whole database just in case.
        db = copy_database(base_db)
        try:
            answer_rows = exec_fetch(db, answer)
            answer_dump = list(db.iterdump())
            # Compare results between student's answer and the correct one.
            if answer_rows == correct_rows and answer_dump == correct_dump:
                student_scores[student_name] += 1
        except Exception:
            print(f"Failed to run {student_name}'s answer")

    return student_scores


def remove_sql_comments(sql_string):
    """Removes SQLite comments. If the supposed comment is inside quotation marks, leaves it as is."""

    pattern = r"(([\"\'])(?:(?=(\\?))\3.)*?\2)|(--.*?$|\/\*[\s\S]*?\*\/)"
    # Group 1 catches all quotation marks so they can be left unchanged
    return re.sub(
        pattern,
        lambda m: m.group(1) if m.group(1) else "",
        sql_string,
        flags=re.MULTILINE,
    )


def remove_extra_spaces(string):
    """Removes extra spaces, tabs, newlines and carriage returns."""

    pattern = r" {2,}|\t+|\n+|\r+"
    return re.sub(pattern, " ", string, flags=re.UNICODE)


def remove_dot_commands(string):
    """Removes lines starting with . [dot] from a string."""
    lines = string.split("\n")
    kept_lines = [line for line in lines if not line.startswith('.')]
    return "\n".join(kept_lines)


def compute_similarity(
    treshold_pct: float, extracted: dict[str, str]
) -> dict[str, list[tuple[str, float]]]:
    """Check students' exercises."""

    result = {}

    # Go through each students file against other files.
    for file1, content1 in extracted.items():
        for file2, content2 in extracted.items():
            # Exclude self-comparisons.
            if file1 != file2:
                # Calculate the ratio of how similar the answers are.
                similarity_ratio = difflib.SequenceMatcher(
                    a=content1, b=content2
                ).ratio()

                if similarity_ratio >= treshold_pct:
                    student1 = student_info(file1)
                    student2 = student_info(file2)

                    # Append a new similarity to the result.
                    result[student1] = result.get(student1, []) + [
                        (student2, similarity_ratio)
                    ]

    return result
