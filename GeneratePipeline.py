import pandas as pd

def GeneratePipeline(genomedir="genomes",
                     prokkadir="prokkaSPOT",
                     ASV2Kingdomfile="SPOT_Prokaryotic16S_ASV_Domain_identity.csv",
                     blastoutput="SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv",
                     ncores=4):

    # process the blast output and collect the genome ids
    filename = blastoutput
    data = pd.read_csv(filename, sep='\t', header=None)

    # write an array to a tsv file
    unique_genomeid = data.iloc[:, 1].unique()
    with open("genomeid_full.tsv", "w") as f:
        for i in range(len(unique_genomeid)):
            # print(str(unique_genomeid[i]))
            f.write(str(unique_genomeid[i] + "\n"))

    header_string = """
#!/bin/bash                        
#SBATCH --time=5-10:10:00   # walltime
#SBATCH --ntasks=%i   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=10G   # memory per CPU core
#SBATCH -J "Jobnames"   # job name
#SBATCH --mail-user=liangxu@caltech.edu   # email address
""" % (ncores)

    ## write the sh script get_genome.sh
    with open('get_genome_test.sh', 'w') as f:
        f.write("""
#!/bin/bash

# Define the download function with one line from the tsv file as the feed-in
dl_data(){
    info=($1)
    str1="%s" #${info[0]} # blast id, e.g. c497da3b39f30aceede6bec3b03cd100
    str2=${info[1]} # genome id, e.g. GB_GCA_905618805.1
    # echo $str1 
    # echo $str2

    if [[ ! -e $str1/$str2 ]]; then
        # create folders to hold each species and further down to matched genomes for each species
        mkdir -p $str1/$str2
        # get database and the correct genome id, e.g. sourceid=GB, genomeid=GCA_905618805.1
        IFS='_' read -ra ADDR <<< "$str2"
        sourceid="${ADDR[0]}"
        genomeid="${ADDR[1]}_${ADDR[2]}" 
        

        # downloaed zip file and file directory
        output="${genomeid}.zip"
        filedir="${str1}/${str2}/${output}"    
        
        # echo $output
        # echo $filedir
        # download data using datasets from ncbi
        ./datasets download genome accession $genomeid --include gff3,rna,cds,protein,genome,seq-report --filename $filedir

        unzip $filedir -d "${str1}/${str2}"
    fi
}
export -f dl_data

echo "FileReading Starts"

# The second argument specifies the input file
inputfile=$2

# parallel the download function with the first argument specifying number of cores
cat $inputfile | parallel -j $1 dl_data

echo "Done"
        
""" % (genomedir))

    ## write the sh script sub_getgenome.bash
    with open('sub_getgenome_test.bash', 'w') as f:
        f.write(header_string)
        f.write("""
module load parallel/20180222

sh get_genome_test.sh %i %s 
""" % (ncores, blastoutput))


    ## write the sh script prokka_genomes.sh
    with open('prokka_genomes_test.sh', 'w') as f:
        f.write("""
#!/bin/bash

# Define the download function with one line from the tsv file as the feed-in
prokka_data(){
    info=($1)
    ASVtag=${info[0]} # ASV tag, e.g. c497da3b39f30aceede6bec3b03cd100
    str2=${info[1]} # genome id, e.g. GB_GCA_905618805.1

    extline="$(grep -m1 -i "$ASVtag" %s)" # get the line with the ASV tag

    IFS=';' read -ra ADDR <<< "$extline"
    kingdom="$(echo ${ADDR[0]} | cut -d',' -f2)"

    prokkaoutput="%s"

    if [[ ! -e $prokkaoutput/$str2 ]]; then
        # create folders to hold annotated genomes for $str2
        # mkdir -p $prokkaoutput
        # read json file
        json_file="SPOT/genomes/${str2}/ncbi_dataset/data/dataset_catalog.json"

        # get the path to the genome file
        genome_file1=$(jq -r .assemblies[1].files[0].filePath ${json_file})
        # e.g. /SPOT/genomes/GB_GCA_902623215.1/ncbi_dataset/data/GCA_902623215.1/GCA_902623215.1_AG-893-M16_genomic.fna
        genome_file2="SPOT/genomes/${str2}/ncbi_dataset/data/${genome_file1}"

        # download data using datasets from ncbi
        if [[ $kingdom == *"Bacteria"* ]]; then
            singularity exec prokka.sif prokka --norrna --notrna --centre X --compliant --kingdom Bacteria $genome_file2 --prefix $str2 --outdir $prokkaoutput/$str2 #--prefix $prokkaoutput/$str2 
        elif [[ $kingdom == *"Archaea"* ]]; then
            singularity exec prokka.sif prokka --norrna --notrna --centre X --compliant --kingdom Archaea $genome_file2 --prefix $str2 --outdir $prokkaoutput/$str2 #--prefix $prokkaoutput/$str2 
        else
            singularity exec prokka.sif prokka --norrna --notrna --centre X --compliant --kingdom Bacteria $genome_file2 --prefix $str2 --outdir $prokkaoutput/$str2 #--prefix $prokkaoutput/$str2 
        fi

    fi
}
export -f prokka_data

echo "Prokka Starts"

# The second argument specifies the input file
inputfile=$2

# parallel the download function with the first argument specifying number of cores
cat $inputfile | parallel -j $1 prokka_data

echo "Done"

""" % (ASV2Kingdomfile, prokkadir))

    ## write the sh script sub_prokka.bash
    with open('sub_prokka_test.bash', 'w') as f:
        f.write(header_string)
        f.write("""
#!/bin/bash
## now loop through the above array

#SBATCH --time=6-20:10:00   # walltime
#SBATCH --ntasks=%i   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=10G   # memory per CPU core
#SBATCH -J "ProkkaSPOT"   # job name
#SBATCH --mail-user=liangxu@caltech.edu   # email address

module load parallel/20180222
module load singularity/3.3.0

sh prokka_genomes_test.sh %i %s
""" % (ncores, ncores, blastoutput))


    ## write the sh script R_CDS.sh
    with open('R_CDS_test.sh', 'w') as f:
        f.write("""
#!/bin/bash

# Define the download function with one line from the tsv file as the feed-in
CDS_data(){
    str2=($1)
    prokkaoutput="%s"

    # create folders to hold annotated genomes for $str2
    gff_file="${prokkaoutput}/${str2}/${str2}.gff"
    cds_file="${str2}_CDS_names.txt"

    # generate CDS names
    sed -n '/##FASTA/q;p' $gff_file | awk '$3=="CDS"' | awk '{print $9'} | awk 'gsub(";.*","")' | awk 'gsub("ID=","")' > $prokkaoutput/$str2/$cds_file
    sleep 1
    Rscript gRodonGenomes.R $str2

}
export -f CDS_data

echo "CDS Starts"

# The second argument specifies the input file
inputfile=$2

# parallel the download function with the first argument specifying number of cores
cat $inputfile | parallel -j $1 CDS_data

echo "Done"


""" % (prokkadir))

        ## write the R script gRodonGenomes.R
        with open('gRodonGenomes_test.R', 'w') as f:
            f.write(f"""
#!/usr/bin/env Rscript

library(gRodon, quietly = T)
library(Biostrings, quietly = T)
library(jsonlite, quietly = T)
# Load your *.ffn file into R

args = commandArgs(trailingOnly = TRUE)[1]

genes <- readDNAStringSet(paste0("{prokkadir}/",args,"/",args,".ffn"))

# Subset your sequences to those that code for proteins
CDS_IDs <- readLines(paste0("{prokkadir}/",args,"/",args,"_CDS_names.txt"))
gene_IDs <- gsub(" .*","",names(genes)) #Just look at first part of name before the space
genes <- genes[gene_IDs %in% CDS_IDs]

#Search for genes annotated as ribosomal proteins
highly_expressed <- grepl("ribosomal protein",names(genes),ignore.case = T)

maxg <- predictGrowth(genes, highly_expressed)
ListJSON=toJSON(maxg,pretty=TRUE,auto_unbox=TRUE)
write(ListJSON, paste0("{prokkadir}/",args,"/",args,"_growth_est.json"))
""")

    ## write the sh script SumJsons.py
    with open('SumJsons_test.py', 'w') as f:
        f.write(f"""
import json
import pandas as pd
import os
dir = "{prokkadir}/"
file = pd.read_csv("genomeid_full.tsv",sep='\t', header=None)
data_df = pd.DataFrame()

for genomeid in file.iloc[:,0].unique():
    est_file = dir + str(genomeid) + "/" + str(genomeid) + "_growth_est.json"
    if os.path.isfile(est_file):
        with open(est_file) as f:
            data = json.load(f)
            data['genomeid'] = genomeid
            data_df = pd.concat([data_df, pd.DataFrame(data, index=[0])], ignore_index=True)
            # print(data["CUBHE"])

data_df.to_csv("EstG_genome_full.tsv", sep='\t', index=False)
""")

    ## write the sh script sub_sumjson.bash
    with open('sub_sumjson_test.bash', 'w') as f:
        f.write(header_string)
        f.write("""
#!/bin/bash
## now loop through the above array

#SBATCH --time=10:10:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=10G   # memory per CPU core
#SBATCH -J "SumJsons"   # job name
#SBATCH --mail-user=liangxu@caltech.edu   # email address

python SumJsons.py
""")
        
        ## write the python script to check the missed ASV tags
        with open('check_missed_ASV.py', 'w') as f:
            f.write(f"""
import pandas as pd
import multiprocess as mp


def missed_species(i):
    import pandas as pd

    # find those species that have no hits and what these species are
    p16_blast = pd.read_csv("{blastoutput}", sep='\t', header=None)
    ori_data = pd.read_csv("{ASV2Kingdomfile}", sep='\t')

    if ori_data.iloc[i,0] not in p16_blast.iloc[:,0].unique():
        missed_kingdom = ori_data.iloc[i,1].split(";")[0]
        missed_species =pd.DataFrame({'Species': ori_data.iloc[i,0], 'Kingdom': missed_kingdom}, index=[0])
        return missed_species


ori_data = pd.read_csv("{ASV2Kingdomfile}", sep='\t')

with mp.Pool(mp.cpu_count() - 1) as pool:
    data = pool.map(missed_species, [i for i in range(ori_data.shape[0])])
p16missed = pd.concat(data, axis=0)
p16missed.to_csv('missedTags.csv')
""")

