# Fully Reproducible Scholarship Track

This is the second part of the repository. It is separate from the thesis
archive and defines the work required to turn the thesis materials into a
publication-grade, fully reproducible computational research package.

## Purpose

Part I preserves what supports the doctoral thesis. Part II defines how a
future reader should be able to rerun the computational work from documented
inputs to documented outputs without relying on private notebooks, private
database state, or undocumented manual steps.

## Reproducibility Target

A release is fully reproducible when an external reviewer can:

1. identify every input dataset and its source;
2. recreate the software environment;
3. run a deterministic pipeline from source tables to graph artifacts;
4. verify generated outputs using checksums and validation tests;
5. inspect the graph schema and transformation logic;
6. cite a stable release with a DOI, commit hash, and archived artifacts.

## Required Scholarly Artifacts

- Data statement with source URLs, access dates, licenses, and transformations.
- Machine-readable file inventory with checksums.
- Deterministic scripts derived from the exploratory Colab notebooks.
- Graph schema describing node labels, edge types, properties, and constraints.
- Cypher migrations or import scripts for Neo4j graph reconstruction.
- Versioned outputs, including node/edge tables and summary figures.
- Run manifest for each published execution.
- Tests that validate notebooks, data schemas, graph outputs, and credential hygiene.
- `CITATION.cff` release metadata with DOI after archival deposit.

## Proposed Future Layout

The current thesis archive keeps its historical folder names. The reproducible
track should eventually add a deterministic layout such as:

```text
data/
  raw/
  interim/
  processed/
schemas/
  input-tables/
  graph/
src/
  extract/
  transform/
  graph/
  report/
outputs/
  manifests/
  graph/
  tables/
tests/
```

Do not move the thesis archive until compatibility with existing notebook links
has been handled.

## Boundary From The Thesis Archive

This track is not additional evidence that the 2022 thesis already contained a
finished reproducible software package. It is a scholarly hardening path built
from the thesis materials. The distinction matters for accurate citation and
review.

## Next Implementation Step

Convert one notebook into a deterministic script that reads committed CSV/XLSX
inputs and emits a small node/edge graph artifact plus a run manifest. That
single working slice should become the template for the rest of the pipeline.
