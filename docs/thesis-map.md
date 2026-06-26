# Thesis Map

This repository supports the doctoral thesis:

**Perspectivas de diseno en sistemas y grafos de recomendacion para el analisis de politicas publicas sostenibles**

Edgar Antonio Valdes Porras, Doctorado en Sostenibilidad, UNICEPES, 2022.

## Repository Role

The thesis proposes a design perspective for using graph structures and
recommendation systems to analyze sustainable public policies. This repository
preserves the computational side of that work:

- structured sustainability indicator dictionaries;
- policy and development-plan tables;
- graph-construction notebooks;
- exploratory NLP and recommendation-system workflows.

## Thesis-to-Repository Mapping

| Thesis element | Repository artifact | Purpose |
| --- | --- | --- |
| Sustainable-development indicators | `ASDI Tables/` | Indicator dictionaries and open-data alignment inputs. |
| Public-policy structures | `Public Policies Tables/` | State policy tables and policy-level structures. |
| Graph construction | `Google Colab Notebooks/*Neo4j*.ipynb` | Exploratory graph loading and relationship creation. |
| Recommendation-system design | `Google Colab Notebooks/DS_Neo4j_ExpertIA_Sustainable_Public_Policies_MX.ipynb` | Early data-science workflow for recommendation inputs. |
| NLP-assisted policy analysis | `Google Colab Notebooks/NLP_Neo4j_ExpertIA_Sustainable_Public_Policies_MX.ipynb` | Experimental text-processing layer for policy terms. |
| Research audit | `scripts/validate_repository.py` | Hygiene check for notebooks, docs, and credential safety. |

## Boundaries

This repository contains research materials and reproducibility scaffolding. It
does not contain the full doctoral dissertation text, institutional documents,
or private academic records. Those should remain in the controlled document
archive unless intentionally published elsewhere.

## Relationship To The Reproducible Scholarship Track

The thesis archive and the reproducible scholarship track have different roles:

- The thesis archive preserves the computational evidence associated with the
  doctoral work.
- The reproducible scholarship track defines the extra work required for a
  later computational publication that can be independently rerun.

The second track should not be cited as proof that the original thesis already
had a complete deterministic pipeline. It is a transparent hardening path from
the thesis materials to a stronger scholarly artifact.

## Current Evidence Level

The repository is sufficient as a public pointer to the thesis-supporting code
and data. It still requires additional normalization before it should be cited
as a fully reproducible computational package.
