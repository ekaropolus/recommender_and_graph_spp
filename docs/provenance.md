# Data Provenance

This document records the current provenance status of the repository data. It
is intentionally conservative: when a precise source, extraction date, or
license has not been verified at table level, the status is marked as
`needs_table_level_source_note`.

## Source Families

| Dataset family | Path | Current provenance status | Notes |
| --- | --- | --- | --- |
| ASDI dictionary | `ASDI Tables/02 ASDI Data Set Dictionary.csv` | partial | Dictionary of sustainability/open-data datasets aligned to SDG identifiers. Needs source URL and extraction date per dataset. |
| ASDI workbook | `ASDI Tables/01 ASDI Data Sets Dictionary.xlsx` | partial | Spreadsheet version of the ASDI dictionary. Should be treated as a working data artifact. |
| GBIF Mexico sample | `ASDI Tables/GBI Data Set/GBI MX Dataset.csv` | partial | Contains GBIF-style occurrence fields and CC BY 4.0 rows. Needs download query, date, and citation export. |
| Public policy tables | `Public Policies Tables/*.xlsx` | partial | Structured policy/development-plan tables used in thesis graph experiments. Need state/source mapping and source URLs. |
| Public policy seed CSV | `Public Policies Tables/01 Tabla B1.csv` | partial | CSV seed file with SDG indicator content and classification labels. Needs source note and transformation note. |

## Provenance Requirements Before Formal Release

For each table intended for publication, add:

1. Source institution or source publication.
2. Source URL or archival reference.
3. Date accessed or extracted.
4. Transformation steps from raw source to repository table.
5. License or permitted-use basis.
6. Checksum of the committed file.
7. Relationship to thesis chapter, figure, table, or appendix.

## File Integrity

Use the validation script to generate a local inventory:

```bash
python scripts/validate_repository.py --inventory
```

The inventory is intended for audit and should be regenerated when files are
changed for a formal release.
