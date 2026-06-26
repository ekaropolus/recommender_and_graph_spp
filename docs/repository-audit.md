# Repository Audit

Audit date: 2026-06-26

## Current State

- Repository: `ekaropolus/recommender_and_graph_spp`
- Default branch: `main`
- Visibility: public
- Local status before curation: clean and synchronized with `origin/main`
- Primary research context: doctoral thesis materials for graph-based
  recommendation systems in sustainable public policy.

## Strengths

- The repository exists publicly and is not archived.
- It contains thesis-relevant data tables and notebooks.
- It has a permissive MIT license.
- The README now names the academic context and current reproducibility status.
- Credentials are expected through environment variables rather than literals.

## Issues Addressed In This Curation

- Removed hard-coded service credentials from current notebook files.
- Added `.env.example` and `.gitignore` safeguards.
- Added citation metadata through `CITATION.cff`.
- Added provenance and reproducibility documentation.
- Added a validation script for notebook JSON and common secret patterns.

## Remaining Risks

- Historical commits may still contain credentials; rotate exposed credentials.
- Git history has not been rewritten.
- Notebooks still depend on external services and should be converted to scripts.
- Data provenance is not yet complete at every table level.
- No DOI has been minted.

## Release Criteria For A Formal Research Artifact

Before tagging a formal release, complete:

1. Credential rotation and secret-scanning review.
2. Table-level provenance for each committed dataset.
3. Deterministic scripts for graph construction.
4. Output manifests and checksums.
5. `CITATION.cff` update with release date and DOI.
