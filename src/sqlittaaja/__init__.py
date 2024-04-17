from sqlittaaja.printer import print_scores
from sqlittaaja.config import read_args, Config
from sqlittaaja.checker import check_exercises
from sqlittaaja.diff_check import compute_similarity
from sqlittaaja.extractor import extract


def main():
    args = read_args()
    # Type hint the configuration.
    config: Config = args.config

    exercises = extract(config.exercise_paths[0])
    student_scores = check_exercises(config.initialize_script, config.answer, exercises)
    answer_similarities = compute_similarity(config.threshold_pct, exercises)

    print_scores(student_scores, answer_similarities)
