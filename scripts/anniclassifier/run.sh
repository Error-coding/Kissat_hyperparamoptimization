#!/bin/sh
spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC

OUT="/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scriptout/anniclassifier/liskov/random_forest_top29.out"
ERR="/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scriptout/anniclassifier/liskov/random_forest_top29.err"

python3 /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts/anniclassifier/anni.py  > $OUT 2> $ERR