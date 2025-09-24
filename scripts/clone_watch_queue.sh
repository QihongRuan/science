#!/bin/bash
set -euo pipefail

# Config
WORKSPACE="${1:-aeaverification}"
TARGET_DIR="${2:-$HOME/Downloads/lars/aea_replication_packages}"
QUEUE_FILE="${3:-$PWD/REPO_QUEUE.txt}"
CONCURRENCY="${4:-4}"
LOG_FILE="${5:-$PWD/clone_queue.log}"

mkdir -p "$TARGET_DIR"
touch "$QUEUE_FILE" "$LOG_FILE"

log() { echo "[$(date +%F_%T)] $*" | tee -a "$LOG_FILE"; }

clone_one() {
  local slug="$1"
  local ssh="git@bitbucket.org:${WORKSPACE}/${slug}.git"
  local dest="${TARGET_DIR}/${slug}"
  if [ -d "$dest/.git" ]; then
    log "SKIP ${slug} already exists"
    return 0
  fi
  log "CLONE ${slug} -> ${dest}"
  if git clone --depth=1 "$ssh" "$dest" >>"$LOG_FILE" 2>&1; then
    log "OK   ${slug}"
  else
    log "FAIL ${slug}"
  fi
}

log "Watcher started. Workspace=${WORKSPACE}, Target=${TARGET_DIR}, Queue=${QUEUE_FILE}, Concurrency=${CONCURRENCY}"

while true; do
  mapfile -t batch < <(grep -v "^#" "$QUEUE_FILE" | sed 's/\r$//' | awk 'NF' | head -n 100)
  if [ ${#batch[@]} -gt 0 ]; then
    printf "" > "$QUEUE_FILE.tmp"
    tail -n +$(( ${#batch[@]} + 1 )) "$QUEUE_FILE" >> "$QUEUE_FILE.tmp" 2>/dev/null || true
    mv "$QUEUE_FILE.tmp" "$QUEUE_FILE"

    printf "%s\n" "${batch[@]}" | xargs -n1 -P"$CONCURRENCY" -I{} bash -c 'slug="$1"; shift; "$0" "$slug"' clone_one {}
  fi
  sleep 5
done


