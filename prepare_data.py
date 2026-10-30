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

print("Sample Shape:", df.shape)

print("\nSample Preview:")
print(df.head().to_string(index=False))

print("\nResult Counts:")
print(df["test_result"].value_counts().to_string())