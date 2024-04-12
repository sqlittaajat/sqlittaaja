import difflib
from typing import Any
from zipfile import ZipFile
from sqlittaaja.extractor import extract, student_info

# Threshold percentage for warning >=
threshold = 90

def compare_files(file1_content, file2_content):
    """Compute the similarity ratio using SequenceMatcher"""

    similarity_ratio = difflib.SequenceMatcher(None, file1_content, file2_content).ratio()*100
    return similarity_ratio

def compute_similarity(config: dict[str, Any]) -> dict[str, int]:
    """Check students' exercises."""

    similarity_matrix = {}
    with ZipFile(config["exercise"]["path"], "r") as exercises:
        extracted = extract(exercises)

        for file1, content1 in extracted.items():
            if file1.endswith('.sql'):
                for file2, content2 in extracted.items():
                    if file2.endswith('.sql') and file1 != file2:  # Exclude self-comparisons
                        similarity_ratio = compare_files(content1, content2)
                        if similarity_ratio >= threshold:
                            student1 = student_info(file1)[0]+"/"+file1.rsplit('/', 1)[-1]
                            student2 = student_info(file2)[0]+"/"+file2.rsplit('/', 1)[-1]

                            similarity_matrix[(student1, student2)] = str(round(similarity_ratio, 2))+"%"
        return similarity_matrix