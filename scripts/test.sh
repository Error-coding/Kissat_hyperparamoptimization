#!/bin/sh
spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC
python3 /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts/smactest.py

