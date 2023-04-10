#!/bin/bash

echo "Searching Starts"

# Define the download function with one line from the tsv file as the feed-in

while IFS= read -r line; do
    str2=$line
    [ ! -d "prokkaooutput/${str2}" ] && echo $str2 >> missinggenome.txt
    
done < $1

echo "Done"

