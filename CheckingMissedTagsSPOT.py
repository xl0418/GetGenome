import pandas as pd
import multiprocess as mp

def spot_missed_species(i):
    # find species that have no hits in BLAST for SPOT dataset
    spot_blast = pd.read_csv("SPOT/SPOT_Prokaryotic16S_ASV_Domain_identity.csv", sep='\t', header=None)
    spot_data = pd.read_csv("SPOT/SPOT_Prokaryotic16S_ASV_dna-sequences_BLASToutput.tsv", sep='\t')
    speciestag = spot_blast.iloc[i, 0].split(",")[0]
    speciestag = speciestag.replace(">", "")

    if speciestag not in spot_data.iloc[:,0].unique():
        missed_kingdom = spot_blast.iloc[i, 0].split(",")[1]
        missed_species_spot =pd.DataFrame({'Species': spot_blast.iloc[i,0], 'Kingdom': missed_kingdom}, index=[0])
        return missed_species_spot

spot_blast = pd.read_csv("SPOT/SPOT_Prokaryotic16S_ASV_Domain_identity.csv", sep='\t', header=None)


with mp.Pool(mp.cpu_count() - 1) as pool:
    data = pool.map(spot_missed_species, [i for i in range(spot_blast.shape[0])])
spotmissed = pd.concat(data, axis=0)
spotmissed.to_csv('spotmissedTags.csv')
