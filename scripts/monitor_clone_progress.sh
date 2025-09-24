#!/bin/bash

# Monitor script for the batch clone operation
# This script provides real-time progress information

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$BASE_DIR/clone_batch.log"
SUCCESS_LOG="$BASE_DIR/clone_success.log"
ERROR_LOG="$BASE_DIR/clone_errors.log"
QUEUE_FILE="$BASE_DIR/REPO_QUEUE.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to get current counts
get_counts() {
    local success_count=0
    local error_count=0
    local total_repos=0

    if [ -f "$SUCCESS_LOG" ]; then
        success_count=$(grep -v "^Successful clones:" "$SUCCESS_LOG" | grep -c "^[^[:space:]]")
    fi

    if [ -f "$ERROR_LOG" ]; then
        error_count=$(grep -v "^Failed clones:" "$ERROR_LOG" | grep -c "^[^[:space:]]")
    fi

    if [ -f "$QUEUE_FILE" ]; then
        total_repos=$(wc -l < "$QUEUE_FILE")
    fi

    echo "$success_count $error_count $total_repos"
}

# Function to show current progress
show_progress() {
    read success_count error_count total_repos <<< $(get_counts)
    local completed=$((success_count + error_count))
    local remaining=$((total_repos - completed))
    local percentage=0

    if [ $total_repos -gt 0 ]; then
        percentage=$((completed * 100 / total_repos))
    fi

    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}     CLONE PROGRESS MONITOR${NC}"
    echo -e "${BLUE}================================${NC}"
    echo -e "Total repositories: $total_repos"
    echo -e "${GREEN}Successfully cloned: $success_count${NC}"
    echo -e "${RED}Failed to clone: $error_count${NC}"
    echo -e "Completed: $completed"
    echo -e "Remaining: $remaining"
    echo -e "Progress: ${percentage}%"
    echo ""

    # Show last few successful clones
    if [ -f "$SUCCESS_LOG" ] && [ $success_count -gt 0 ]; then
        echo -e "${GREEN}Last 5 successful clones:${NC}"
        tail -5 "$SUCCESS_LOG" | grep -v "^Successful clones:" | sed 's/^/  ✅ /'
        echo ""
    fi

    # Show last few errors
    if [ -f "$ERROR_LOG" ] && [ $error_count -gt 0 ]; then
        echo -e "${RED}Last 5 failed clones:${NC}"
        tail -5 "$ERROR_LOG" | grep -v "^Failed clones:" | sed 's/^/  ❌ /'
        echo ""
    fi
}

# Function to watch progress continuously
watch_progress() {
    while true; do
        clear
        show_progress
        echo "Press Ctrl+C to stop monitoring"
        echo "Last updated: $(date)"
        sleep 5
    done
}

# Main script logic
case "${1:-watch}" in
    "once")
        show_progress
        ;;
    "watch")
        echo "Starting continuous monitoring..."
        echo "Press Ctrl+C to stop"
        sleep 2
        watch_progress
        ;;
    "summary")
        show_progress
        echo "=== DIRECTORY COUNT ==="
        echo "Actual directories found: $(ls -d aearep* 2>/dev/null | wc -l)"
        echo ""
        ;;
    *)
        echo "Usage: $0 [once|watch|summary]"
        echo "  once    - Show progress once and exit"
        echo "  watch   - Continuously monitor progress (default)"
        echo "  summary - Show progress with directory count"
        ;;
esac