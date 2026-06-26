#!/usr/bin/env python3
"""Validate generated Part II reproducible-scholarship artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "reproducible-scholarship" / "outputs"


REQUIRED_FILES = [
    "tables/file_inventory.csv",
    "tables/asdi_datasets.csv",
    "tables/sdg_policy_indicators.csv",
    "graph/nodes.csv",
    "graph/edges.csv",
    "manifests/summary.json",
    "manifests/run-manifest.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def fail(message: str) -> int:
    print(f"FAILED: {message}")
    return 1


def main() -> int:
    for rel_path in REQUIRED_FILES:
        path = OUTPUT_ROOT / rel_path
        if not path.exists():
            return fail(f"missing output file: {rel_path}")

    nodes = read_csv(OUTPUT_ROOT / "graph" / "nodes.csv")
    edges = read_csv(OUTPUT_ROOT / "graph" / "edges.csv")
    asdi_rows = read_csv(OUTPUT_ROOT / "tables" / "asdi_datasets.csv")
    policy_rows = read_csv(OUTPUT_ROOT / "tables" / "sdg_policy_indicators.csv")

    if len(asdi_rows) < 100:
        return fail("ASDI normalized table is unexpectedly small")
    if len(policy_rows) < 200:
        return fail("policy indicator table is unexpectedly small")
    if not nodes or not edges:
        return fail("graph outputs are empty")

    node_ids = {row["node_id"] for row in nodes}
    required_labels = {"ResearchTrack", "SourceFile", "AsdiDataset", "SdgGoal", "SdgTarget", "PolicyIndicator"}
    labels = {row["label"] for row in nodes}
    missing_labels = required_labels - labels
    if missing_labels:
        return fail(f"missing graph labels: {sorted(missing_labels)}")

    for edge in edges:
        if edge["source_id"] not in node_ids:
            return fail(f"edge source does not exist: {edge['edge_id']}")
        if edge["target_id"] not in node_ids:
            return fail(f"edge target does not exist: {edge['edge_id']}")

    manifest = json.loads((OUTPUT_ROOT / "manifests" / "run-manifest.json").read_text(encoding="utf-8"))
    output_checksums = {item["path"]: item["sha256"] for item in manifest["outputs"]}
    for rel_path, expected_sha in output_checksums.items():
        path = ROOT / rel_path
        if not path.exists():
            return fail(f"manifest output missing on disk: {rel_path}")
        if sha256(path) != expected_sha:
            return fail(f"manifest checksum mismatch: {rel_path}")

    print("Reproducible scholarship outputs passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
