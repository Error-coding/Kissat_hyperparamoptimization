#!/bin/sh
spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC
cd /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts
task=$(($1 + $SLURM_PROCID))
echo $task
python3 ./kissatparallel.py $task 5000 20 10
exit