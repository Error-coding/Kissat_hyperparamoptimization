#!/bin/bash
spack env activate smac3
source /nfs/home/rzipperer/.bashrc
conda activate SMAC

echo "sh /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts/toplevel/8_21.sh\nsh /nfs/home/rzipperer/git/Kissat_hyperparamoptimization/scripts/toplevel/22_35.sh" | parallel -j 2