# Graph Schema

The Part II pipeline emits a portable graph as CSV files:

- `outputs/graph/nodes.csv`
- `outputs/graph/edges.csv`

## Node Columns

| Column | Meaning |
| --- | --- |
| `node_id` | Stable identifier for the node. |
| `label` | Node class. |
| `name` | Human-readable display name. |
| `source_path` | Repository path that supplied the node, when applicable. |
| `attributes_json` | Additional deterministic metadata encoded as JSON. |

## Node Labels

| Label | Meaning |
| --- | --- |
| `ResearchTrack` | Part I or Part II repository layer. |
| `SourceFile` | Committed source file included in the inventory. |
| `AsdiDataset` | Dataset entry from the ASDI dictionary. |
| `DatasetType` | ASDI dataset type such as weather, climate, or related categories. |
| `SdgGoal` | Sustainable Development Goal derived from ASDI or policy tables. |
| `SdgTarget` | SDG target derived from the policy indicator table. |
| `PolicyIndicator` | Policy indicator row derived from `01 Tabla B1.csv`. |

## Edge Columns

| Column | Meaning |
| --- | --- |
| `edge_id` | Stable hash identifier for the edge. |
| `source_id` | Source node id. |
| `target_id` | Target node id. |
| `edge_type` | Relationship class. |
| `source_path` | Repository path that supplied the relationship, when applicable. |
| `attributes_json` | Additional deterministic metadata encoded as JSON. |

## Edge Types

| Edge type | Meaning |
| --- | --- |
| `DERIVES_FROM` | Part II derives from Part I thesis materials. |
| `CONTAINS_FILE` | Part I contains a committed source file. |
| `DECLARES_ASDI_DATASET` | The ASDI CSV declares an ASDI dataset node. |
| `HAS_DATASET_TYPE` | An ASDI dataset has a dataset type. |
| `SUPPORTS_GOAL` | An ASDI dataset is associated with an SDG goal. |
| `DECLARES_POLICY_INDICATOR` | The policy CSV declares a policy indicator. |
| `MEASURES_TARGET` | A policy indicator measures an SDG target. |
| `BELONGS_TO_GOAL` | An SDG target belongs to an SDG goal. |

## Neo4j Import Note

The CSVs are intentionally database-neutral. A Neo4j import can map `label` to
node labels and `edge_type` to relationship types. Cypher migration files are a
publication task if a future release must reproduce a live Neo4j database.
