#!/bin/bash

spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC

cd /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts

for i in $(seq 0 34); do
    OUT="/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scriptout/$i.out"
    ERR="/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scriptout/$i.err"

    if [ ! -f $OUT ]; then
        echo "python3 /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts/kissatparallel.py $i 5000 20 10 > $OUT 2> $ERR" 
    fi
done | parallel -j 16
