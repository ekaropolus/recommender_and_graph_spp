# Data Statement

This statement documents the data used by the Part II reproducible layer.

## Committed Source Families

| Family | Path | Used directly by pipeline | Role |
| --- | --- | --- | --- |
| ASDI dataset dictionary | `ASDI Tables/02 ASDI Data Set Dictionary.csv` | yes | Normalized into ASDI dataset nodes and SDG goal support edges. |
| Public policy indicator table | `Public Policies Tables/01 Tabla B1.csv` | yes | Normalized into SDG goals, targets, policy indicators, and measurement edges. |
| ASDI workbook | `ASDI Tables/01 ASDI Data Sets Dictionary.xlsx` | inventory only | Historical thesis-supporting workbook. |
| GBIF Mexico sample | `ASDI Tables/GBI Data Set/GBI MX Dataset.csv` | inventory only | Historical biodiversity-linked input. |
| Public policy workbooks | `Public Policies Tables/*.xlsx` | inventory only | Historical thesis-supporting policy tables. |
| Colab notebooks | `Google Colab Notebooks/*.ipynb` | inventory only | Exploratory execution records used by the thesis archive. |

## Provenance Status

The committed files are sufficient for a deterministic repository-local rebuild
of the Part II graph slice. External scholarly provenance is still incomplete
for several historical files because the original archive does not include
source URLs, access dates, and license statements for every table.

The run manifest records file checksums so future reviewers can verify that the
same committed inputs were used.

## Ethical And Security Notes

The reproducible layer does not require service credentials. Private database
state and notebook secrets are intentionally excluded.
