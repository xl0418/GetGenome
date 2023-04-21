#!/bin/bash

#SBATCH --time=6-00:00:00   # walltime
#SBATCH --ntasks=16   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=10G   # memory per CPU core
#SBATCH -J "GetGenome"   # job name
#SBATCH --mail-user=liangxu@caltech.edu   # email address

module load parallel/20180222

sh getgenome_parallel_uniformdb.sh 16 SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv


