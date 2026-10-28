import csv
import pandas as pd
import random
import json

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

def iter_eligible_records(zip_path):
    with ZipFile(zip_path, "r") as archive:
        for month in range(1, 13):
            month_file_path = (
                "dft_test_result_extracts_2025/"
                f"dft_test_result_extract_2025{month:02d}.csv"
            )

            print(f"Reading month {month:02d}...")

            with archive.open(month_file_path) as binary_file:
                with TextIOWrapper(
                    binary_file,
                    encoding="utf-8-sig",
                    newline=""
                ) as text_file:
                    reader = csv.DictReader(
                        text_file,
                        escapechar="\\"
                    )

                    for row in reader:
                        if is_eligible(row):
                            yield row

# project directory path
project_dir = Path(__file__).resolve().parent
zip_path = project_dir / "data" / "raw" / "dft_test_result_extracts_2025.zip"
sample_size = 50000
seed = 42

eligible_rows = iter_eligible_records(zip_path)

print("\nBuilding annual random sample...")

sample, seen_count = reservoir_sample(
    eligible_rows,
    sample_size=sample_size,
    seed=seed
)

df = pd.DataFrame(sample)

print("\nTotal Eligible Records Seen:", seen_count)
print("Sample Shape:", df.shape)

print("\nSample Preview:")
print(df.head(10).to_string(index=False))

print("\nSample Result Counts:")
print(df["test_result"].value_counts().to_string())

output_dir = project_dir / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)
sample_path = output_dir / f"mot_2025_sample_{sample_size}.csv"

df.to_csv(
    sample_path,
    index=False,
    encoding="utf-8"
)

print("\nSample saved to:", sample_path)

metadata = {
    "dataset_year": 2025,
    "source_url": (
        "https://open.data.dvsa.gov.uk/"
        "mot-anonymised/index.html"
    ),
    "source_archive": zip_path.name,
    "source_archive_size_bytes": zip_path.stat().st_size,
    "months": list(range(1, 13)),
    "sampling_method": "reservoir sampling",
    "seed": seed,
    "requested_sample_size": sample_size,
    "saved_sample_size": len(df),
    "eligible_records_seen": seen_count,
    "filters": {
        "test_class_id": "4",
        "test_type": "NT",
        "test_result": ["P", "F", "PRS"]
    },
    "sample_result_counts": {
        result: int(count)
        for result, count in df["test_result"].value_counts().items()
    },
    "columns": df.columns.tolist()
}

metadata_path = (
    output_dir / f"mot_2025_sample_{sample_size}_metadata.json"
)

metadata_path.write_text(
    json.dumps(metadata, indent=4, ensure_ascii=False),
    encoding="utf-8"
)

print("Metadata saved to:", metadata_path)

saved_df = pd.read_csv(
    sample_path,
    dtype=str,
    keep_default_na=False
)

assert saved_df.shape == df.shape
assert saved_df.columns.tolist() == df.columns.tolist()
assert saved_df["test_id"].tolist() == df["test_id"].tolist()

print("\nSaved Sample Shape:", saved_df.shape)