# Dataset Reference

[Back to README](README.md)

## Dataset columns

Each row represents one MOT test. A vehicle can appear in more than one row.

| Column | Meaning | Example or unit |
| --- | --- | --- |
| `test_id` | Unique identifier for a test | `1809551695` |
| `vehicle_id` | Anonymous vehicle identifier; links tests for the same vehicle | `986896270` |
| `test_date` | Date of the test | `2025-01-16` |
| `test_class_id` | Vehicle test category; see the class table below | `1` = motorcycle class |
| `test_type` | Type of test, such as a normal test or a retest | `NT` = normal test |
| `test_result` | Recorded test outcome | `P` = passed; `F` = failed |
| `test_mileage` | Odometer reading at the test, in miles. Zero or blank may mean no reading was recorded | Miles, not kilometres |
| `postcode_area` | Broad postcode area of the test location, not a full address. `XX` groups areas with fewer than five active test stations | `BN`, `RM`, `XX` |
| `make` | Vehicle manufacturer. `UNCLASSIFIED` means no valid make/model record was available | `HONDA` |
| `model` | Manufacturer's model name | `CG125` |
| `colour` | Recorded vehicle colour | `RED` |
| `fuel_type` | Fuel or power source; see the fuel table below | `PE` = petrol; `EL` = electric |
| `cylinder_capacity` | Engine displacement in cubic centimetres (cc). It may be blank for electric vehicles | `124` means 124 cc |
| `first_use_date` | Date the vehicle was first used; can be used with `test_date` to calculate age. The guide identifies `1971-01-01` as a possible placeholder for an unknown date | `1989-03-09` |
| `completed_date` | Recorded test completion timestamp. `Z` indicates UTC | `2025-01-16T12:11:50.000Z` |

## Code meanings

### Vehicle class (`test_class_id`)

These are vehicle categories, not ratings or levels of defect severity.

| Code | Meaning |
| --- | --- |
| `0` | Legacy records from before MOT computerisation, if present |
| `1` | Motorcycles up to 200 cc, with or without a sidecar; also qualifying low-power motorcycles up to 4 kW and 45 km/h |
| `2` | Motorcycles and motorcycle combinations other than category L1 mopeds. This is a broader motorcycle class, not a defect level |
| `3` | Three-wheeled vehicles up to 450 kg unladen weight, excluding motorcycle-and-sidecar combinations |
| `4` | Cars, taxis, motor caravans and other qualifying light vehicles; includes goods vehicles up to 3,000 kg and qualifying passenger vehicles with up to 12 passenger seats |
| `5` | Qualifying private passenger vehicles with 13 or more passenger seats, including certain ambulances and motor caravans |
| `7` | Goods vehicles over 3,000 kg and up to 3,500 kg in the dataset guide |

Sources: [DVSA dataset guide](https://edh-dvsa-data-gov-uk-files-prod.s3.eu-west-1.amazonaws.com/mot-testing-data-user-guide-v5.1.odt) and [motorcycle class definitions](https://www.gov.uk/guidance/mot-inspection-manual-for-motorcycles/introduction#application-classes-1-and-2).

### Test type (`test_type`)

VTS means Vehicle Testing Station.

| Code | Meaning |
| --- | --- |
| `NT` | Normal test: a full initial inspection |
| `RT` | Full retest |
| `PV` | Partial retest after repairs while the vehicle remained at the test station |
| `PL` | Partial retest after the vehicle left the station for repairs |
| `ES` | Statutory appeal test |
| `EI` | Inverted appeal, as named in the DVSA lookup |

Source: [DVSA test-type lookup](https://edh-dvsa-data-gov-uk-files-prod.s3.eu-west-1.amazonaws.com/dft_mdr_test_type_extract.csv).

### Test result (`test_result`)

| Code | Meaning |
| --- | --- |
| `P` | Passed |
| `F` | Failed |
| `PRS` | Passed after defects were repaired at the station, within one hour and before the result was recorded. The vehicle initially had defects that would cause failure |
| `ABA` | Abandoned: the test could not be completed safely or some items could not be inspected satisfactorily |
| `ABR` | Aborted because of a problem with the testing equipment or tester |
| `ABRVE` | Aborted by a Vehicle Examiner (VE) |
| `R` | Refused |

`P` and `F` are test outcomes, not fuel types. `PRS` is different from passing directly.

Source: [DVSA result lookup](https://edh-dvsa-data-gov-uk-files-prod.s3.eu-west-1.amazonaws.com/dft_mdr_test_outcome_extract.csv) and the dataset guide above.

### Fuel type (`fuel_type`)

| Code | Meaning |
| --- | --- |
| `PE` | Petrol |
| `DI` | Diesel |
| `EL` | Electric |
| `HY` | Hybrid electric, labelled "Hybrid Electric (Clean)" by DVSA |
| `ED` | Electric diesel |
| `CN` | Compressed natural gas (CNG) |
| `LN` | Liquefied natural gas (LNG) |
| `LP` | Liquefied petroleum gas (LPG) |
| `GA` | Gas |
| `GB` | Gas bi-fuel |
| `GD` | Gas diesel |
| `FC` | Fuel cells |
| `ST` | Steam |
| `OT` | Other |

Some 2025 records use full labels such as `ELECTRIC` and `HYBRID ELECTRIC (CLEAN)` instead of codes. These need to be standardised during preprocessing.

Source: [DVSA fuel-type lookup](https://edh-dvsa-data-gov-uk-files-prod.s3.eu-west-1.amazonaws.com/dft_mdr_fuel_type_extract.csv).

Data source: [DVSA 2025 MOT data](https://open.data.dvsa.gov.uk/mot-anonymised/index.html).
