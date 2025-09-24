#!/usr/bin/env python3
"""
Bitbucket workspace repository enumerator and concurrent cloner using API Token.

- Auth: Bitbucket API Token (Bearer) with minimal scopes: repository:read, project:read
- Discovers repositories in a workspace, optionally filtered by project keys
- Optionally skips repositories over a size limit
- Clones via SSH using existing local SSH key configuration

Usage example:
  python scripts/bitbucket_clone_by_project.py \
    --workspace aeaverification \
    --projects AEJAPPLIED,AEJMACRO,AEJMICRO,AEJPOLICY,AER,JEL,JEP,PUBLIC,TRAC \
    --token $BITBUCKET_TOKEN \
    --target /Users/startup/Downloads/lars/aea_replication_packages \
    --concurrency 4 \
    --size-limit-mb 400

This script depends only on the Python standard library.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import ssl
import subprocess
from typing import Dict, Iterable, List, Optional, Tuple
import base64


API_BASE = "https://api.bitbucket.org/2.0"


def human_mb(num_bytes: Optional[int]) -> str:
    if num_bytes is None:
        return "unknown"
    return f"{num_bytes / (1024*1024):.1f} MB"


def _ssl_context_with_certifi() -> Optional[ssl.SSLContext]:
    """Create an SSL context that trusts certifi CA bundle when available."""
    try:
        import certifi  # type: ignore

        context = ssl.create_default_context(cafile=certifi.where())
        return context
    except Exception:
        try:
            return ssl.create_default_context()
        except Exception:
            return None


def fetch_all_repos(
    workspace: str,
    token: str,
    project_keys: Optional[Iterable[str]] = None,
    username: Optional[str] = None,
) -> List[Dict]:
    """Fetch all repositories for a workspace via Bitbucket API v2 with pagination.

    Returns list of dicts with at least keys: slug, size, project.key
    """
    if username:
        userpass = f"{username}:{token}".encode("utf-8")
        b64 = base64.b64encode(userpass).decode("ascii")
        headers = {"Authorization": f"Basic {b64}"}
    else:
        headers = {"Authorization": f"Bearer {token}"}
    fields = "values.slug,values.size,values.project.key,next"
    url = f"{API_BASE}/repositories/{urllib.parse.quote(workspace)}?pagelen=100&fields={fields}"

    repos: List[Dict] = []
    seen = 0
    context = _ssl_context_with_certifi()
    while url:
        req = urllib.request.Request(url, headers=headers)
        if context is not None:
            resp_obj = urllib.request.urlopen(req, context=context)
        else:
            resp_obj = urllib.request.urlopen(req)
        with resp_obj as resp:
            data = json.loads(resp.read().decode("utf-8"))
        values = data.get("values", [])
        repos.extend(values)
        seen += len(values)
        url = data.get("next")
    if project_keys:
        project_keys_upper = {k.upper() for k in project_keys}
        repos = [r for r in repos if r.get("project", {}).get("key", "").upper() in project_keys_upper]
    return repos


def build_ssh_url(workspace: str, slug: str) -> str:
    # short SSH form is typically supported
    return f"git@bitbucket.org:{workspace}/{slug}.git"


def clone_repo(target_dir: str, ssh_url: str, retries: int = 2, timeout_sec: int = 1800) -> Tuple[str, int]:
    """Clone a repository via SSH with shallow depth. Returns (repo_dir, return_code)."""
    repo_name = os.path.splitext(os.path.basename(ssh_url))[0]
    dest = os.path.join(target_dir, repo_name)
    if os.path.isdir(dest) and os.path.isdir(os.path.join(dest, ".git")):
        return dest, 0
    cmd = [
        "git",
        "clone",
        "--depth=1",
        ssh_url,
        dest,
    ]
    attempt = 0
    while True:
        attempt += 1
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout_sec)
            rc = proc.returncode
            if rc == 0:
                return dest, 0
            if attempt > retries:
                sys.stderr.write(proc.stdout.decode("utf-8", errors="ignore"))
                return dest, rc
            time.sleep(2 * attempt)
        except subprocess.TimeoutExpired:
            if attempt > retries:
                return dest, 124
            time.sleep(2 * attempt)


def main() -> int:
    parser = argparse.ArgumentParser(description="Bitbucket auto-discover and clone repositories by project")
    parser.add_argument("--workspace", required=True, help="Bitbucket workspace id, e.g., aeaverification")
    parser.add_argument("--projects", default="", help="Comma-separated project keys to include; empty for all")
    parser.add_argument("--token", default=os.environ.get("BITBUCKET_TOKEN", ""), help="Bitbucket API token (Bearer)")
    parser.add_argument("--target", default=os.path.expanduser("~/Downloads/lars/aea_replication_packages"), help="Target directory to clone into")
    parser.add_argument("--concurrency", type=int, default=4, help="Number of concurrent clones")
    parser.add_argument("--size-limit-mb", type=int, default=0, help="Skip repos larger than this size (MB); 0 disables")
    parser.add_argument("--dry-run", action="store_true", help="List what would be cloned without executing")
    args = parser.parse_args()

    if not args.token:
        print("ERROR: Missing API token. Provide --token or set BITBUCKET_TOKEN.", file=sys.stderr)
        return 2

    project_keys = [p.strip() for p in args.projects.split(",") if p.strip()] or None
    os.makedirs(args.target, exist_ok=True)

    print("Enumerating repositories ...", file=sys.stderr)
    repos = fetch_all_repos(args.workspace, args.token, project_keys, username=os.environ.get("BITBUCKET_USERNAME"))
    print(f"Discovered {len(repos)} repositories in workspace '{args.workspace}'", file=sys.stderr)

    selected: List[Tuple[str, Dict]] = []
    for r in repos:
        slug = r.get("slug")
        size = r.get("size")  # bytes or None
        if not slug:
            continue
        if args.size_limit_mb and isinstance(size, int):
            if size > args.size_limit_mb * 1024 * 1024:
                print(f"Skip {slug} due to size {human_mb(size)} > {args.size_limit_mb} MB", file=sys.stderr)
                continue
        selected.append((slug, r))

    print(f"Selected {len(selected)} repositories for cloning", file=sys.stderr)
    if args.dry_run:
        for slug, r in selected:
            ssh_url = build_ssh_url(args.workspace, slug)
            pj = r.get("project", {}).get("key", "")
            size = r.get("size")
            print(f"[DRY] {slug} | project={pj} | size={human_mb(size)} | {ssh_url}")
        return 0

    work_items = [(build_ssh_url(args.workspace, slug), slug) for slug, _ in selected]

    errors: List[Tuple[str, int]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
        fut_to_repo = {pool.submit(clone_repo, args.target, ssh_url): slug for ssh_url, slug in work_items}
        for fut in concurrent.futures.as_completed(fut_to_repo):
            slug = fut_to_repo[fut]
            try:
                dest, rc = fut.result()
            except Exception as exc:  # noqa: BLE001
                print(f"FAIL {slug}: exception {exc}", file=sys.stderr)
                errors.append((slug, -1))
                continue
            if rc == 0:
                print(f"OK   {slug} -> {dest}")
            else:
                print(f"FAIL {slug} (rc={rc})", file=sys.stderr)
                errors.append((slug, rc))

    if errors:
        print(f"Completed with {len(errors)} failures", file=sys.stderr)
        return 1
    print("All clones completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())


