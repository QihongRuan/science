#!/bin/bash

# Batch clone script for AEA Bitbucket repositories
# This script reads repository names from REPO_QUEUE.txt and clones them from Bitbucket

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
QUEUE_FILE="$BASE_DIR/REPO_QUEUE.txt"
LOG_FILE="$BASE_DIR/clone_batch.log"
SUCCESS_LOG="$BASE_DIR/clone_success.log"
ERROR_LOG="$BASE_DIR/clone_errors.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Initialize log files
echo "Batch clone started at $(date)" > "$LOG_FILE"
echo "Successful clones:" > "$SUCCESS_LOG"
echo "Failed clones:" > "$ERROR_LOG"

# Check if queue file exists
if [ ! -f "$QUEUE_FILE" ]; then
    echo -e "${RED}Error: REPO_QUEUE.txt not found at $QUEUE_FILE${NC}"
    exit 1
fi

# Count total repositories
TOTAL_REPOS=$(wc -l < "$QUEUE_FILE")
echo -e "${BLUE}Found $TOTAL_REPOS repositories to clone${NC}"

# Initialize counters
SUCCESS_COUNT=0
ERROR_COUNT=0
SKIP_COUNT=0
CURRENT=0

# Function to clone a single repository
clone_repo() {
    local repo_name="$1"
    local current_num="$2"
    local total="$3"

    echo -e "${BLUE}[$current_num/$total] Processing: $repo_name${NC}"

    # Check if directory already exists
    if [ -d "$repo_name" ]; then
        echo -e "${YELLOW}  → Skipping $repo_name (directory already exists)${NC}"
        echo "[$current_num/$total] SKIPPED: $repo_name (directory exists)" >> "$LOG_FILE"
        return 2
    fi

    # Clone the repository
    echo "  → Cloning from git@bitbucket.org:aeaverification/$repo_name.git"
    if git clone "git@bitbucket.org:aeaverification/$repo_name.git" 2>> "$ERROR_LOG"; then
        echo -e "${GREEN}  ✅ Successfully cloned $repo_name${NC}"
        echo "[$current_num/$total] SUCCESS: $repo_name" >> "$LOG_FILE"
        echo "$repo_name" >> "$SUCCESS_LOG"
        return 0
    else
        echo -e "${RED}  ❌ Failed to clone $repo_name${NC}"
        echo "[$current_num/$total] ERROR: $repo_name" >> "$LOG_FILE"
        echo "$repo_name" >> "$ERROR_LOG"
        return 1
    fi
}

# Process each repository in the queue
while IFS= read -r repo_name; do
    # Skip empty lines
    [ -z "$repo_name" ] && continue

    CURRENT=$((CURRENT + 1))

    clone_repo "$repo_name" "$CURRENT" "$TOTAL_REPOS"
    result=$?

    case $result in
        0) SUCCESS_COUNT=$((SUCCESS_COUNT + 1)) ;;
        1) ERROR_COUNT=$((ERROR_COUNT + 1)) ;;
        2) SKIP_COUNT=$((SKIP_COUNT + 1)) ;;
    esac

    # Brief pause to avoid overwhelming the server
    sleep 0.5

done < "$QUEUE_FILE"

# Final summary
echo ""
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}     BATCH CLONE SUMMARY${NC}"
echo -e "${BLUE}================================${NC}"
echo -e "Total repositories: $TOTAL_REPOS"
echo -e "${GREEN}Successfully cloned: $SUCCESS_COUNT${NC}"
echo -e "${YELLOW}Skipped (exists): $SKIP_COUNT${NC}"
echo -e "${RED}Failed to clone: $ERROR_COUNT${NC}"
echo ""
echo "Logs saved to:"
echo "  - Full log: $LOG_FILE"
echo "  - Success log: $SUCCESS_LOG"
echo "  - Error log: $ERROR_LOG"

# Final log entry
echo "" >> "$LOG_FILE"
echo "Batch clone completed at $(date)" >> "$LOG_FILE"
echo "Summary: $SUCCESS_COUNT success, $SKIP_COUNT skipped, $ERROR_COUNT errors" >> "$LOG_FILE"

# Exit with appropriate code
if [ $ERROR_COUNT -gt 0 ]; then
    exit 1
else
    exit 0
fi