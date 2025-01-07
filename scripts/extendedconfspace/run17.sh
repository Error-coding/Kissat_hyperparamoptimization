#!/bin/bash

spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC

OUT="/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scriptout/extend/liskov/$i.out"
ERR="/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scriptout/extend/liskov/$i.err"
python3 /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts/extendedconfspace/extended_optimization.py $i 1800 17 32 > $OUT 2> $ERR
