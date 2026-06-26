# Recommender and Graph Systems for Sustainable Public Policy

Research archive and reproducibility scaffold for doctoral thesis work on graph-based recommendation systems for sustainable public policy analysis.

The repository is organized in two parts:

- **Part I - Thesis-dependent research archive:** the data tables, notebooks, and documentation that support the doctoral thesis.
- **Part II - Fully reproducible scholarship track:** a separate roadmap for turning the thesis archive into a deterministic, citable, computational research package.

## Part I - Thesis-Dependent Research Archive

This repository supports the doctoral research project:

**Perspectivas de diseno en sistemas y grafos de recomendacion para el analisis de politicas publicas sostenibles**

Edgar Antonio Valdes Porras, Doctorado en Sostenibilidad, Universidad Centro Panamericano de Estudios Superiores (UNICEPES), 2022.

The thesis studies how public policy documents, sustainability indicators, and institutional plans can be represented as graph structures. The objective is to make policy relationships easier to compare, recommend, and explain across places, policy themes, and development priorities.

This repository is not a polished software product. It is a curated research archive containing thesis-supporting data tables, exploratory notebooks, graph construction routines, and documentation needed to make the work auditable.

### Research Questions

The repository is organized around these operational questions:

1. How can sustainable-development indicators and public-policy structures be represented as interoperable graph layers?
2. How can graph relationships support policy comparison, filtering, and recommendation?
3. Which data structures are needed to move from static policy documents toward computable public-policy intelligence?
4. What evidence from the thesis can be preserved as reusable research infrastructure?

### Repository Contents

- `ASDI Tables/`: sustainability indicator and open-data dictionaries used as structured inputs.
- `Public Policies Tables/`: policy and development-plan tables used for graph and recommendation experiments.
- `Google Colab Notebooks/`: exploratory notebooks for Neo4j graph construction, ASDI/GBIF extraction, and NLP-assisted policy analysis.
- `docs/`: research map, provenance notes, and reproducibility guidance.
- `reproducible-scholarship/`: second-track plan for full computational reproducibility.
- `scripts/`: lightweight validation utilities for repository hygiene.

## Reproducibility Status

Part I status: **curated thesis archive, partial reproducibility**.

Part II status: **implemented committed-input reproducible graph slice; DOI and external source recovery remain publication tasks**.

What is already present:

- Public thesis-supporting repository under `ekaropolus/recommender_and_graph_spp`.
- Structured datasets in CSV/XLSX form.
- Exploratory Colab notebooks for graph loading and extraction.
- MIT license.
- Reproducibility and provenance documentation.

What remains intentionally flagged:

- Some notebook steps require external Neo4j or ExpertAI credentials.
- Historical notebooks were created in Colab and should be treated as exploratory execution records.
- A fully automated end-to-end pipeline still needs to be derived from the notebooks.
- Data provenance is documented at repository level, but several XLSX tables need table-level source notes before formal publication.

## Part II - Fully Reproducible Scholarship Track

The second part does not claim that the original thesis archive is already fully reproducible. It implements a deterministic graph slice from committed source data to generated outputs and marks remaining DOI/source-recovery work as publication tasks.

See [`reproducible-scholarship/`](reproducible-scholarship/) for:

- the reproducibility target;
- the publication-grade definition of done;
- the dataset and graph-schema requirements;
- the run-manifest template;
- the release checklist for DOI-ready publication.
- generated graph, table, and manifest outputs.

## Quick Start

Install the minimal Python environment:

```bash
python -m pip install -r requirements.txt
```

Run the repository audit:

```bash
python scripts/validate_repository.py
```

For notebook execution, copy `.env.example` to `.env` or configure equivalent Colab secrets. Do not commit `.env` or real service credentials.

## Research Use

Use this repository as:

- evidence of the data and computational materials associated with the doctoral thesis;
- a starting point for reproducible policy-graph reconstruction;
- a source archive for sustainable public-policy recommendation experiments;
- a bridge between thesis claims, datasets, and exploratory graph notebooks.

Do not use it yet as:

- a production-ready recommendation engine;
- a final data package with complete provenance at table level;
- a credentialed service deployment.

## Documentation

- [Thesis map](docs/thesis-map.md)
- [Data provenance](docs/provenance.md)
- [Reproducibility guide](docs/reproducibility.md)
- [Fully reproducible scholarship track](reproducible-scholarship/README.md)
- [Scholarship release checklist](reproducible-scholarship/checklist.md)
- [Repository audit](docs/repository-audit.md)

## Citation

See [CITATION.cff](CITATION.cff). Until a DOI is minted, cite the GitHub repository URL and the commit hash used for analysis.

## Security

Credentials must be provided through environment variables or notebook secrets. The current notebooks are configured to read:

- `NEO4J_URI`
- `NEO4J_USER`
- `NEO4J_PASSWORD`
- `EAI_USERNAME`
- `EAI_PASSWORD`

If a prior public revision exposed credentials, rotate those credentials and consider history rewriting or GitHub secret scanning remediation before relying on the repository as a public artifact.
