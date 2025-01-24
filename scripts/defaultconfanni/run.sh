#!/bin/sh
spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC

OUT="/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scriptout/defaultconfanni/liskov/anni.out"
ERR="/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scriptout/defaultconfanni/liskov/anni.err"

python3 /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts/defaultconfanni/defaultparallel.py  > $OUT 2> $ERR