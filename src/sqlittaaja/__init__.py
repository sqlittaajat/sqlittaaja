from sqlittaaja.extractor import extract, student_info
from sqlittaaja.checker import init_database, copy_database
from sqlittaaja.printer import print_scores
from sqlittaaja.config import read_args, validate_config
import tomllib
from zipfile import ZipFile


def main():
    args = read_args()
    student_scores = {}

    config = tomllib.load(args.config)
    validate_config(config)

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

            # Copy the whole database just in case.
            db = copy_database(base_db)
            try:
                answer_rows = db.execute(answer).fetchall()
                answer_dump = list(db.iterdump())
                # Compare results between student's answer and the correct one.
                if answer_rows == correct_rows and answer_dump == correct_dump:
                    student_scores[student_name] = (
                        student_scores.get(student_name, 0) + 1
                    )
                else:
                    raise Exception("Incorrect")
            except Exception:
                print(f"Incorrect answer for {student_name}")
                student_scores[student_name] = student_scores.get(student_name, 0) + 0

    print_scores(student_scores)
