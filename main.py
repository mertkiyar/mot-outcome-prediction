import csv
import pandas as pd

from pathlib import Path
from zipfile import ZipFile
from io import TextIOWrapper
from collections import Counter

def is_eligible(row):
    return (
        row["test_class_id"] == "4"
        and row["test_type"] == "NT"
        and row["test_result"] in {"P", "F", "PRS"}
    )

def read_month(zip_path, month_file_path, preview_size=50):
    result_counts = Counter()
    records = []

    with ZipFile(zip_path, "r") as archive:
        with archive.open(month_file_path) as binary_file:
            with TextIOWrapper(
                binary_file,
                encoding="utf-8-sig",
                newline=""
            ) as text_file:
                reader = csv.DictReader(text_file)
                column_names = reader.fieldnames

                for row in reader:
                    if is_eligible(row):
                        result_counts[row["test_result"]] += 1

                        if len(records) < preview_size:
                            records.append(row)

    return records, result_counts, column_names

def display_results(records, result_counts, column_names):
    print("\nColumns:")
    print(column_names)

    df = pd.DataFrame(records)

    print("\nFirst 50 Eligible Records")
    print(df.to_string(index=False))

    print("\nShape:", df.shape)

    total_count = sum(result_counts.values())

    print("\nTotal Eligible Records:", total_count)

    summary_rows = []

    for result in ("P", "F", "PRS"):
        count = result_counts[result]
        percentage = count / total_count * 100 if total_count else 0

        summary_rows.append({
            "result": result,
            "count": count,
            "percentage": round(percentage, 2)
        })

    summary = pd.DataFrame(summary_rows)

    print("\nResult Distribution (%)")
    print(summary.to_string(index=False))

    direct_pass_count = result_counts["P"]
    initial_defect_count = result_counts["F"] + result_counts["PRS"]

    print("\nDirect Pass:", direct_pass_count)
    print("Initial Defect:", initial_defect_count)


# project directory path
project_dir = Path(__file__).resolve().parent
zip_path = project_dir / "data" / "raw" / "dft_test_result_extracts_2025.zip"

# open the zip file, after print file name and size
with ZipFile(zip_path, "r") as archive:
    for file in archive.infolist():
        print(file.filename, f"{file.file_size / 1_000_000:.1f} MB")

january_file_path = (
    "dft_test_result_extracts_2025/"
    "dft_test_result_extract_202501.csv"
)

print("\nCounting eligible records...")

records, result_counts, column_names = read_month(
    zip_path,
    january_file_path
)

display_results(records, result_counts, column_names)