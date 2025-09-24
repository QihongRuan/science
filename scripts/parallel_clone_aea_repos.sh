#!/bin/bash

# Enhanced parallel batch clone script for AEA Bitbucket repositories
# Features: Parallel downloading, retry mechanism, improved error handling

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
QUEUE_FILE="$BASE_DIR/REPO_QUEUE.txt"
LOG_FILE="$BASE_DIR/parallel_clone_batch.log"
SUCCESS_LOG="$BASE_DIR/parallel_clone_success.log"
ERROR_LOG="$BASE_DIR/parallel_clone_errors.log"
RETRY_LOG="$BASE_DIR/parallel_clone_retry.log"
FAILED_QUEUE="$BASE_DIR/failed_repos.txt"

# Configuration
MAX_PARALLEL_JOBS=5  # Number of parallel clone operations
MAX_RETRIES=3        # Maximum retry attempts for failed repositories
RETRY_DELAY=5        # Delay between retries (seconds)
CLONE_TIMEOUT=300    # Timeout for each clone operation (5 minutes)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Initialize log files
echo "Parallel batch clone started at $(date) with $MAX_PARALLEL_JOBS parallel jobs" > "$LOG_FILE"
echo "Successful clones:" > "$SUCCESS_LOG"
echo "Failed clones:" > "$ERROR_LOG"
echo "Retry attempts:" > "$RETRY_LOG"
> "$FAILED_QUEUE"

# Check if queue file exists
if [ ! -f "$QUEUE_FILE" ]; then
    echo -e "${RED}Error: REPO_QUEUE.txt not found at $QUEUE_FILE${NC}"
    exit 1
fi

# Count total repositories
TOTAL_REPOS=$(wc -l < "$QUEUE_FILE")
echo -e "${BLUE}Found $TOTAL_REPOS repositories to clone with $MAX_PARALLEL_JOBS parallel workers${NC}"

# Function to clone a single repository with timeout and retry
clone_repo_with_retry() {
    local repo_name="$1"
    local attempt="$2"
    local max_attempts="$3"
    local job_id="$4"

    local attempt_suffix=""
    if [ $attempt -gt 1 ]; then
        attempt_suffix=" (retry $((attempt-1))/$((max_attempts-1)))"
    fi

    echo -e "${BLUE}[Worker $job_id] Processing: $repo_name$attempt_suffix${NC}"

    # Check if directory already exists
    if [ -d "$repo_name" ]; then
        echo -e "${YELLOW}[Worker $job_id] → Skipping $repo_name (directory already exists)${NC}"
        echo "SKIPPED: $repo_name (directory exists)" >> "$LOG_FILE"
        return 2
    fi

    # Clone with timeout
    echo "[Worker $job_id] → Cloning from git@bitbucket.org:aeaverification/$repo_name.git"

    if timeout $CLONE_TIMEOUT git clone "git@bitbucket.org:aeaverification/$repo_name.git" 2>/dev/null; then
        echo -e "${GREEN}[Worker $job_id] ✅ Successfully cloned $repo_name$attempt_suffix${NC}"
        echo "$repo_name" >> "$SUCCESS_LOG"
        echo "SUCCESS: $repo_name (attempt $attempt)" >> "$LOG_FILE"
        return 0
    else
        local error_code=$?
        echo -e "${RED}[Worker $job_id] ❌ Failed to clone $repo_name$attempt_suffix (exit code: $error_code)${NC}"

        # Log the attempt
        echo "ATTEMPT $attempt: $repo_name failed" >> "$RETRY_LOG"

        if [ $attempt -lt $max_attempts ]; then
            echo -e "${YELLOW}[Worker $job_id] → Will retry $repo_name in $RETRY_DELAY seconds${NC}"
            sleep $RETRY_DELAY
            clone_repo_with_retry "$repo_name" $((attempt+1)) $max_attempts $job_id
            return $?
        else
            echo -e "${RED}[Worker $job_id] → Max retries reached for $repo_name${NC}"
            echo "$repo_name" >> "$FAILED_QUEUE"
            echo "$repo_name" >> "$ERROR_LOG"
            echo "FAILED: $repo_name (all $max_attempts attempts failed)" >> "$LOG_FILE"
            return 1
        fi
    fi
}

