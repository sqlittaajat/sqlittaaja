from sqlittaaja.printer import print_scores
from sqlittaaja.config import read_args, validate_config
from sqlittaaja.checker import check_exercises
from sqlittaaja.diff_check import compute_similarity
import tomllib


def main():
    args = read_args()

    config = tomllib.load(args.config)
    validate_config(config)

    student_scores = check_exercises(config)

    diff_check = compute_similarity(config)

    print_scores(student_scores, diff_check)
