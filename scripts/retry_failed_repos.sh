#!/bin/bash

# Retry failed repositories with enhanced parallel processing
# This script extracts failed repo names from the error log and retries them

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
ERROR_LOG="$BASE_DIR/clone_errors.log"
FAILED_QUEUE="$BASE_DIR/failed_repos_extracted.txt"
RETRY_LOG="$BASE_DIR/retry_failed.log"
RETRY_SUCCESS_LOG="$BASE_DIR/retry_success.log"

# Configuration
MAX_PARALLEL_JOBS=3  # Fewer parallel jobs for retries to be gentler on server
MAX_RETRIES=2        # Retry attempts for each failed repo
RETRY_DELAY=10       # Longer delay between retries
CLONE_TIMEOUT=600    # Longer timeout for retries (10 minutes)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Extracting failed repository names from error log...${NC}"

# Extract failed repository names from the current error log
if [ ! -f "$ERROR_LOG" ]; then
    echo -e "${RED}Error: $ERROR_LOG not found${NC}"
    exit 1
fi

# Extract unique repository names that failed
grep -E "^(aearep|AEAREP|train|TRAIN)" "$ERROR_LOG" | sort -u > "$FAILED_QUEUE"

FAILED_COUNT=$(wc -l < "$FAILED_QUEUE")
echo -e "${YELLOW}Found $FAILED_COUNT unique failed repositories to retry${NC}"

if [ $FAILED_COUNT -eq 0 ]; then
    echo -e "${GREEN}No failed repositories found to retry!${NC}"
    exit 0
fi

# Initialize retry logs
echo "Retry attempt started at $(date)" > "$RETRY_LOG"
echo "Retry successes:" > "$RETRY_SUCCESS_LOG"

# Function to retry a single repository
retry_repo() {
    local repo_name="$1"
    local attempt="$2"
    local max_attempts="$3"
    local worker_id="$4"

    echo -e "${BLUE}[Retry Worker $worker_id] Attempting: $repo_name (attempt $attempt/$max_attempts)${NC}"

    # Check if directory already exists
    if [ -d "$repo_name" ]; then
        echo -e "${GREEN}[Retry Worker $worker_id] ✅ $repo_name already exists (previous success)${NC}"
        echo "$repo_name" >> "$RETRY_SUCCESS_LOG"
        return 0
    fi

    # Clone with timeout and better error handling
    if timeout $CLONE_TIMEOUT git clone "git@bitbucket.org:aeaverification/$repo_name.git" 2>/dev/null; then
        echo -e "${GREEN}[Retry Worker $worker_id] ✅ Successfully cloned $repo_name${NC}"
        echo "$repo_name" >> "$RETRY_SUCCESS_LOG"
        echo "RETRY_SUCCESS: $repo_name (attempt $attempt)" >> "$RETRY_LOG"
        return 0
    else
        echo -e "${RED}[Retry Worker $worker_id] ❌ Failed to clone $repo_name (attempt $attempt)${NC}"
        echo "RETRY_FAILED: $repo_name (attempt $attempt)" >> "$RETRY_LOG"

        if [ $attempt -lt $max_attempts ]; then
            echo -e "${YELLOW}[Retry Worker $worker_id] → Waiting $RETRY_DELAY seconds before next attempt...${NC}"
            sleep $RETRY_DELAY
            retry_repo "$repo_name" $((attempt+1)) $max_attempts $worker_id
            return $?
        else
            return 1
        fi
    fi
}

# Function to process a batch of failed repositories
retry_batch() {
    local start_line="$1"
    local end_line="$2"
    local worker_id="$3"

    sed -n "${start_line},${end_line}p" "$FAILED_QUEUE" | while IFS= read -r repo_name; do
        [ -z "$repo_name" ] && continue
        retry_repo "$repo_name" 1 $MAX_RETRIES $worker_id

        # Longer delay between repos to be gentle on server
        sleep 3
    done
}

# Calculate batch sizes for parallel processing
REPOS_PER_BATCH=$((FAILED_COUNT / MAX_PARALLEL_JOBS + 1))
echo -e "${BLUE}Processing ~$REPOS_PER_BATCH failed repositories per retry worker${NC}"

# Start parallel retry workers
declare -a worker_pids=()
for ((i=0; i<MAX_PARALLEL_JOBS; i++)); do
    start_line=$((i * REPOS_PER_BATCH + 1))
    end_line=$(((i + 1) * REPOS_PER_BATCH))

    if [ $end_line -gt $FAILED_COUNT ]; then
        end_line=$FAILED_COUNT
    fi

    if [ $start_line -gt $FAILED_COUNT ]; then
        break
    fi

    echo -e "${YELLOW}Starting Retry Worker $((i+1)) (lines $start_line-$end_line)${NC}"
    retry_batch $start_line $end_line $((i+1)) &
    worker_pids+=($!)
done

echo -e "${BLUE}Started ${#worker_pids[@]} parallel retry workers${NC}"

# Wait for all retry workers to complete
echo -e "${BLUE}Waiting for all retry workers to complete...${NC}"
for pid in "${worker_pids[@]}"; do
    wait $pid
done

# Calculate final statistics
RETRY_SUCCESS_COUNT=$(grep -c "^[^[:space:]]" "$RETRY_SUCCESS_LOG" 2>/dev/null || echo "0")
STILL_FAILED=$((FAILED_COUNT - RETRY_SUCCESS_COUNT))

# Final summary
echo ""
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}     RETRY SUMMARY${NC}"
echo -e "${BLUE}================================${NC}"
echo -e "Repositories attempted: $FAILED_COUNT"
echo -e "${GREEN}Successfully recovered: $RETRY_SUCCESS_COUNT${NC}"
echo -e "${RED}Still failed: $STILL_FAILED${NC}"
echo -e "Recovery rate: $(( (RETRY_SUCCESS_COUNT * 100) / FAILED_COUNT ))%"
echo ""
echo "Logs saved to:"
echo "  - Retry log: $RETRY_LOG"
echo "  - Retry success log: $RETRY_SUCCESS_LOG"
echo "  - Failed repos list: $FAILED_QUEUE"

echo "" >> "$RETRY_LOG"
echo "Retry attempt completed at $(date)" >> "$RETRY_LOG"
echo "Summary: $RETRY_SUCCESS_COUNT recovered, $STILL_FAILED still failed" >> "$RETRY_LOG"

if [ $STILL_FAILED -gt 0 ]; then
    echo -e "${YELLOW}Some repositories still failed after retry attempts.${NC}"
    exit 1
else
    echo -e "${GREEN}All failed repositories successfully recovered!${NC}"
    exit 0
fi