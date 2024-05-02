import difflib

make_table = difflib.HtmlDiff(wrapcolumn=50).make_table


def generate_html_table(
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
            tables += make_table(
                content1.splitlines(),
                content2.splitlines(),
                fromdesc=f"{student1_name}: {str(round(similarity * 100, 2))}%",
                todesc=f"{student2_name}: {str(round(similarity * 100, 2))}%",
            )
    return tables
