import csv
import pandas as pd

from pathlib import Path
from zipfile import ZipFile
from io import TextIOWrapper
from itertools import islice

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

# open the zip file, after print the column names
with ZipFile(zip_path, "r") as archive:
    with archive.open(january_file_path) as binary_file:
        with TextIOWrapper(binary_file, encoding="utf-8-sig", newline="") as text_file:
            reader = csv.DictReader(text_file)
            print("\nColumns:")
            print(reader.fieldnames)

            eligible_records = (
                row for row in reader
                if row["test_class_id"] == "4"
                   and row["test_type"] == "NT"
                   and row["test_result"] in {"P", "F", "PRS"}
            )

            records = list(islice(eligible_records, 50))
            df = pd.DataFrame(records)

            print("\nFirst 50 Eligible Records")
            print(df.to_string(index=False))

            print("\nShape:", df.shape)