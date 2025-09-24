#!/bin/bash

# Complementary parallel clone system - works alongside existing process
# Identifies unprocessed repos and downloads them in parallel without conflicts

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
QUEUE_FILE="$BASE_DIR/REPO_QUEUE.txt"
SUCCESS_LOG="$BASE_DIR/clone_success.log"
ERROR_LOG="$BASE_DIR/clone_errors.log"

# New logs for complementary system
REMAINING_QUEUE="$BASE_DIR/remaining_repos.txt"
COMPLEMENT_LOG="$BASE_DIR/complement_clone.log"
COMPLEMENT_SUCCESS="$BASE_DIR/complement_success.log"
COMPLEMENT_ERRORS="$BASE_DIR/complement_errors.log"

# Configuration
MAX_PARALLEL_JOBS=4  # Conservative to not overwhelm alongside existing process
MAX_RETRIES=3
RETRY_DELAY=8
CLONE_TIMEOUT=300
UPDATE_INTERVAL=30   # Check for updates every 30 seconds

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Initialize logs
echo "Complementary parallel clone started at $(date)" > "$COMPLEMENT_LOG"
echo "Complementary successes:" > "$COMPLEMENT_SUCCESS"
echo "Complementary errors:" > "$COMPLEMENT_ERRORS"

# Function to identify remaining repositories
identify_remaining_repos() {
    local iteration="$1"

    echo -e "${CYAN}[Scan $iteration] Identifying remaining repositories...${NC}"

    # Get all repos from queue
    local total_repos=$(wc -l < "$QUEUE_FILE")

    # Get already processed repos (both success and failed)
    local processed_repos=$(mktemp)

    # Extract successful repos
    if [ -f "$SUCCESS_LOG" ]; then
        grep -E "^(aearep|AEAREP|train|TRAIN)" "$SUCCESS_LOG" 2>/dev/null >> "$processed_repos" || true
    fi

    # Extract failed repos (repo names from error log)
    if [ -f "$ERROR_LOG" ]; then
        grep -E "^(aearep|AEAREP|train|TRAIN)" "$ERROR_LOG" 2>/dev/null >> "$processed_repos" || true
    fi

    # Extract repos from complement logs
    if [ -f "$COMPLEMENT_SUCCESS" ]; then
        grep -E "^(aearep|AEAREP|train|TRAIN)" "$COMPLEMENT_SUCCESS" 2>/dev/null >> "$processed_repos" || true
    fi

    # Get existing directories (already successfully cloned)
    ls -d aearep* AEAREP* train* TRAIN* 2>/dev/null | sed 's|.*/||' >> "$processed_repos" || true

    # Sort and deduplicate processed repos
    sort "$processed_repos" | uniq > "${processed_repos}.clean"

    # Find remaining repos (in queue but not processed)
    comm -23 <(sort "$QUEUE_FILE") "${processed_repos}.clean" > "$REMAINING_QUEUE"

    local remaining_count=$(wc -l < "$REMAINING_QUEUE")
    local processed_count=$(wc -l < "${processed_repos}.clean")

    echo -e "${BLUE}[Scan $iteration] Status: $processed_count processed, $remaining_count remaining of $total_repos total${NC}"

    # Cleanup
    rm -f "$processed_repos" "${processed_repos}.clean"

    echo "$remaining_count"
}

