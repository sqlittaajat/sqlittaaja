import difflib
from sqlittaaja.extractor import student_info

# Threshold percentage for warning >=
threshold = 0.9


def compute_similarity(extracted: dict[str, str]) -> dict[str, list[tuple[str, float]]]:
    """Check students' exercises."""

    result = {}

    # Go through each students file against other files.
    for file1, content1 in extracted.items():
        for file2, content2 in extracted.items():
            # Exclude self-comparisons.
            if file1 != file2:
                # Calculate the ratio of how similar the answers are.
                similarity_ratio = difflib.SequenceMatcher(
                    a=content1, b=content2
                ).ratio()

                if similarity_ratio >= threshold:
                    student1 = student_info(file1)[0]
                    student2 = student_info(file2)[0]

                    # Append a new similarity to the result.
                    result[student1] = result.get(student1, []) + [
                        (student2, similarity_ratio)
                    ]

    return result
