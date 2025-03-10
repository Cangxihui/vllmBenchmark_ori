#!/bin/bash

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <model> <base url> <save file key> <version> <mla>"
    exit 1
fi

MODEL=$1
BASE_URL=$2
VERSION=$4
MLA=$5

# CONFIGURATION
NUM_USERS=320
NUM_ROUNDS=10

SYSTEM_PROMPT=50 # Shared system prompt length
CHAT_HISTORY=20000 # User specific chat history length
ANSWER_LEN=100 # Generation length per round

BACKEND="vllm"

run_benchmark() {
    # $1: qps
    # $2: output file
    python benchmarks/benchmark_serving.py \
        --backend $BACKEND \
        --model "$MODEL" \
        --dataset-name random \
        --random-input-len 2000\
        --random-output-len 200\
        --random-prefix-len 0 \
        --num-prompts $SYSTEM_PROMPT \
        --save-result \
        --result-dir ./ \
        --result-filename "$2"\
        --trust-remote-code \
        --request-rate "$1"
}




KEY=$3
MODEL=$1
backend_kqps_model_Version-MLA.json
# Run benchmarks for different QPS values
for qps in 1 2 3 4 5 6 7 8; do
    output_file="${BACKEND}_${qps}qps_output_${VERSION}-${MLA}.json"
    run_benchmark "$qps" "$output_file"
done
