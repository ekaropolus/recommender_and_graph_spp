# Reproducibility Guide

This guide describes how to move from the current research archive to a
reproducible analysis run.

## 1. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## 2. Configure External Services

Some notebooks require Neo4j Aura and ExpertAI credentials. Configure them
through environment variables or Colab secrets:

```bash
NEO4J_URI=neo4j+s://<neo4j-aura-host>
NEO4J_USER=neo4j
NEO4J_PASSWORD=...
EAI_USERNAME=...
EAI_PASSWORD=...
```

Do not hard-code these values into notebooks.

## 3. Validate the Repository

```bash
python scripts/validate_repository.py
```

This verifies:

- required documentation files exist;
- notebooks are valid JSON;
- tracked files do not contain common credential patterns;
- expected data directories are present.

## 4. Notebook Order

The original Colab workflow is exploratory. For manual reconstruction, use this
order:

1. `Neo4j_ASDI_Sustainable_Public_Policies.ipynb`
2. `Extractor_Neo4j_ASDI_Sustainable_Public_Policies_MX.ipynb`
3. `Extractor_Neo4j_ASDI_GBIF.ipynb`
4. `DS_Neo4j_ExpertIA_Sustainable_Public_Policies_MX.ipynb`
5. `NLP_Neo4j_ExpertIA_Sustainable_Public_Policies_MX.ipynb`

## 5. Known Reproducibility Gaps

- The notebooks still need to be converted into deterministic scripts.
- Neo4j database state should be represented as migration files or Cypher
  scripts, not only notebook cells.
- Output tables and graph snapshots should be written to a versioned
  `outputs/` or release artifact, not committed ad hoc.
- Several data files need source-level provenance notes before formal release.

## 6. Recommended Next Hardening Step

Create a `src/` pipeline that:

1. reads committed CSV/XLSX inputs;
2. normalizes table names and schemas;
3. emits deterministic graph node/edge CSVs;
4. writes a reproducible Cypher import script;
5. produces a machine-readable run manifest with checksums.
