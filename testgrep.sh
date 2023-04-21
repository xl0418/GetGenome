#!/bin/bash

ASVtag="c497da3b39f30aceede6bec3b03cd100"
extline="$(grep -m1 -i "$ASVtag" TaxInfo.tsv)"

IFS=';' read -ra ADDR <<< "$extline"
kingdom="$(echo ${ADDR[0]} | cut -d' ' -f2)"
echo $kingdom
