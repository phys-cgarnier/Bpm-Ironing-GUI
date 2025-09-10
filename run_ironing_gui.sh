#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IRON_SCRIPT="$SCRIPT_DIR/iron_bpms.py"



NUM="${1:-250}"
BSA_MODE="${2:-Inclusion}"
IRON_MODE="${3:-0}"
IRON_SW="${4:-0}"

echo "Launching ironing GUI with ironing Parameters:"
echo "  Number of points $NUM"
echo "  BSA Mode: $BSA_MODE"
echo "  Iron Mode: $IRON_MODE"
echo "  Iron SW Flag: $IRON_SW"

pydm -m  "num=$NUM, mode=$BSA_MODE, iron_mode=$IRON_MODE,iron_sw=$IRON_SW" $IRON_SCRIPT&