def print_scores(student_scores):
    """Prints student scores."""

    print("STUDENT SCORES")
    for student_name, score in student_scores.items():
        print(f"{student_name}: {score}")
