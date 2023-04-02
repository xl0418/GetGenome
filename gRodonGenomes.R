#!/usr/bin/env Rscript

library(gRodon, quietly = T)
library(Biostrings, quietly = T)
library(jsonlite, quietly = T)
# Load your *.ffn file into R

args = commandArgs(trailingOnly = TRUE)[1]

genes <- readDNAStringSet(paste0("prokkaooutput/",args,"/",args,".ffn"))

# Subset your sequences to those that code for proteins
CDS_IDs <- readLines(paste0("prokkaooutput/",args,"/",args,"_CDS_names.txt"))
gene_IDs <- gsub(" .*","",names(genes)) #Just look at first part of name before the space
genes <- genes[gene_IDs %in% CDS_IDs]

#Search for genes annotated as ribosomal proteins
highly_expressed <- grepl("ribosomal protein",names(genes),ignore.case = T)

maxg <- predictGrowth(genes, highly_expressed)
ListJSON=toJSON(maxg,pretty=TRUE,auto_unbox=TRUE)
write(ListJSON, paste0("prokkaooutput/",args,"/",args,"_growth_est.json"))
