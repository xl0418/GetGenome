#!/bin/bash
## now loop through the above array

#SBATCH --time=1-10:10:00   # walltime
#SBATCH --ntasks=16   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=10G   # memory per CPU core
#SBATCH -J "MissTagSPOT"   # job name
#SBATCH --mail-user=liangxu@caltech.edu   # email address

python CheckingMissedTagsSPOT.py


