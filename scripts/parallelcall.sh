#!/bin/sh
#SBATCH --ntasks-per-node=16

spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC


cd /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts
srun ./callproc.sh


exit