from sqlittaaja.printer import print_scores
from sqlittaaja.config import read_args
from sqlittaaja.checker import check_exercises
from sqlittaaja.diff_check import compute_similarity
from sqlittaaja.extractor import extract


def main():
    config = read_args()

    total_scores: dict[str, int] = {}

    for path in config.exercise_paths:
        exercises = extract(path)
        student_scores = check_exercises(
            config.initialize_script, config.answer, exercises
        )
        answer_similarities = compute_similarity(config.threshold_pct, exercises)

        # Add the score in order to accumulate overall score for each student.
        for student_name, score in student_scores.items():
            total_scores[student_name] = total_scores.get(student_name, 0) + score

        # Print scores for each individual exercise packet.
        print(f"Scores for '{path}'")
        print_scores(student_scores, answer_similarities)
        print()

    # Print the final scores for each student.
    print("Total scores")
    print_scores(total_scores, max_score=len(config.exercise_paths))
