import pandas as pd

from pathlib import Path

project_dir = Path(__file__).resolve().parent
sample_path = (
    project_dir / "data" / "processed" / "mot_2025_sample_50000.csv"
)

df = pd.read_csv(
    sample_path,
    dtype=str,
    keep_default_na=False
)

target_mapping = {
    "P": 0,
    "F": 1,
    "PRS": 1
}

df["initial_defect"] = df["test_result"].map(target_mapping)

assert df["initial_defect"].notna().all(), "Unexpected test result"

print("Sample Shape:", df.shape)

print("\nSample Preview:")
print(df.head().to_string(index=False))

print("\nResult Counts:")
print(df["test_result"].value_counts().to_string())

print("\nInitial Defect Counts:")
print(df["initial_defect"].value_counts().sort_index().to_string())