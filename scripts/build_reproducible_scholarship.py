#!/usr/bin/env python3
"""Build deterministic Part II reproducible-scholarship artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "reproducible-scholarship" / "outputs"
INPUT_ROOTS = [
    "ASDI Tables",
    "Public Policies Tables",
    "Google Colab Notebooks",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_hash(*parts: str, length: int = 16) -> str:
    text = "|".join(parts)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def clean_text(value: str | None) -> str:
    return " ".join((value or "").replace("\ufeff", "").split())


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def classify_file(path: Path) -> str:
    rel_path = rel(path)
    suffix = path.suffix.lower()
    if rel_path.startswith("ASDI Tables/"):
        return "asdi_input"
    if rel_path.startswith("Public Policies Tables/"):
        return "public_policy_input"
    if rel_path.startswith("Google Colab Notebooks/"):
        return "exploratory_notebook" if suffix == ".ipynb" else "notebook_documentation"
    return "supporting_file"


def build_file_inventory() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for root_name in INPUT_ROOTS:
        root = ROOT / root_name
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rows.append(
                {
                    "path": rel(path),
                    "role": classify_file(path),
                    "size_bytes": str(path.stat().st_size),
                    "sha256": sha256(path),
                }
            )
    return rows


def read_asdi_datasets() -> list[dict[str, str]]:
    path = ROOT / "ASDI Tables" / "02 ASDI Data Set Dictionary.csv"
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            dataset_id = clean_text(raw.get("ID"))
            title = clean_text(raw.get("ANSI DATASET"))
            if not dataset_id or not title:
                continue
            rows.append(
                {
                    "dataset_id": dataset_id,
                    "dataset_name": title,
                    "dataset_type": clean_text(raw.get("TYPE")),
                    "sdg_id": clean_text(raw.get("ID SDG")).upper(),
                    "source_path": rel(path),
                }
            )
    return sorted(rows, key=lambda item: item["dataset_id"])


def extract_first(pattern: str, text: str) -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else ""


def read_policy_indicators() -> list[dict[str, str]]:
    path = ROOT / "Public Policies Tables" / "01 Tabla B1.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        all_rows = list(csv.reader(handle))

    header_index = None
    for idx, row in enumerate(all_rows):
        normalized = [clean_text(cell).lower() for cell in row]
        if "objetivos" in normalized and "indicadores" in normalized:
            header_index = idx
            break
    if header_index is None:
        raise RuntimeError(f"Could not locate policy CSV header in {rel(path)}")

    current_goal = ""
    current_target = ""
    parsed: list[dict[str, str]] = []
    for raw in all_rows[header_index + 1 :]:
        padded = list(raw) + [""] * max(0, 5 - len(raw))
        goal_text = clean_text(padded[0])
        target_text = clean_text(padded[1])
        indicator_text = clean_text(padded[2])
        variable = clean_text(padded[3])
        disaggregated = clean_text(padded[4])

        if goal_text:
            current_goal = goal_text
        if target_text:
            current_target = target_text
        if not indicator_text:
            continue

        goal_id = extract_first(r"Objetivo\s+(\d+)", current_goal)
        target_id = extract_first(r"^(\d+(?:\.\w+)?)", current_target)
        indicator_id = extract_first(r"^(\d+(?:\.\w+){1,2})", indicator_text)
        fallback_id = stable_hash(current_goal, current_target, indicator_text)
        parsed.append(
            {
                "goal_id": goal_id,
                "goal_text": current_goal,
                "target_id": target_id,
                "target_text": current_target,
                "indicator_id": indicator_id or fallback_id,
                "indicator_text": indicator_text,
                "variable_principal": variable,
                "disaggregated": disaggregated,
                "source_path": rel(path),
            }
        )
    return sorted(parsed, key=lambda item: item["indicator_id"])


def attrs(**values: str) -> str:
    cleaned = {key: value for key, value in values.items() if value}
    return json.dumps(cleaned, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def add_node(nodes: dict[str, dict[str, str]], node_id: str, label: str, name: str, source_path: str = "", **extra: str) -> None:
    nodes[node_id] = {
        "node_id": node_id,
        "label": label,
        "name": name,
        "source_path": source_path,
        "attributes_json": attrs(**extra),
    }


def add_edge(
    edges: dict[str, dict[str, str]],
    source_id: str,
    target_id: str,
    edge_type: str,
    source_path: str = "",
    **extra: str,
) -> None:
    edge_id = f"edge:{stable_hash(source_id, edge_type, target_id, source_path)}"
    edges[edge_id] = {
        "edge_id": edge_id,
        "source_id": source_id,
        "target_id": target_id,
        "edge_type": edge_type,
        "source_path": source_path,
        "attributes_json": attrs(**extra),
    }


def build_graph(
    inventory: list[dict[str, str]],
    asdi_rows: list[dict[str, str]],
    policy_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    nodes: dict[str, dict[str, str]] = {}
    edges: dict[str, dict[str, str]] = {}

    add_node(nodes, "track:part-i", "ResearchTrack", "Part I - Thesis-dependent research archive")
    add_node(nodes, "track:part-ii", "ResearchTrack", "Part II - Fully reproducible scholarship track")
    add_edge(edges, "track:part-ii", "track:part-i", "DERIVES_FROM")

    for item in inventory:
        node_id = f"file:{stable_hash(item['path'])}"
        add_node(
            nodes,
            node_id,
            "SourceFile",
            item["path"],
            item["path"],
            role=item["role"],
            sha256=item["sha256"],
            size_bytes=item["size_bytes"],
        )
        add_edge(edges, "track:part-i", node_id, "CONTAINS_FILE", item["path"], role=item["role"])

    asdi_source_node = f"file:{stable_hash('ASDI Tables/02 ASDI Data Set Dictionary.csv')}"
    for row in asdi_rows:
        dataset_node = f"asdi:{row['dataset_id']}"
        add_node(
            nodes,
            dataset_node,
            "AsdiDataset",
            row["dataset_name"],
            row["source_path"],
            dataset_id=row["dataset_id"],
        )
        add_edge(edges, asdi_source_node, dataset_node, "DECLARES_ASDI_DATASET", row["source_path"])

        if row["dataset_type"]:
            type_node = f"dataset_type:{row['dataset_type'].lower()}"
            add_node(nodes, type_node, "DatasetType", row["dataset_type"], row["source_path"])
            add_edge(edges, dataset_node, type_node, "HAS_DATASET_TYPE", row["source_path"])

        if row["sdg_id"]:
            sdg_number = row["sdg_id"].replace("SDG", "")
            goal_node = f"sdg:{sdg_number}"
            add_node(nodes, goal_node, "SdgGoal", f"SDG {sdg_number}", row["source_path"], sdg_id=row["sdg_id"])
            add_edge(edges, dataset_node, goal_node, "SUPPORTS_GOAL", row["source_path"], sdg_id=row["sdg_id"])

    policy_source_node = f"file:{stable_hash('Public Policies Tables/01 Tabla B1.csv')}"
    for row in policy_rows:
        goal_node = f"sdg:{row['goal_id']}" if row["goal_id"] else f"sdg:{stable_hash(row['goal_text'])}"
        add_node(
            nodes,
            goal_node,
            "SdgGoal",
            f"SDG {row['goal_id']}" if row["goal_id"] else row["goal_text"][:80],
            row["source_path"],
            goal_text=row["goal_text"],
        )

        target_node = f"sdg_target:{row['target_id']}" if row["target_id"] else f"sdg_target:{stable_hash(row['target_text'])}"
        add_node(
            nodes,
            target_node,
            "SdgTarget",
            row["target_id"] or row["target_text"][:80],
            row["source_path"],
            target_text=row["target_text"],
        )
        add_edge(edges, target_node, goal_node, "BELONGS_TO_GOAL", row["source_path"])

        indicator_node = f"policy_indicator:{row['indicator_id']}"
        add_node(
            nodes,
            indicator_node,
            "PolicyIndicator",
            row["indicator_id"],
            row["source_path"],
            indicator_text=row["indicator_text"],
            variable_principal=row["variable_principal"],
            disaggregated=row["disaggregated"],
        )
        add_edge(edges, indicator_node, target_node, "MEASURES_TARGET", row["source_path"])
        add_edge(edges, policy_source_node, indicator_node, "DECLARES_POLICY_INDICATOR", row["source_path"])

    return (
        sorted(nodes.values(), key=lambda item: item["node_id"]),
        sorted(edges.values(), key=lambda item: item["edge_id"]),
    )


def output_checksums(output_root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(output_root.rglob("*")):
        if not path.is_file() or path.name == "run-manifest.json":
            continue
        rows.append(
            {
                "path": rel(path),
                "sha256": sha256(path),
                "size_bytes": str(path.stat().st_size),
            }
        )
    return rows


def build(output_root: Path) -> dict[str, int]:
    inventory = build_file_inventory()
    asdi_rows = read_asdi_datasets()
    policy_rows = read_policy_indicators()
    nodes, edges = build_graph(inventory, asdi_rows, policy_rows)

    write_csv(output_root / "tables" / "file_inventory.csv", inventory, ["path", "role", "size_bytes", "sha256"])
    write_csv(
        output_root / "tables" / "asdi_datasets.csv",
        asdi_rows,
        ["dataset_id", "dataset_name", "dataset_type", "sdg_id", "source_path"],
    )
    write_csv(
        output_root / "tables" / "sdg_policy_indicators.csv",
        policy_rows,
        [
            "goal_id",
            "goal_text",
            "target_id",
            "target_text",
            "indicator_id",
            "indicator_text",
            "variable_principal",
            "disaggregated",
            "source_path",
        ],
    )
    write_csv(output_root / "graph" / "nodes.csv", nodes, ["node_id", "label", "name", "source_path", "attributes_json"])
    write_csv(
        output_root / "graph" / "edges.csv",
        edges,
        ["edge_id", "source_id", "target_id", "edge_type", "source_path", "attributes_json"],
    )

    counts = {
        "input_files": len(inventory),
        "asdi_datasets": len(asdi_rows),
        "policy_indicators": len(policy_rows),
        "graph_nodes": len(nodes),
        "graph_edges": len(edges),
    }
    write_json(output_root / "manifests" / "summary.json", counts)

    manifest = {
        "run_id": "reproducible-scholarship-v0",
        "created_at_utc": "deterministic-build",
        "repository": "https://github.com/ekaropolus/recommender_and_graph_spp",
        "scope": "Part II reproducible layer generated only from committed repository inputs.",
        "generator": "scripts/build_reproducible_scholarship.py",
        "inputs": inventory,
        "outputs": output_checksums(output_root),
        "counts": counts,
        "limitations": [
            "External source URLs and access dates remain incomplete for several historical tables.",
            "Neo4j database reconstruction is represented as graph CSV artifacts; Cypher migrations remain a publication task.",
            "The DOI field is intentionally omitted until an archival release is minted.",
        ],
    }
    write_json(output_root / "manifests" / "run-manifest.json", manifest)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="Directory where reproducible-scholarship outputs are written.",
    )
    args = parser.parse_args()

    counts = build(args.output_root)
    print(json.dumps(counts, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
