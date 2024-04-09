def print_scores(student_scores: dict[str, int]):
    """Prints student scores."""

    name_col = "student name"
    score_col = "score"
    # Determine the maximum width.
    max_name_len = max(len(max(student_scores.keys(), key=len)), len(name_col))

    # Header part.
    print(f"┏━{'━' * max_name_len}━┳━{'━' * len(score_col)}━┓")
    print(f"┃ {{:^{max_name_len}}} ┃ {{}} ┃".format(name_col, score_col))
    print(f"┡━{'━' * max_name_len}━╇━{'━' * len(score_col)}━┩")

    # Each row.
    for student_name, score in student_scores.items():
        fmt = f"│ {{:<{max_name_len}}} │ {{:>{len(score_col)}}} │"
        print(fmt.format(student_name, score))
    print(f"└─{'─' * max_name_len}─┴─{'─' * len(score_col)}─┘")
