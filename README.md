# MOT Outcome Prediction

A data mining course project to predict vehicle MOT test outcomes.

## Dataset columns

Each row represents one MOT test. A few key columns are listed below.

| Column | Meaning | Example |
| --- | --- | --- |
| `test_date` | Date of the test | `2025-01-16` |
| `test_class_id` | Vehicle test category | `4` = cars and other qualifying light vehicles |
| `test_type` | Type of test | `NT` = normal test; `RT` = retest |
| `test_result` | Recorded test outcome | `P` = passed; `F` = failed; `PRS` = passed after repairs at the station |
| `test_mileage` | Odometer reading in miles | `50000` |
| `fuel_type` | Fuel or power source | `PE` = petrol; `DI` = diesel; `EL` = electric |

See the [full column descriptions and code definitions](DATA_DICTIONARY.md).

Data source: [DVSA 2025 MOT data](https://open.data.dvsa.gov.uk/mot-anonymised/index.html).
