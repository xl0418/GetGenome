import json
import pandas as pd
import os
from Bio import SeqIO

dir = "prokkaP16NS/"
file = pd.read_csv("genomeid_full.tsv",sep='\t', header=None)
data_df = pd.DataFrame()

for genomeid in file.iloc[:,0].unique():
    est_file = dir + str(genomeid) + "/" + str(genomeid) + "_growth_est_tempopt.json"
    dna_file = dir + str(genomeid) + "/" + str(genomeid) + ".fna"
    if os.path.isfile(est_file):

        fasta_sequences = SeqIO.parse(dna_file, 'fasta')

        for fasta in fasta_sequences:
            name, sequence = fasta.id, str(fasta.seq)
            if len(sequence) > 300:
                dna_seq300 = sequence[0:300]
                break


        with open(est_file) as f:
            data = json.load(f)
            data['genomeid'] = genomeid
            data['dna'] = dna_seq300
            data_df = pd.concat([data_df, pd.DataFrame(data, index=[0])], ignore_index=True)
            # print(data["CUBHE"])

data_df.to_csv("P16NS_DNA_maxg.tsv", sep='\t', index=False)