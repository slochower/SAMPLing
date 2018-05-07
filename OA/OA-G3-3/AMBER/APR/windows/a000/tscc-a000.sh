#!/bin/bash
#PBS -l walltime=8:00:00,nodes=1:ppn=2 -q home-gibbs
#PBS -j oe -r n
#PBS -N SAMPLing

source /home/davids4/amber18_gnu.sh

SCRDIR=/oasis/tscc/scratch/davids4/SAMPLing/$PBS_JOBID
mkdir -p $SCRDIR

# Need the `-L` to resolve any links.
rsync -avL $PBS_O_WORKDIR/ $SCRDIR/

cd $SCRDIR
source activate paprika
python simulate-a000.py

rsync -avL $SCRDIR/ $PBS_O_WORKDIR/
