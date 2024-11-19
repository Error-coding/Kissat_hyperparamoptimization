#!/bin/sh


cd /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts
srun --exclusive ./callproc.sh $1


exit