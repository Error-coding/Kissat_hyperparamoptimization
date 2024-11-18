#!/bin/sh
spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC
cd /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts
python3 kissatparallel.py 0 10 5