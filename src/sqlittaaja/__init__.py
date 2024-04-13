from sqlittaaja.printer import print_scores
from sqlittaaja.config import read_args, validate_config
from sqlittaaja.checker import check_exercises
from sqlittaaja.diff_check import compute_similarity
from sqlittaaja.extractor import extract
import tomllib


def main():
    args = read_args()

    config = tomllib.load(args.config)
    validate_config(config)

    init_script = config["answer"].get("initialize", "")
    answer = config["answer"]["exercise"]
    exercises = extract(config["exercise"]["path"])
    # Treshold default 90% if not in config.toml
    treshold_pct = config["check_options"].get("treshold_pct", 0.9)

    student_scores = check_exercises(init_script, answer, exercises)
    answer_similarities = compute_similarity(treshold_pct, exercises)

    print_scores(student_scores, answer_similarities)
