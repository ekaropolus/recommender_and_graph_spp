# Research Notebooks

These notebooks preserve exploratory Colab workflows used during thesis work on
graph-based recommendation systems for sustainable public policy.

## Notebook Index

1. `Neo4j_ASDI_Sustainable_Public_Policies.ipynb`
   Creates early Neo4j relationships between ASDI datasets and public-policy graph structures.
2. `Extractor_Neo4j_ASDI_Sustainable_Public_Policies_MX.ipynb`
   Extracts sustainable-development-goal relationships for Mexico-facing policy analysis.
3. `Extractor_Neo4j_ASDI_GBIF.ipynb`
   Extracts ASDI/GBIF relationships for biodiversity-linked sustainability data.
4. `DS_Neo4j_ExpertIA_Sustainable_Public_Policies_MX.ipynb`
   Builds data-science inputs for recommendation and graph experiments.
5. `NLP_Neo4j_ExpertIA_Sustainable_Public_Policies_MX.ipynb`
   Explores NLP-assisted extraction of terms and semantic features from policy text.

## Execution Notes

The notebooks require external credentials for some cells. Configure them
through environment variables or Colab secrets:

- `NEO4J_URI`
- `NEO4J_USER`
- `NEO4J_PASSWORD`
- `EAI_USERNAME`
- `EAI_PASSWORD`

Do not hard-code credentials in notebook cells. For formal reproducibility,
convert these notebooks into deterministic scripts and record input/output
checksums.
