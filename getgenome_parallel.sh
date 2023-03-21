#!/bin/bash

dl_data(){
    info=($1)
    str1=${info[0]} # blast id, e.g. c497da3b39f30aceede6bec3b03cd100
    str2=${info[1]} # genome id, e.g. GB_GCA_905618805.1
    echo $str1 
    echo $str2

    # create folders to hold each species and further down to matched genomes for each species
    mkdir -p $str1/$str2
    # get database and the correct genome id, e.g. sourceid=GB, genomeid=GCA_905618805.1
    IFS='_' read -ra ADDR <<< "$str2"
    sourceid="${ADDR[0]}"
    genomeid="${ADDR[1]}_${ADDR[2]}" 
    

    # downloaed zip file and file directory
    output="${genomeid}.zip"
    filedir="${str1}/${str2}/${output}"    
    
    echo $output
    echo $filedir
    # download data using datasets from ncbi
    ./datasets download genome accession $genomeid --filename $filedir

    unzip $filedir -d "${str1}/${str2}"
}


echo "FileReading Starts"

# Get the total number of lines in the file
inputfile="test.tsv"
total_lines=$(wc -l < $inputfile)
echo $inputfile
echo $total_lines
# Initialize the line counter
line_number=1
# Iterate the lines in the tsv file
while IFS= read -r line
do
    # extract the blast species id and the genome matching id 
    dl_data "$line"
    
    # Print the progress bar
    echo -ne "\rProcessing line $line_number of $total_lines"
    # Increase the line counter
    line_number=$((line_number+1))
done < $inputfile
echo "Done"


# Record the line when the process stops
echo $line_number > last_line.txt
