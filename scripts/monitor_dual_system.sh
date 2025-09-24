#!/bin/bash

# Monitor script for dual download system (original + complementary parallel)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Original system logs
SUCCESS_LOG="$BASE_DIR/clone_success.log"
ERROR_LOG="$BASE_DIR/clone_errors.log"
QUEUE_FILE="$BASE_DIR/REPO_QUEUE.txt"

# Complementary system logs
COMPLEMENT_SUCCESS="$BASE_DIR/complement_success.log"
COMPLEMENT_ERRORS="$BASE_DIR/complement_errors.log"
COMPLEMENT_LOG="$BASE_DIR/complement_clone.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

get_counts() {
    # Original system
    local orig_success=0
    local orig_errors=0

    if [ -f "$SUCCESS_LOG" ]; then
        orig_success=$(grep -c "^[^[:space:]]" "$SUCCESS_LOG" 2>/dev/null || echo "0")
    fi

    if [ -f "$ERROR_LOG" ]; then
        orig_errors=$(grep -E "^(aearep|AEAREP|train|TRAIN)" "$ERROR_LOG" 2>/dev/null | wc -l || echo "0")
    fi

    # Complementary system
    local comp_success=0
    local comp_errors=0

    if [ -f "$COMPLEMENT_SUCCESS" ]; then
        comp_success=$(grep -c "^[^[:space:]]" "$COMPLEMENT_SUCCESS" 2>/dev/null || echo "0")
    fi

    if [ -f "$COMPLEMENT_ERRORS" ]; then
        comp_errors=$(grep -c "^[^[:space:]]" "$COMPLEMENT_ERRORS" 2>/dev/null || echo "0")
    fi

    # Total counts
    local total_success=$((orig_success + comp_success))
    local total_errors=$((orig_errors + comp_errors))
    local total_processed=$((total_success + total_errors))

    # Actual directories on disk
    local actual_dirs=$(ls -d aearep* AEAREP* train* TRAIN* 2>/dev/null | wc -l || echo "0")

    # Total repositories
    local total_repos=0
    if [ -f "$QUEUE_FILE" ]; then
        total_repos=$(wc -l < "$QUEUE_FILE")
    fi

    echo "$orig_success $orig_errors $comp_success $comp_errors $total_success $total_errors $total_processed $actual_dirs $total_repos"
}

show_progress() {
    read orig_success orig_errors comp_success comp_errors total_success total_errors total_processed actual_dirs total_repos <<< $(get_counts)

    local remaining=$((total_repos - total_processed))
    local percentage=0

    if [ $total_repos -gt 0 ]; then
        percentage=$((total_processed * 100 / total_repos))
    fi

    echo -e "${CYAN}================================${NC}"
    echo -e "${CYAN}    DUAL SYSTEM PROGRESS${NC}"
    echo -e "${CYAN}================================${NC}"
    echo -e "Total repositories: $total_repos"
    echo -e "${GREEN}Total successfully cloned: $total_success${NC}"
    echo -e "${RED}Total failed: $total_errors${NC}"
    echo -e "${BLUE}Total processed: $total_processed${NC}"
    echo -e "${YELLOW}Remaining: $remaining${NC}"
    echo -e "${PURPLE}Actual directories on disk: $actual_dirs${NC}"
    echo -e "Overall progress: ${percentage}%"
    echo ""

    echo -e "${BLUE}--- ORIGINAL SYSTEM ---${NC}"
    echo -e "${GREEN}Original successes: $orig_success${NC}"
    echo -e "${RED}Original failures: $orig_errors${NC}"
    echo ""

    echo -e "${PURPLE}--- COMPLEMENTARY SYSTEM ---${NC}"
    echo -e "${GREEN}Complement successes: $comp_success${NC}"
    echo -e "${RED}Complement failures: $comp_errors${NC}"

    # Check if complementary system is running
    if pgrep -f "complementary_parallel_clone" > /dev/null; then
        echo -e "${CYAN}Status: Complementary system is RUNNING${NC}"
    else
        echo -e "${YELLOW}Status: Complementary system is STOPPED${NC}"
    fi
    echo ""

    # Show recent successes from both systems
    echo -e "${GREEN}Last 5 successful clones (combined):${NC}"
    {
        if [ -f "$SUCCESS_LOG" ]; then
            tail -5 "$SUCCESS_LOG" 2>/dev/null | sed 's/^/  [ORIG] ✅ /'
        fi
        if [ -f "$COMPLEMENT_SUCCESS" ]; then
            tail -5 "$COMPLEMENT_SUCCESS" 2>/dev/null | sed 's/^/  [COMP] ✅ /'
        fi
    } | tail -5

    echo ""

    # Show download rate estimate
    if [ -f "$COMPLEMENT_LOG" ]; then
        local start_time=$(head -1 "$COMPLEMENT_LOG" 2>/dev/null | grep -o '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]' || echo "")
        if [ -n "$start_time" ]; then
            local current_time=$(date '+%H:%M:%S')
            echo -e "${CYAN}Complement system started: $start_time${NC}"
        fi
    fi
}

watch_progress() {
    while true; do
        clear
        show_progress
        echo ""
        echo -e "${BLUE}Press Ctrl+C to stop monitoring${NC}"
        echo -e "${BLUE}Last updated: $(date)${NC}"

        # Show process status
        if pgrep -f "batch_clone_aea_repos" > /dev/null; then
            echo -e "${GREEN}Original system: RUNNING${NC}"
        else
            echo -e "${YELLOW}Original system: STOPPED${NC}"
        fi

        if pgrep -f "complementary_parallel_clone" > /dev/null; then
            echo -e "${GREEN}Complementary system: RUNNING${NC}"
        else
            echo -e "${YELLOW}Complementary system: STOPPED${NC}"
        fi

        sleep 10
    done
}

case "${1:-watch}" in
    "once")
        show_progress
        ;;
    "watch")
        echo "Starting continuous monitoring of dual system..."
        echo "Press Ctrl+C to stop"
        sleep 2
        watch_progress
        ;;
    "summary")
        show_progress
        echo ""
        echo -e "${CYAN}=== DIRECTORY BREAKDOWN ===${NC}"
        echo -e "Directories by prefix:"
        for prefix in aearep AEAREP train TRAIN; do
            local count=$(ls -d ${prefix}* 2>/dev/null | wc -l || echo "0")
            echo -e "  ${prefix}*: $count directories"
        done
        echo ""
        echo -e "${CYAN}=== SYSTEM STATUS ===${NC}"
        if pgrep -f "batch_clone_aea_repos" > /dev/null; then
            echo -e "${GREEN}✓ Original system is running${NC}"
        else
            echo -e "${YELLOW}○ Original system stopped${NC}"
        fi

        if pgrep -f "complementary_parallel_clone" > /dev/null; then
            echo -e "${GREEN}✓ Complementary system is running${NC}"
        else
            echo -e "${YELLOW}○ Complementary system stopped${NC}"
        fi
        ;;
    *)
        echo "Usage: $0 [once|watch|summary]"
        echo "  once    - Show progress once and exit"
        echo "  watch   - Continuously monitor progress (default)"
        echo "  summary - Show detailed summary with system status"
        ;;
esac