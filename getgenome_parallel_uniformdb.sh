#!/bin/bash

# Define the download function with one line from the tsv file as the feed-in
dl_data(){
    info=($1)
    str1="genomes" #${info[0]} # blast id, e.g. c497da3b39f30aceede6bec3b03cd100
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

# parallel the download function with the first argument $1 specifying number of cores
cat $inputfile | parallel -j $1 dl_data

echo "Done"


