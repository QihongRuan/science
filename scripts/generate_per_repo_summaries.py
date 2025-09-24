#!/usr/bin/env python3
"""
Generate per-repo markdown summaries under reports/per_repo.
Summaries include: language counts, README score, presence of master scripts,
dependencies/data statements, file counts, and detected methods (coarse).
"""
from __future__ import annotations

import os
import re
import json
from pathlib import Path
from collections import defaultdict

from analyze_repos import AEARepositoryAnalyzer
from econometric_analysis import EconometricAnalyzer

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE
REPORT_DIR = ROOT / "reports" / "per_repo"
TARGETS = []

# Identify candidate repo dirs (top-level under lars)
for p in ROOT.iterdir():
    if p.is_dir() and not p.name.startswith(".") and p.name not in {"reports", "scripts", "docs", "pdf_text"}:
        if any(k in p.name.lower() for k in ["aearep-", "aer", "aej", "train", "testing", "test-"]):
            TARGETS.append(p)

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Helpers

def detect_languages_quick(repo_path: Path) -> dict[str, int]:
    ext_map = {'.do': 'Stata', '.m': 'MATLAB', '.py': 'Python', '.R': 'R', '.jl': 'Julia'}
    counts = defaultdict(int)
    for ext, lang in ext_map.items():
        counts[lang] += len(list(repo_path.rglob(f"*{ext}")))
    return dict(counts)


def summarize_repo(repo: Path) -> dict:
    analyzer = AEARepositoryAnalyzer(repo)
    analyzer.repos = [repo]
    single = analyzer.analyze_single_repo(repo)

    econ = EconometricAnalyzer(repo)
    methods = econ.analyze_all_repos()
    robust = econ.analyze_robustness_checks()

    return {
        "name": repo.name,
        "path": str(repo),
        "languages": single.get("languages", {}),
        "structure_type": single.get("structure_type"),
        "readme_score": single.get("readme_score"),
        "has_master_script": single.get("has_master_script"),
        "has_data_statement": single.get("has_data_statement"),
        "has_dependencies": single.get("has_dependencies"),
        "code_organization": single.get("code_organization"),
        "statistical_methods": single.get("statistical_methods", []),
        "robustness_counts": {k:int(v) for k,v in robust.items()},
        "language_quick": detect_languages_quick(repo),
        "file_counts": {
            "do": len(list(repo.rglob("*.do"))),
            "R": len(list(repo.rglob("*.R"))),
            "py": len(list(repo.rglob("*.py"))),
            "m": len(list(repo.rglob("*.m"))),
            "md": len(list(repo.rglob("*.md"))),
            "pdf": len(list(repo.rglob("*.pdf"))),
        },
    }


def to_markdown(summary: dict) -> str:
    lines = []
    lines.append(f"# {summary['name']}")
    lines.append("")
    lines.append(f"Path: `{summary['path']}`")
    lines.append("")
    lines.append("## Overview")
    lines.append(f"- Structure: {summary['structure_type']}")
    lines.append(f"- README score: {summary['readme_score']}")
    lines.append(f"- Master script: {summary['has_master_script']}")
    lines.append(f"- Data statement: {summary['has_data_statement']}")
    lines.append(f"- Dependencies documented: {summary['has_dependencies']}")
    lines.append("")
    lines.append("## Languages")
    for k, v in (summary.get("languages") or {}).items():
        lines.append(f"- {k}: {v} files")
    lines.append("")
    lines.append("## Files")
    for k, v in summary["file_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Statistical methods (detected)")
    if summary.get("statistical_methods"):
        lines.append(", ".join(sorted(summary["statistical_methods"])))
    else:
        lines.append("(none detected)")
    lines.append("")
    lines.append("## Robustness mentions (counts)")
    if summary.get("robustness_counts"):
        for k, v in sorted(summary["robustness_counts"].items(), key=lambda x: -x[1])[:10]:
            lines.append(f"- {k}: {v}")
    else:
        lines.append("(none)")
    return "\n".join(lines)


all_summaries = []
for repo in TARGETS:
    try:
        s = summarize_repo(repo)
        all_summaries.append(s)
        (REPORT_DIR / f"{repo.name}.md").write_text(to_markdown(s), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        # Skip problematic repos, continue
        continue

# Write index
index = ["# Per-repo summaries", "", f"Total: {len(all_summaries)}", ""]
for s in sorted(all_summaries, key=lambda x: x["name"].lower()):
    index.append(f"- [{s['name']}](./{s['name']}.md)")
(REPORT_DIR / "README.md").write_text("\n".join(index), encoding="utf-8")

print(f"Generated {len(all_summaries)} per-repo summaries at {REPORT_DIR}")
