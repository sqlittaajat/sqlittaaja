import difflib
import os
import sys


def gen_scores_table(
    student_scores: dict[str, int],
    answer_similarities: dict[str, list[tuple[str, float]]] = {},
    max_score=0,
) -> list[list[str]]:
    """Generate table list matrix out of student scores."""

    scores_list = [
        [
            student_name,
            f"{score} / {max_score}" if max_score > 0 else str(score),
        ]
        for student_name, score in student_scores.items()
    ]

    return (
        [["Student Name", "Score", "Similarity"]]
        + [
            [
                student_score[0],
                student_score[1],
                # Show similarity for each student.
                "\n".join(
                    f"{similarity[0]} ({str(round(similarity[1] * 100, 2))}%)"
                    for similarity in answer_similarities.get(student_score[0], [])
                ),
            ]
            for student_score in scores_list
        ]
        if answer_similarities
        else [["Student Name", "Score"]] + scores_list
    )


def print_scores(
    student_scores: dict[str, int],
    answer_similarities: dict[str, list[tuple[str, float]]] = {},
    max_score=0,
):
    """Prints student scores and similarity ratios"""

    print_table(
        gen_scores_table(student_scores, answer_similarities, max_score),
        separators=bool(answer_similarities),
    )
    print(f"Total rows: {len(student_scores)}")


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


def html_scores(
    student_scores: dict[str, int],
    answer_similarities: dict[str, list[tuple[str, float]]] = {},
    max_score=0,
) -> str:
    """Generate student scores and similarity ratios in HTML."""

    return f"{
        html_table(gen_scores_table(student_scores,
                   answer_similarities, max_score))
    }\n<p>Total rows: {len(student_scores)}</p>"


def html_table(table: list[list[str]]) -> str:
    """Generate a generic HTML table."""

    return (
        """<table>
  <thead>
    <tr>
"""
        # Generate header.
        + "".join(
            (
                f"      <th>\n{indent(title, width=8)}\n      </th>\n"
                if title
                else "      <th></th>\n"
            )
            for title in table[0]
        )
        + """    </tr>
  </thead>
  <tbody>
"""
        + "".join(
            (
                # Generate each row.
                "    <tr>\n"
                + "".join(
                    (
                        f"      <td>\n{indent(text, width=8)}\n      </td>\n"
                        if text
                        else "      <td></td>\n"
                    )
                    for text in row
                )
                + "    </tr>\n"
            )
            for row in table[1:]
        )
        + """  </tbody>
</table>"""
    )


def indent(text: str, width: int) -> str:
    """Indent each line of the text."""

    return "\n".join(map(lambda line: " " * width + line, text.splitlines()))


def html_diff_table(
    similarity_results: dict[tuple[str, str], float], extracted: dict[str, str]
) -> str:
    """Generate HTML table from flagged exercises."""

    tables = ""
    for student1_key, flags in similarity_results.items():
        student1_name = student1_key.split("_")[0]
        for student2_key, similarity in flags:
            student2_name = student2_key.split("_")[0]
            # Find the key in extracted_data by matching the first part
            content1 = extracted[
                [key for key in extracted.keys() if key.startswith(student1_name)][0]
            ]
            content2 = extracted[
                [key for key in extracted.keys() if key.startswith(student2_name)][0]
            ]
            tables += (
                difflib.HtmlDiff(tabsize=2, wrapcolumn=50).make_table(
                    content1.splitlines(),
                    content2.splitlines(),
                    fromdesc=f"{student1_name}: {
                        str(round(similarity * 100, 2))}%",
                    todesc=f"{student2_name}: {
                        str(round(similarity * 100, 2))}%",
                )
                # Replace 4 spaces with 2 spaces for indentation.
                .replace("    ", "  ")
            )
    return tables


def report_style() -> str:
    """Reads style.css file and returns content."""

    try:
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        style_css_path = os.path.join(base_path, "style.css")
        with open(style_css_path, encoding="utf-8") as style_file:
            return style_file.read()
    except FileNotFoundError:
        return ""
