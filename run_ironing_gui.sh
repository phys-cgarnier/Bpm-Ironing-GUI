#!/bin/bash

echo "Usage: $0 num_samples bsa_mode iron_mode"
if [ "$#" -eq 3 ]; then
    echo "Using provided args"
    pydm -m  "num=$1, mode=$2, iron_mode=$3" iron_bpms.py&
else
    pydm -m  "num=25, mode=Inclusion, iron_mode=0" iron_bpms.py 
    
fi

