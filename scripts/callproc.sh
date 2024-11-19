#!/bin/sh
spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC
cd /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts
python3 ./kissatparallel.py $SLURM_PROCID 5000 20 10
exit