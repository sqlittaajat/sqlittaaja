import difflib
from sqlittaaja.extractor import student_info

# Threshold percentage for warning >=
threshold = 0.9


def compare_files(file1_content: str, file2_content: str) -> float:
    """Compute the similarity ratio using SequenceMatcher"""

    return difflib.SequenceMatcher(a=file1_content, b=file2_content).ratio()


def compute_similarity(extracted: dict[str, str]) -> dict[tuple[str, str], float]:
    """Check students' exercises."""

    similarity_matrix = {}

    # Go through each students file against other files
    for file1, content1 in extracted.items():
        for file2, content2 in extracted.items():
            # Exclude self-comparisons
            if file1 != file2:
                similarity_ratio = compare_files(content1, content2)
                if similarity_ratio >= threshold:
                    student1 = student_info(file1)[0]
                    student2 = student_info(file2)[0]
                    similarity_matrix[(student1, student2)] = similarity_ratio

    return similarity_matrix
