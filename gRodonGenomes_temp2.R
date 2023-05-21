#!/usr/bin/env Rscript

library(gRodon, quietly = T)
library(Biostrings, quietly = T)
library(jsonlite, quietly = T)
# Load your *.ffn file into R

args = commandArgs(trailingOnly = TRUE)[1]

read_csv = read.csv('data/P16NS_full_data_fullhits.csv')
temp_df = read_csv[read_csv$genomeid == args,]
top1 = ceiling(nrow(temp_df) / 100)

temp_vec = rev(sort(temp_df$relative_a, index.return=TRUE)$ix)[1:top1]

temp_args = mean(temp_df$temp[temp_vec])

genes <- readDNAStringSet(paste0("prokkaooutput/",args,"/",args,".ffn"))

# Subset your sequences to those that code for proteins
CDS_IDs <- readLines(paste0("prokkaooutput/",args,"/",args,"_CDS_names.txt"))
gene_IDs <- gsub(" .*","",names(genes)) #Just look at first part of name before the space
genes <- genes[gene_IDs %in% CDS_IDs]

#Search for genes annotated as ribosomal proteins
highly_expressed <- grepl("ribosomal protein",names(genes),ignore.case = T)

maxg <- predictGrowth(genes, highly_expressed, temperature = temp_args)
ListJSON=toJSON(maxg,pretty=TRUE,auto_unbox=TRUE)
write(ListJSON, paste0("prokkaooutput/",args,"/",args,"_growth_est_tempopt.json"))
