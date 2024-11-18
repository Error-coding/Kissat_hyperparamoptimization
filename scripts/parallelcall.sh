#!/bin/sh
#SBATCH --ntasks-per-node=16

cd /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts
srun ./callproc.sh


exit