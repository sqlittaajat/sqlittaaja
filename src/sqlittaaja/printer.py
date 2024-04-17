def print_scores(
    student_scores: dict[str, int],
    answer_similarities: dict[str, list[tuple[str, float]]] = {},
):
    """Prints student scores and similarity ratios"""

    if answer_similarities:
        print_table(
            [["Student Name", "Score", "Similarity"]]
            + [
                [
                    student_name,
                    str(score),
                    # Show similarity for each student.
                    "\n".join(
                        f"{similarity[0]} ({str(round(similarity[1] * 100, 2))}%)"
                        for similarity in answer_similarities.get(student_name, [])
                    ),
                ]
                for student_name, score in student_scores.items()
            ],
            separators=True,
        )
    else:
        print_table(
            [["Student Name", "Score"]]
            + [
                [student_name, str(score)]
                for student_name, score in student_scores.items()
            ],
        )


def print_table(table: list[list[str]], separators: bool = False):
    """Print a table with pretty formatting."""

    max_column_lens = [
        # Calculate maximum length for each column.
        max(
            [
                len(max(table[j][i].splitlines(), key=len, default=""))
                for j, _ in enumerate(table)
            ]
        )
        for i, _ in enumerate(table[0])
    ]

    # Print header part.
    print("┏━" + "━┳━".join(["━" * max_len for max_len in max_column_lens]) + "━┓")
    print(
        "┃ "
        + " ┃ ".join(
            [title.ljust(max_column_lens[i]) for i, title in enumerate(table[0])]
        )
        + " ┃"
    )
    print("┡━" + "━╇━".join(["━" * max_len for max_len in max_column_lens]) + "━┩")

    # Print each row one-by-one.
    for i, row in enumerate(table[1:]):
        actual_rows = []
        for j, field in enumerate(row):
            # Go through each line for each field.
            for k, line in enumerate(field.splitlines()):
                if k >= len(actual_rows):
                    # Add a new empty row if we have more lines.
                    actual_rows.append([""] * len(row))
                # Set the value for the field on this line (row) or keep the default.
                actual_rows[k][j] = line

        # Print each line (row).
        for actual_row in actual_rows:
            print(
                "│ "
                + " │ ".join(
                    [
                        value.ljust(max_column_lens[j])
                        for j, value in enumerate(actual_row)
                    ]
                )
                + " │"
            )
        if separators and i + 1 < len(table) - 1:
            print(
                "├─" + "─┼─".join(["─" * max_len for max_len in max_column_lens]) + "─┤"
            )
    print("└─" + "─┴─".join(["─" * max_len for max_len in max_column_lens]) + "─┘")
