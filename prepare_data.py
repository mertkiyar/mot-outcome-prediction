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

df["test_date"] = pd.to_datetime(
    df["test_date"],
    format="%Y-%m-%d",
    errors="coerce"
)

df["first_use_date"] = pd.to_datetime(
    df["first_use_date"],
    format="%Y-%m-%d",
    errors="coerce"
)

df["vehicle_age"] = (
    df["test_date"] - df["first_use_date"]
).dt.days / 365.25

df["test_month"] = df["test_date"].dt.month.astype("Int64")

numeric_columns = ["test_mileage", "cylinder_capacity"]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

feature_columns = [
    "vehicle_age",
    "test_mileage",
    "cylinder_capacity",
    "fuel_type",
    "make",
    "test_month"
]

target_column = "initial_defect"

X = df[feature_columns].copy()
y = df[target_column].copy()

print("Sample Shape:", df.shape)

print("\nSample Preview:")
print(df.head().to_string(index=False))

print("\nResult Counts:")
print(df["test_result"].value_counts().to_string())

print("\nInitial Defect Counts:")
print(df["initial_defect"].value_counts().sort_index().to_string())

date_columns = ["test_date", "first_use_date"]

print("\nMissing or Invalid Dates:")
print(df[date_columns].isna().sum().to_string())

print("\nDate Feature Preview:")
print(
    df[
        ["test_date", "first_use_date", "vehicle_age", "test_month"]
    ].head(10).to_string(index=False)
)

print("\nNegative Vehicle Ages:", (df["vehicle_age"] < 0).sum())

print("\nTest Month Counts:")
print(df["test_month"].value_counts().sort_index().to_string())

print("\nNumeric Column Types:")
print(df[numeric_columns].dtypes.to_string())

print("\nMissing Numeric Values:")
print(df[numeric_columns].isna().sum().to_string())

print("\nNumeric Summary:")
print(df[numeric_columns].describe().to_string())

print("\nFeature Columns:")
print(X.columns.tolist())

print("\nFeature Shape:", X.shape)
print("Target Shape:", y.shape)