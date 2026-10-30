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

fuel_mapping = {
    "ELECTRIC": "EL",
    "HYBRID ELECTRIC (CLEAN)": "HY"
}

df["fuel_type_standardized"] = (
    df["fuel_type"]
    .str.strip()
    .str.upper()
    .replace(fuel_mapping)
)

feature_columns = [
    "vehicle_age",
    "test_mileage",
    "cylinder_capacity",
    "fuel_type_standardized",
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

blank_values = df.apply(
    lambda column: column.astype("string").str.strip().eq("")
).fillna(False)

missing_values = df.isna() | blank_values

missing_summary = pd.DataFrame({
    "missing_count": missing_values.sum(),
    "missing_percentage": (
        missing_values.mean() * 100
    ).round(2)
})

print("\nMissing Value Summary:")
print(missing_summary.to_string())

duplicate_row_count = df.duplicated().sum()

print("\nDuplicate Rows:", duplicate_row_count)

duplicate_test_count = df["test_id"].duplicated().sum()

print("Repeated Test IDs:", duplicate_test_count)

if duplicate_test_count > 0:
    repeated_tests = df[
        df["test_id"].duplicated(keep=False)
    ]

    print("\nRepeated Test Preview:")
    print(repeated_tests.head(10).to_string(index=False))

vehicle_counts = df["vehicle_id"].value_counts()
repeated_vehicles = vehicle_counts[vehicle_counts > 1]

print("\nUnique Vehicles:", df["vehicle_id"].nunique())
print("Vehicles With Multiple Records:", len(repeated_vehicles))
print("Records From These Vehicles:", repeated_vehicles.sum())

capacity_audit = df[["fuel_type", "cylinder_capacity"]].copy()

capacity_audit["capacity_missing"] = (
    capacity_audit["cylinder_capacity"].isna()
)

capacity_summary = capacity_audit.groupby("fuel_type").agg(
    total_records=("capacity_missing", "size"),
    missing_capacity=("capacity_missing", "sum")
)

capacity_summary["missing_percentage"] = (
    capacity_summary["missing_capacity"]
    / capacity_summary["total_records"]
    * 100
).round(2)

capacity_summary = capacity_summary.sort_values(
    "missing_capacity",
    ascending=False
)

print("\nMissing Engine Capacity by Fuel Type:")
print(capacity_summary.to_string())

assert (
    capacity_summary["missing_capacity"].sum()
    == df["cylinder_capacity"].isna().sum()
), "Missing capacity counts do not match"

print("\nMissing Engine Capacity Preview:")
print(
    df.loc[
        df["cylinder_capacity"].isna(),
        ["test_id", "make", "model", "fuel_type", "cylinder_capacity"]
    ].head(15).to_string(index=False)
)

print("\nFuel Type Counts:")
print(
    df["fuel_type"]
    .value_counts(dropna=False)
    .to_string()
)

text_columns = ["make", "model", "colour", "fuel_type"]

text_audit = df[text_columns].apply(
    lambda column: column.astype("string").str.strip().str.upper()
)

uncertain_labels = [
    "UNCLASSIFIED",
    "UNKNOWN",
    "NOT STATED",
    "NOT KNOWN",
    "N/A"
]

uncertain_summary = pd.DataFrame({
    column: text_audit[column].value_counts().reindex(
        uncertain_labels,
        fill_value=0
    )
    for column in text_columns
})

print("\nUncertain Label Counts:")
print(uncertain_summary.to_string())

for column in ["make", "model"]:
    print(f"\nTop 20 Values: {column}")
    print(text_audit[column].value_counts().head(20).to_string())

uncertain_mask = text_audit.isin(uncertain_labels).any(axis=1)

print("\nRecords With Uncertain Labels:", uncertain_mask.sum())

print("\nUncertain Label Preview:")
print(
    df.loc[
        uncertain_mask,
        ["test_id", "make", "model", "colour", "fuel_type"]
    ].head(15).to_string(index=False)
)

print("\nStandardized Fuel Type Counts:")
print(
    df["fuel_type_standardized"]
    .value_counts(dropna=False)
    .to_string()
)

assert not df["fuel_type_standardized"].isin(
    fuel_mapping.keys()
).any(), "Unmapped fuel labels remain"

audit_columns = [
    "vehicle_age",
    "test_mileage",
    "cylinder_capacity"
]

print("\nNumeric Quality Summary:")
print(
    df[audit_columns].describe(
        percentiles=[0.01, 0.5, 0.95, 0.99]
    ).to_string()
)

invalid_checks = pd.DataFrame({
    "negative_vehicle_age": df["vehicle_age"] < 0,
    "negative_mileage": df["test_mileage"] < 0,
    "nonpositive_capacity": df["cylinder_capacity"] <= 0
})

print("\nInvalid Value Counts:")
print(invalid_checks.sum().to_string())

print("\nZero Mileage Records:", df["test_mileage"].eq(0).sum())

preview_columns = [
    "test_id",
    "make",
    "model",
    "fuel_type_standardized",
    "vehicle_age",
    "test_mileage",
    "cylinder_capacity"
]

for column in audit_columns:
    available_rows = df.dropna(subset=[column])

    print(f"\nLowest Values: {column}")
    print(
        available_rows.nsmallest(5, column)[preview_columns]
        .to_string(index=False)
    )

    print(f"\nHighest Values: {column}")
    print(
        available_rows.nlargest(5, column)[preview_columns]
        .to_string(index=False)
    )

electric_with_capacity = (
    df["fuel_type_standardized"].eq("EL")
    & df["cylinder_capacity"].notna()
)

print(
    "\nElectric Vehicles With Recorded Engine Capacity:",
    electric_with_capacity.sum()
)

print(
    df.loc[electric_with_capacity, preview_columns]
    .head(15)
    .to_string(index=False)
)