import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import multiprocess as mp

filename = "221201_P16N-S.prok-nonphoautototrophic.BLAST-95pcID-vs-GTDB-r207-allproks.tsv"
data=pd.read_csv(filename,sep='\t', header=None)

total_hits = data.shape[0]

total_species = len(data.iloc[:,0].unique())
#
df2 = data.pivot_table(index = [0], aggfunc ='size',
               fill_value=0)

total_unique_genomes=len(data.iloc[:,1].unique())


fig, axes = plt.subplots(1, 2)
axes[0].set_title('Unscaled hits')
axes[1].set_title('Log2 scaled hits')

unscaled = sns.histplot(data = df2, kde=False, ax = axes[0])

scaled = sns.histplot(data = np.log2(df2), kde=False, ax = axes[1])
fig.show()
fig.savefig("Hits_distribution.png")


# write an array to a tsv file
unique_genomeid = data.iloc[:,1].unique()
with open("genomeid_full.tsv", "w") as f:
    for i in range(len(unique_genomeid)):
        # print(str(unique_genomeid[i]))
        f.write(str(unique_genomeid[i] + "\n"))
