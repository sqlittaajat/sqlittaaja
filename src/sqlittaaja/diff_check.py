import difflib
from sqlittaaja.extractor import student_info

# Threshold percentage for warning >=
threshold = 90


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
        for file2, content2 in extracted.items():
            # Exclude self-comparisons
            if file1 != file2:
                similarity_ratio = compare_files(content1, content2)
                if similarity_ratio >= threshold:
                    similarity_matrix[
                        (student_info(file1)[0], student_info(file2)[0])
                    ] = (str(round(similarity_ratio, 2)) + "%")

    return similarity_matrix
