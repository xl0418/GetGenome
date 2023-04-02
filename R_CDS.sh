#!/bin/bash

# Define the download function with one line from the tsv file as the feed-in
CDS_data(){
    str2=($1)
    prokkaoutput="prokkaooutput"

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


