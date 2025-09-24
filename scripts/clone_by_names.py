#!/usr/bin/env python3
"""
Concurrent SSH clone for a given list of Bitbucket repo slugs (names).

Usage:
  python scripts/clone_by_names.py \
    --workspace aeaverification \
    --names AEAREP-103,aearep-1016,aearep-1086 \
    --target /Users/startup/Downloads/lars/aea_replication_packages \
    --concurrency 4 \
    --size-limit-mb 0
"""

from __future__ import annotations

import argparse
import concurrent.futures
import os
import subprocess
import sys
import time
from typing import Iterable, List, Tuple


def build_ssh_url(workspace: str, slug: str) -> str:
    return f"git@bitbucket.org:{workspace}/{slug}.git"


def clone_repo(target_dir: str, ssh_url: str, retries: int = 2, timeout_sec: int = 1800) -> Tuple[str, int]:
    repo_name = os.path.splitext(os.path.basename(ssh_url))[0]
    dest = os.path.join(target_dir, repo_name)
    if os.path.isdir(dest) and os.path.isdir(os.path.join(dest, ".git")):
        return dest, 0
    cmd = ["git", "clone", "--depth=1", ssh_url, dest]
    attempt = 0
    while True:
        attempt += 1
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout_sec)
            if proc.returncode == 0:
                return dest, 0
            if attempt > retries:
                sys.stderr.write(proc.stdout.decode("utf-8", errors="ignore"))
                return dest, proc.returncode
            time.sleep(2 * attempt)
        except subprocess.TimeoutExpired:
            if attempt > retries:
                return dest, 124
            time.sleep(2 * attempt)


def main() -> int:
    parser = argparse.ArgumentParser(description="Concurrent SSH clone by repo names")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--names", required=True, help="Comma-separated repo slugs")
    parser.add_argument("--target", required=True)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    names: List[str] = [n.strip() for n in args.names.split(",") if n.strip()]
    os.makedirs(args.target, exist_ok=True)

    if args.dry_run:
        for n in names:
            print(build_ssh_url(args.workspace, n))
        return 0

    work_items = [(build_ssh_url(args.workspace, n), n) for n in names]

    errors: List[Tuple[str, int]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
        fut_to_repo = {pool.submit(clone_repo, args.target, ssh): name for ssh, name in work_items}
        for fut in concurrent.futures.as_completed(fut_to_repo):
            name = fut_to_repo[fut]
            try:
                dest, rc = fut.result()
            except Exception as exc:  # noqa: BLE001
                print(f"FAIL {name}: exception {exc}", file=sys.stderr)
                errors.append((name, -1))
                continue
            if rc == 0:
                print(f"OK   {name} -> {dest}")
            else:
                print(f"FAIL {name} (rc={rc})", file=sys.stderr)
                errors.append((name, rc))

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())


