import json
import pandas as pd
import os
from Bio import SeqIO

dir = "prokkaP16NS/"
# dir = "preprocessdata/"
file = pd.read_csv("genomeid_full.tsv",sep='\t', header=None)

data_df = pd.DataFrame()

for genomeid in file.iloc[:,0].unique():
    est_file = dir + str(genomeid) + "/" + str(genomeid) + "_growth_est_tempopt.json"
    dna_file = dir + str(genomeid) + "/" + str(genomeid) + ".ffn"
    if os.path.isfile(est_file):

        fasta_sequences = SeqIO.parse(dna_file, 'fasta')

        for fasta in fasta_sequences:
            desc, sequence = fasta.description, str(fasta.seq)

            if "ribosomal protein" in desc:
                dna_seq300 = sequence
                with open(est_file) as f:
                    data = json.load(f)
                    data['description'] = desc
                    data['genomeid'] = genomeid
                    data['dna'] = dna_seq300
                    data_df = pd.concat([data_df, pd.DataFrame(data, index=[0])], ignore_index=True)
            # print(data["CUBHE"])

data_df.to_csv("P16NS_ribosomal_maxg.tsv", sep='\t', index=False)