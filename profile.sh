#!/usr/bin/env bash

profile_cmd() {
    if [[ $# -lt 2 ]]; then
        echo "Usage: profile_cmd <repeats> <command> [args...]"
        return 1
    fi

    local repeats="$1"
    shift
    local cmd=("$@")

    if ! [[ "$repeats" =~ ^[1-9][0-9]*$ ]]; then
        echo "Error: <repeats> must be a positive integer."
        return 1
    fi

    local times=()
    for ((i = 0; i < repeats; i++)); do
        local start end elapsed
        start=$(date +%s.%N)
        "${cmd[@]}" > /dev/null 2>&1
        end=$(date +%s.%N)
        elapsed=$(echo "$end - $start" | bc)
        times+=("$elapsed")
    done

    # Calculate average and standard deviation
    local sum=0
    for t in "${times[@]}"; do
        sum=$(echo "$sum + $t" | bc)
    done
    local avg=$(echo "scale=3; $sum / $repeats" | bc)

    local sq_diff_sum=0
    for t in "${times[@]}"; do
        diff=$(echo "$t - $avg" | bc)
        sq_diff=$(echo "$diff * $diff" | bc)
        sq_diff_sum=$(echo "$sq_diff_sum + $sq_diff" | bc)
    done
    local stddev=$(echo "scale=3; sqrt($sq_diff_sum / $repeats)" | bc -l)

    echo "${cmd[*]} --> $avg +/- $stddev sec. ($repeats loops)"
}


profile_cmd $@
