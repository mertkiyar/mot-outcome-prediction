import csv
import pandas as pd
import random

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
                reader = csv.DictReader(text_file, escapechar="\\")
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

def reservoir_sample(rows, sample_size, seed=42):
    if sample_size <= 0:
        raise ValueError("Sample size must be positive")

    rng = random.Random(seed)
    sample = []
    seen_count = 0

    for seen_count, row in enumerate(rows, start=1):
        if len(sample) < sample_size:
            sample.append(row)
        else:
            index = rng.randrange(seen_count)

            if index < sample_size:
                sample[index] = row

    return sample, seen_count
# project directory path
project_dir = Path(__file__).resolve().parent
zip_path = project_dir / "data" / "raw" / "dft_test_result_extracts_2025.zip"
month = 2

if not 1 <= month <= 12:
    raise ValueError("Month must be between 1 and 12")

# open the zip file, after print file name and size
with ZipFile(zip_path, "r") as archive:
    for file in archive.infolist():
        print(file.filename, f"{file.file_size / 1_000_000:.1f} MB")

month_file_path = (
    "dft_test_result_extracts_2025/"
    f"dft_test_result_extract_2025{month:02d}.csv"
)

print(f"\nCounting eligible records for month {month:02d}...")

records, result_counts, column_names = read_month(
    zip_path,
    month_file_path
)

display_results(records, result_counts, column_names)

sample, seen_count = reservoir_sample(
    range(1, 11),
    sample_size=3,
    seed=42
)

print("\nSample:", sample)
print("Seen Records:", seen_count)