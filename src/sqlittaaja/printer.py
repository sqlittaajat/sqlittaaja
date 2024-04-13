import itertools


def print_scores(
    student_scores: dict[str, int],
    answer_similarities: dict[str, list[tuple[str, float]]],
):
    """Prints student scores and similarity ratios"""

    print_table(
        [["Student Name", "Score"]]
        + [[student_name, str(score)] for student_name, score in student_scores.items()]
    )

    if answer_similarities:
        print_table(
            [["Student Name", "Similarity Ratio"]]
            + list(
                itertools.chain.from_iterable(
                    [
                        [
                            name + " => " + similarity[0],
                            str(round(similarity[1] * 100, 2)) + "%",
                        ]
                        for similarity in similarities
                    ]
                    for name, similarities in answer_similarities.items()
                )
            ),
            separators=True,
        )


def print_table(table: list[list[str]], separators: bool = False):
    """Print a table with pretty formatting."""

    max_column_lens = [
        # Calculate maximum length for each column.
        max([len(table[j][i]) for j, _ in enumerate(table)])
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
        print(
            "│ "
            + " │ ".join(
                [
                    value.ljust(max_column_lens[j])
                    for j, value in enumerate(table[i + 1])
                ]
            )
            + " │"
        )
        if separators and i + 1 < len(table) - 1:
            print(
                "├─" + "─┼─".join(["─" * max_len for max_len in max_column_lens]) + "─┤"
            )
    print("└─" + "─┴─".join(["─" * max_len for max_len in max_column_lens]) + "─┘")
