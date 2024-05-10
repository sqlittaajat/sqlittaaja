from sqlittaaja.output import (
    print_scores,
    html_scores,
    indent,
    html_diff_table,
    report_style,
)
from sqlittaaja.config import read_args
from sqlittaaja.checker import check_exercises, compute_similarity
from sqlittaaja.extractor import extract
import tempfile
import webbrowser


def main():
    config = read_args()

    total_scores: dict[str, int] = {}

    html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>SQLittaaja Report</title>
    <style>
{indent(report_style(), width=6)}
    </style>
  </head>
  <body>
"""

    for path, answer, must_contain, must_not_contain in config.exercises:
        exercises = extract(path)

        student_scores = check_exercises(
            config.initialize_script, answer, exercises, must_contain, must_not_contain
        )
        answer_similarities = compute_similarity(config.threshold_pct, exercises)

        # Add the score in order to accumulate overall score for each student.
        for student_name, score in student_scores.items():
            total_scores[student_name] = total_scores.get(student_name, 0) + score

        # Print scores for each individual exercise packet.
        print(f"Scores for '{path}'")
        print_scores(student_scores, answer_similarities)

        html += f"""    <details>
      <summary>Scores for '{path}'</summary>
{indent(html_scores(student_scores, answer_similarities), width=6)}
"""
        if answer_similarities:
            html += f"""      <details>
        <summary>Differ</summary>{indent(html_diff_table(answer_similarities, exercises), width=6)}
      </details>
"""
        html += "    </details>\n"

        print()

    # Print the final scores for each student.
    print("Total scores")
    max_score = len(config.exercises)
    print_scores(total_scores, max_score=max_score)
    html += indent(html_scores(total_scores, max_score=max_score), width=4)
    print()

    html += """
  </body>
</html>
"""

    # Write the HTML report to a temporary file and print the filepath.
    with tempfile.NamedTemporaryFile(
        mode="w",
        prefix="sqlittaaja_report_",
        suffix=".html",
        encoding="utf-8",
        delete=False,
    ) as file:
        file.write(html)
        print(f"Report: {file.name}")

        if config.open_report:
            webbrowser.open(file.name)
