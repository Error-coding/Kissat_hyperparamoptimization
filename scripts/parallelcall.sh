#!/bin/sh
#SBATCH --ntasks-per-node=1

cd /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts
srun ./callproc.sh


exit