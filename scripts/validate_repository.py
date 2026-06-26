#!/usr/bin/env python3
"""Validate research-repository hygiene for the thesis archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "SECURITY.md",
    ".env.example",
    "requirements.txt",
    "docs/thesis-map.md",
    "docs/provenance.md",
    "docs/reproducibility.md",
    "docs/repository-audit.md",
    "ASDI Tables",
    "Public Policies Tables",
    "Google Colab Notebooks",
]

SECRET_PATTERNS = [
    re.compile(r"password\s*=\s*[\"'][^\"']{8,}[\"']", re.IGNORECASE),
    re.compile(r"EAI_PASSWORD[\"']?\s*[\]=:]\s*[\"'][^\"']{8,}[\"']", re.IGNORECASE),
    re.compile(r"neo4j\+s://[a-z0-9-]+\.databases\.neo4j\.io"),
    re.compile(r"(api[_-]?key|secret|token)\s*=\s*[\"'][^\"']{12,}[\"']", re.IGNORECASE),
]

SKIP_DIRS = {".git", "__pycache__", ".ipynb_checkpoints"}
TEXT_EXTENSIONS = {".md", ".py", ".txt", ".csv", ".cff", ".example", ".ipynb", ""}


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_required() -> list[str]:
    errors: list[str] = []
    for item in REQUIRED_PATHS:
        if not (ROOT / item).exists():
            errors.append(f"missing required path: {item}")
    return errors


def check_notebooks() -> list[str]:
    errors: list[str] = []
    for path in (ROOT / "Google Colab Notebooks").glob("*.ipynb"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"invalid notebook JSON: {rel(path)} ({exc})")
            continue
        if "cells" not in data:
            errors.append(f"notebook missing cells: {rel(path)}")
    return errors


def check_secrets() -> list[str]:
    errors: list[str] = []
    for path in iter_files():
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible secret pattern in {rel(path)}")
                break
    return errors


def print_inventory() -> None:
    print("path,size,sha256")
    for path in iter_files():
        print(f"{rel(path)},{path.stat().st_size},{sha256(path)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", action="store_true", help="Print file inventory with SHA-256 checksums.")
    args = parser.parse_args()

    if args.inventory:
        print_inventory()
        return 0

    errors = []
    errors.extend(check_required())
    errors.extend(check_notebooks())
    errors.extend(check_secrets())

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
