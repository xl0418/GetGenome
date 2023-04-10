import json
import pandas as pd
import os
dir = "prokkaooutput/"
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