# Function to process a batch of repositories
process_repo_batch() {
    local start_line="$1"
    local end_line="$2"
    local job_id="$3"

    sed -n "${start_line},${end_line}p" "$QUEUE_FILE" | while IFS= read -r repo_name; do
        [ -z "$repo_name" ] && continue
        clone_repo_with_retry "$repo_name" 1 $MAX_RETRIES $job_id

        # Small delay to avoid overwhelming the server
        sleep 1
    done
}

# Calculate batch sizes for parallel processing
REPOS_PER_BATCH=$((TOTAL_REPOS / MAX_PARALLEL_JOBS + 1))
echo -e "${BLUE}Processing ~$REPOS_PER_BATCH repositories per worker${NC}"

# Start parallel workers
declare -a worker_pids=()
for ((i=0; i<MAX_PARALLEL_JOBS; i++)); do
    start_line=$((i * REPOS_PER_BATCH + 1))
    end_line=$(((i + 1) * REPOS_PER_BATCH))

    # Don't exceed total number of repos
    if [ $end_line -gt $TOTAL_REPOS ]; then
        end_line=$TOTAL_REPOS
    fi

    # Skip if start_line exceeds total repos
    if [ $start_line -gt $TOTAL_REPOS ]; then
        break
    fi

    echo -e "${PURPLE}Starting Worker $((i+1)) (lines $start_line-$end_line)${NC}"
    process_repo_batch $start_line $end_line $((i+1)) &
    worker_pids+=($!)
done

echo -e "${BLUE}Started ${#worker_pids[@]} parallel workers${NC}"

# Wait for all workers to complete
echo -e "${BLUE}Waiting for all workers to complete...${NC}"
for pid in "${worker_pids[@]}"; do
    wait $pid
done

# Calculate final statistics
SUCCESS_COUNT=$(grep -c "^[^[:space:]]" "$SUCCESS_LOG" 2>/dev/null || echo "0")
ERROR_COUNT=$(grep -c "^[^[:space:]]" "$ERROR_LOG" 2>/dev/null || echo "0")
ACTUAL_DIRS=$(ls -d aearep* AEAREP* train* TRAIN* 2>/dev/null | wc -l)
RETRY_ATTEMPTS=$(grep -c "ATTEMPT" "$RETRY_LOG" 2>/dev/null || echo "0")

# Final summary
echo ""
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}   PARALLEL CLONE SUMMARY${NC}"
echo -e "${BLUE}================================${NC}"
echo -e "Total repositories: $TOTAL_REPOS"
echo -e "${GREEN}Successfully cloned: $SUCCESS_COUNT${NC}"
echo -e "${RED}Failed to clone: $ERROR_COUNT${NC}"
echo -e "${YELLOW}Total retry attempts: $RETRY_ATTEMPTS${NC}"
echo -e "${PURPLE}Actual directories on disk: $ACTUAL_DIRS${NC}"
echo -e "Parallel workers used: ${#worker_pids[@]}"
echo -e "Max retries per repo: $MAX_RETRIES"
echo ""
echo "Logs saved to:"
echo "  - Full log: $LOG_FILE"
echo "  - Success log: $SUCCESS_LOG"
echo "  - Error log: $ERROR_LOG"
echo "  - Retry log: $RETRY_LOG"
echo "  - Failed repos list: $FAILED_QUEUE"

# Final log entry
echo "" >> "$LOG_FILE"
echo "Parallel batch clone completed at $(date)" >> "$LOG_FILE"
echo "Summary: $SUCCESS_COUNT success, $ERROR_COUNT errors, $RETRY_ATTEMPTS retries" >> "$LOG_FILE"

# Exit with appropriate code
if [ $ERROR_COUNT -gt 0 ]; then
    echo -e "${YELLOW}Some repositories failed after all retry attempts.${NC}"
    echo -e "${YELLOW}Check $FAILED_QUEUE for the list of failed repositories.${NC}"
    exit 1
else
    echo -e "${GREEN}All accessible repositories cloned successfully!${NC}"
    exit 0
fi