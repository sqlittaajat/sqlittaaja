def print_scores(student_scores):
    """Prints student scores."""

    print("\nSTUDENT SCORES")
    for [student_name, student_id], score in student_scores.items():
        print(f"{student_name} ({student_id}): {score}")