# Function to clone with retries (similar to previous but with conflict avoidance)
clone_repo_smart() {
    local repo_name="$1"
    local attempt="$2"
    local max_attempts="$3"
    local worker_id="$4"

    # Double-check if repo was processed by main process while we were working
    if [ -d "$repo_name" ] || grep -q "^${repo_name}$" "$SUCCESS_LOG" 2>/dev/null; then
        echo -e "${GREEN}[Worker $worker_id] ⏭️ Skipping $repo_name (processed by main process)${NC}"
        return 2
    fi

    local attempt_suffix=""
    if [ $attempt -gt 1 ]; then
        attempt_suffix=" (retry $((attempt-1)))"
    fi

    echo -e "${PURPLE}[Worker $worker_id] Processing: $repo_name$attempt_suffix${NC}"

    # Clone with timeout
    if timeout $CLONE_TIMEOUT git clone "git@bitbucket.org:aeaverification/$repo_name.git" 2>/dev/null; then
        echo -e "${GREEN}[Worker $worker_id] ✅ Successfully cloned $repo_name${NC}"
        echo "$repo_name" >> "$COMPLEMENT_SUCCESS"
        echo "COMPLEMENT_SUCCESS: $repo_name (attempt $attempt)" >> "$COMPLEMENT_LOG"
        return 0
    else
        echo -e "${RED}[Worker $worker_id] ❌ Failed to clone $repo_name (attempt $attempt)${NC}"

        if [ $attempt -lt $max_attempts ]; then
            echo -e "${YELLOW}[Worker $worker_id] → Retrying $repo_name in $RETRY_DELAY seconds...${NC}"
            sleep $RETRY_DELAY
            clone_repo_smart "$repo_name" $((attempt+1)) $max_attempts $worker_id
            return $?
        else
            echo "$repo_name" >> "$COMPLEMENT_ERRORS"
            echo "COMPLEMENT_FAILED: $repo_name (all attempts failed)" >> "$COMPLEMENT_LOG"
            return 1
        fi
    fi
}

# Function to process a batch of repos
process_batch() {
    local batch_file="$1"
    local worker_id="$2"

    while IFS= read -r repo_name; do
        [ -z "$repo_name" ] && continue

        # Skip if already processed
        if [ -d "$repo_name" ]; then
            echo -e "${YELLOW}[Worker $worker_id] ⏭️ $repo_name already exists${NC}"
            continue
        fi

        clone_repo_smart "$repo_name" 1 $MAX_RETRIES $worker_id

        # Small delay between repos
        sleep 2

    done < "$batch_file"
}

