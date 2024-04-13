import difflib
from sqlittaaja.extractor import student_info

# Threshold percentage for warning >=
threshold = 99


def compare_files(file1_content, file2_content):
    """Compute the similarity ratio using SequenceMatcher"""

    similarity_ratio = (
        difflib.SequenceMatcher(None, file1_content, file2_content).ratio() * 100
    )
    return similarity_ratio


def compute_similarity(extracted):
    """Check students' exercises."""

    similarity_matrix = {}

    # Go through each students file against other files
    for file1, content1 in extracted.items():
        if file1.endswith(".sql"):  # Only .sql files
            for file2, content2 in extracted.items():
                if (
                    file2.endswith(".sql") and file1 != file2
                ):  # Exclude self-comparisons
                    similarity_ratio = compare_files(content1, content2)
                    if similarity_ratio >= threshold:
                        # Make more readable: student name + filename
                        student1 = (
                            student_info(file1)[0] + "/" + file1.rsplit("/", 1)[-1]
                        )
                        student2 = (
                            student_info(file2)[0] + "/" + file2.rsplit("/", 1)[-1]
                        )

                        similarity_matrix[(student1, student2)] = (
                            str(round(similarity_ratio, 2)) + "%"
                        )

    return similarity_matrix
