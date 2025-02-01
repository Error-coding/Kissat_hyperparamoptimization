#!/bin/sh
spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC

OUT="/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scriptout/topconfseval/1-5.out"
ERR="/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scriptout/topconfseval/1-5.err"

python3 /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts/topconfseval/topconfseval.py  > $OUT 2> $ERR