# Main processing loop
main_loop() {
    local iteration=1

    while true; do
        # Identify remaining repositories
        local remaining_count=$(identify_remaining_repos $iteration)

        if [ $remaining_count -eq 0 ]; then
            echo -e "${GREEN}🎉 All repositories processed! No remaining work.${NC}"
            break
        fi

        echo -e "${BLUE}Starting complementary parallel processing of $remaining_count repositories...${NC}"

        # Split remaining repos into batches
        local repos_per_batch=$((remaining_count / MAX_PARALLEL_JOBS + 1))

        # Create batch files
        split -l $repos_per_batch "$REMAINING_QUEUE" "${BASE_DIR}/batch_"
        local batch_files=(${BASE_DIR}/batch_*)

        # Start parallel workers
        declare -a worker_pids=()
        for i in "${!batch_files[@]}"; do
            if [ $i -ge $MAX_PARALLEL_JOBS ]; then
                break
            fi

            local batch_file="${batch_files[$i]}"
            local batch_size=$(wc -l < "$batch_file")

            if [ $batch_size -gt 0 ]; then
                echo -e "${PURPLE}Starting Complement Worker $((i+1)) with $batch_size repositories${NC}"
                process_batch "$batch_file" $((i+1)) &
                worker_pids+=($!)
            fi
        done

        if [ ${#worker_pids[@]} -gt 0 ]; then
            echo -e "${BLUE}Started ${#worker_pids[@]} complement workers alongside main process${NC}"

            # Wait for workers to complete
            for pid in "${worker_pids[@]}"; do
                wait $pid
            done

            echo -e "${BLUE}Complement workers completed iteration $iteration${NC}"
        fi

        # Cleanup batch files
        rm -f "${BASE_DIR}/batch_"*

        iteration=$((iteration+1))

        # Wait before next iteration to let main process work
        echo -e "${CYAN}Waiting $UPDATE_INTERVAL seconds before next scan...${NC}"
        sleep $UPDATE_INTERVAL
    done
}

# Function to also retry previously failed repos
retry_previous_failures() {
    echo -e "${YELLOW}🔄 Starting retry of previously failed repositories...${NC}"

    if [ ! -f "$ERROR_LOG" ] || [ ! -s "$ERROR_LOG" ]; then
        echo -e "${BLUE}No previous failures to retry.${NC}"
        return
    fi

    # Extract unique failed repo names
    local failed_repos=$(mktemp)
    grep -E "^(aearep|AEAREP|train|TRAIN)" "$ERROR_LOG" 2>/dev/null | sort -u > "$failed_repos" || true

    local failed_count=$(wc -l < "$failed_repos")

    if [ $failed_count -eq 0 ]; then
        echo -e "${BLUE}No failed repository names found to retry.${NC}"
        rm -f "$failed_repos"
        return
    fi

    echo -e "${YELLOW}Found $failed_count previously failed repositories to retry${NC}"

    # Process failed repos with retry workers (fewer parallel jobs for retries)
    local retry_workers=2
    local repos_per_worker=$((failed_count / retry_workers + 1))

    split -l $repos_per_worker "$failed_repos" "${BASE_DIR}/retry_batch_"
    local retry_batch_files=(${BASE_DIR}/retry_batch_*)

    declare -a retry_pids=()
    for i in "${!retry_batch_files[@]}"; do
        if [ $i -ge $retry_workers ]; then
            break
        fi

        local batch_file="${retry_batch_files[$i]}"
        local batch_size=$(wc -l < "$batch_file")

        if [ $batch_size -gt 0 ]; then
            echo -e "${YELLOW}Starting Retry Worker $((i+1)) with $batch_size failed repositories${NC}"
            process_batch "$batch_file" "R$((i+1))" &
            retry_pids+=($!)
        fi
    done

    # Wait for retry workers
    for pid in "${retry_pids[@]}"; do
        wait $pid
    done

    # Cleanup
    rm -f "$failed_repos" "${BASE_DIR}/retry_batch_"*

    echo -e "${YELLOW}🔄 Retry process completed${NC}"
}

# Start the process
echo -e "${CYAN}🚀 Starting complementary parallel clone system...${NC}"
echo -e "${CYAN}This will work alongside your current download without conflicts${NC}"

# First, retry previous failures
retry_previous_failures

# Then start main processing loop
main_loop

# Final statistics
SUCCESS_COUNT=$(grep -c "^[^[:space:]]" "$COMPLEMENT_SUCCESS" 2>/dev/null || echo "0")
ERROR_COUNT=$(grep -c "^[^[:space:]]" "$COMPLEMENT_ERRORS" 2>/dev/null || echo "0")
TOTAL_DIRS=$(ls -d aearep* AEAREP* train* TRAIN* 2>/dev/null | wc -l)

echo ""
echo -e "${CYAN}================================${NC}"
echo -e "${CYAN}  COMPLEMENTARY SYSTEM SUMMARY${NC}"
echo -e "${CYAN}================================${NC}"
echo -e "${GREEN}Repositories cloned by complement system: $SUCCESS_COUNT${NC}"
echo -e "${RED}Failed in complement system: $ERROR_COUNT${NC}"
echo -e "${BLUE}Total directories on disk: $TOTAL_DIRS${NC}"
echo -e "${PURPLE}Parallel workers used: $MAX_PARALLEL_JOBS${NC}"
echo ""
echo "Logs:"
echo "  - Complement log: $COMPLEMENT_LOG"
echo "  - Complement successes: $COMPLEMENT_SUCCESS"
echo "  - Complement errors: $COMPLEMENT_ERRORS"

echo "" >> "$COMPLEMENT_LOG"
echo "Complementary system completed at $(date)" >> "$COMPLEMENT_LOG"
echo "Final stats: $SUCCESS_COUNT success, $ERROR_COUNT errors, $TOTAL_DIRS total dirs" >> "$COMPLEMENT_LOG"

echo -e "${GREEN}🎉 Complementary parallel system completed!${NC}"