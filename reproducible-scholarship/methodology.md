# Methodology

This Part II layer turns selected committed thesis-supporting inputs into a
deterministic graph artifact.

## Inputs

The pipeline uses committed files only:

- `ASDI Tables/02 ASDI Data Set Dictionary.csv`
- `Public Policies Tables/01 Tabla B1.csv`
- file metadata from `ASDI Tables/`, `Public Policies Tables/`, and
  `Google Colab Notebooks/`

The XLSX files and notebooks are included in the input inventory as auditable
research materials. They are not used as hidden manual steps in the generated
graph slice.

## Transformations

1. Build a SHA-256 inventory of thesis-supporting source files.
2. Normalize ASDI dataset rows into `asdi_datasets.csv`.
3. Normalize SDG policy indicator rows into `sdg_policy_indicators.csv`.
4. Build graph nodes for research tracks, source files, ASDI datasets, dataset
   types, SDG goals, SDG targets, and policy indicators.
5. Build graph edges for containment, dataset declarations, goal support,
   target membership, and indicator measurement relationships.
6. Write generated tables, graph CSVs, summary counts, and a run manifest.

## Determinism

The build is deterministic for committed inputs:

- rows are sorted before writing;
- node and edge identifiers are stable hashes or source identifiers;
- output CSVs use a fixed column order and line ending;
- the manifest uses a stable `run_id` and records checksums for generated
  outputs.

## Scope Limit

The reproducible layer does not recreate a private Neo4j Aura database and does
not claim complete external provenance for every historical XLSX table. It
creates a rerunnable computational artifact from the committed repository state.
