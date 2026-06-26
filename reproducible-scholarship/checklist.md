# Reproducible Scholarship Checklist

Use this checklist before claiming a formal reproducible research release.

| Area | Requirement | Status |
| --- | --- | --- |
| Research scope | Define the exact claims being reproduced from the thesis. | complete for committed-input v0 |
| Data provenance | Add source URL, access date, license, and transformation note for each table. | partial; historical source recovery remains |
| Input integrity | Generate SHA-256 checksums for all input files. | complete |
| Environment | Pin Python version and package versions. | partial; stdlib pipeline is pinned by script, notebooks remain dependency-based |
| Secret handling | Keep all credentials in environment variables or external secrets. | complete for current files |
| Notebook conversion | Convert exploratory notebooks into deterministic scripts. | complete for CSV graph slice |
| Graph schema | Document node labels, relationship types, properties, and constraints. | complete |
| Graph import | Provide Cypher migrations or import scripts. | publication task |
| Outputs | Generate versioned node/edge tables and summary outputs. | complete |
| Run manifest | Save execution metadata for every reproducible run. | complete |
| Tests | Validate data schemas, graph outputs, and credential hygiene. | complete |
| Citation | Add DOI and formal release metadata after archival deposit. | publication task |

## Release Rule

Do not tag an archival DOI release until the publication-task rows are either
completed or explicitly waived in the release notes. The committed-input v0
computational layer is reproducible from the files in this repository.
