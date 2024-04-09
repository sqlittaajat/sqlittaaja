from sqlittaaja.extractor import extract, zipped_file, find_init_scripts, student_info
from sqlittaaja.checker import init_database, copy_database
from sqlittaaja.printer import print_scores
import argparse


def main():
    args = read_args()
    student_scores = {}

    with args.answers as answers:
        extracted = extract(answers)
        exercise_name = "t" + str(args.exercise) + ".sql"
        # Try to find the exercise we are going to check.
        if exercise_name not in extracted:
            print(f"Exercise {args.exercise} not found")
            return

        # Get the correct answer for the exercise we are going to check.
        correct_answer = extracted[exercise_name]
        # Initialize the base database for everything.
        base_db = init_database(find_init_scripts(extracted))

        # Generate information for the correct answer.
        correct_rows = base_db.execute(correct_answer).fetchall()
        correct_dump = list(base_db.iterdump())

    with args.exercises as exercises:
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


def read_args():
    """Reads command line arguments."""

    parser = argparse.ArgumentParser(
        description="Check SQLite exercises", epilog="Created by TIKO"
    )

    parser.add_argument("answers", type=zipped_file, help="correct answers ZIP file")
    parser.add_argument("exercises", type=zipped_file, help="exercises ZIP file")
    parser.add_argument(
        "-e", "--exercise", type=int, default=1, help="check a specific exercise"
    )

    return parser.parse_args()
