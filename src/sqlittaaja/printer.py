def print_scores(student_scores: dict[str, int], similarity_matrix: dict[tuple, str]):
    """Prints student scores and similarity ratios"""

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

    # Prints similarity percentages if over treshold.
    if similarity_matrix:
        file_col = "File name"
        diff_col = "Similarity ratio"
        # Determine the maximum width.
        max_file_len = max(
            max(len(key[0]), len(key[1])) for key in similarity_matrix.keys()
        )

        # Header part.
        print(f"┏━{'━' * max_file_len}━┳━{'━' * len(diff_col)}━┓")
        print(f"┃ {{:^{max_file_len}}} ┃ {{}} ┃".format(file_col, diff_col))
        print(f"┡━{'━' * max_file_len}━╇━{'━' * len(diff_col)}━┩")

        # Each row.
        for file_name, score in similarity_matrix.items():
            fmt = f"│ {{:<{max_file_len}}} │ {{:>{len(diff_col)}}} │"
            print(fmt.format(file_name[0], ""))
            print(fmt.format(file_name[1], score))
            print(f"├─{'─' * max_file_len}─┼─{'─' * len(diff_col)}─┤")
        print(f"└─{'─' * max_file_len}─┴─{'─' * len(diff_col)}─┘")
