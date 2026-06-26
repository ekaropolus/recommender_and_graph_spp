# Reproducible Scholarship Checklist

Use this checklist before claiming a formal reproducible research release.

| Area | Requirement | Status |
| --- | --- | --- |
| Research scope | Define the exact claims being reproduced from the thesis. | pending |
| Data provenance | Add source URL, access date, license, and transformation note for each table. | partial |
| Input integrity | Generate SHA-256 checksums for all input files. | pending |
| Environment | Pin Python version and package versions. | partial |
| Secret handling | Keep all credentials in environment variables or external secrets. | complete for current files |
| Notebook conversion | Convert exploratory notebooks into deterministic scripts. | pending |
| Graph schema | Document node labels, relationship types, properties, and constraints. | pending |
| Graph import | Provide Cypher migrations or import scripts. | pending |
| Outputs | Generate versioned node/edge tables and summary outputs. | pending |
| Run manifest | Save execution metadata for every reproducible run. | scaffolded |
| Tests | Validate data schemas, graph outputs, and credential hygiene. | partial |
| Citation | Add DOI and formal release metadata after archival deposit. | pending |

## Release Rule

Do not tag a release as fully reproducible until every row above is complete or
explicitly waived in the release notes.
