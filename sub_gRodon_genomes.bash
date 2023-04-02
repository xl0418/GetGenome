#!/bin/bash
## now loop through the above array

#SBATCH --time=3-00:10:00   # walltime
#SBATCH --ntasks=16   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=10G   # memory per CPU core
#SBATCH -J "CDS-gRodon"   # job name
#SBATCH --mail-user=liangxu@caltech.edu   # email address

module load parallel/20180222
module load gcc/9.2.0
module load R/4.2.2

sh R_CDS.sh 16 genomeid.tsv


