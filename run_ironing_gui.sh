#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $SCRIPT_DIR
IRON_SCRIPT="$SCRIPT_DIR/iron_bpms.py"
echo $IRON_SCRIPT
echo "Usage: $0 num_samples bsa_mode iron_mode"
if [ "$#" -eq 3 ]; then
    echo "Using provided args"
    pydm -m  "num=$1, mode=$2, iron_mode=$3" $IRON_SCRIPT&
else
    pydm -m  "num=50, mode=Inclusion, iron_mode=0" $IRON_SCRIPT&
fi
