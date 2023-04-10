#!/bin/bash
## now loop through the above array

#SBATCH --time=00:10:00   # walltime
#SBATCH --ntasks=4   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=10G   # memory per CPU core
#SBATCH -J "GetGenome"   # job name
#SBATCH --mail-user=liangxu@caltech.edu   # email address

module load parallel/20180222

sh getgenome_parallel.sh 4 test.tsv


