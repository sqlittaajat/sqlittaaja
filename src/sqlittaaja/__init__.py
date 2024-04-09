from sqlittaaja.printer import print_scores
from sqlittaaja.config import read_args, validate_config
from sqlittaaja.checker import check_exercises
import tomllib


def main():
    args = read_args()

    config = tomllib.load(args.config)
    validate_config(config)

    student_scores = check_exercises(config)
    print_scores(student_scores)
