import sqlite3
from typing import Any
from zipfile import ZipFile
from sqlittaaja.extractor import extract, student_info


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


def check_exercises(config: dict[str, Any]) -> dict[str, int]:
    """Check students' exercises."""

    student_scores = {}

    # Initialize the base database for everything.
    base_db = init_database(config["answer"].get("initialize", ""))

    # Generate information for the correct answer.
    correct_rows = base_db.execute(config["answer"]["exercise"]).fetchall()
    correct_dump = list(base_db.iterdump())

    with ZipFile(config["exercise"]["path"], "r") as exercises:
        extracted = extract(exercises)
        # Go through each student one by one.
        for info in [(student_info(key), extracted[key]) for key in extracted.keys()]:
            student_name = info[0][0]
            answer = info[1]

            student_scores[student_name] = 0

            # Copy the whole database just in case.
            db = copy_database(base_db)
            try:
                answer_rows = db.execute(answer).fetchall()
                answer_dump = list(db.iterdump())
                # Compare results between student's answer and the correct one.
                if answer_rows == correct_rows and answer_dump == correct_dump:
                    student_scores[student_name] += 1
            except Exception:
                print(f"Failed to run {student_name}'s answer")

    return student_scores
