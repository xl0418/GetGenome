import pandas as pd
import multiprocess as mp


def p16_missed_species(i):
    import pandas as pd

    # find those species that have no hits and what these species are
    p16_blast = pd.read_csv("P16NSdata/221117-1910.P16N-S.16S.dna-sequences.tsv", sep='\t', header=None)
    ori_data = pd.read_csv("P16NSdata/221118-0208.P16N-S.16S.all-16S-seqs.with-tax.proportions.tsv", sep='\t')

    if ori_data.iloc[i,0] not in p16_blast.iloc[:,0].unique():
        missed_kingdom = ori_data.iloc[i,1].split(";")[0]
        missed_species =pd.DataFrame({'Species': ori_data.iloc[i,0], 'Kingdom': missed_kingdom}, index=[0])
        return missed_species


ori_data = pd.read_csv("P16NSdata/221118-0208.P16N-S.16S.all-16S-seqs.with-tax.proportions.tsv", sep='\t')

with mp.Pool(mp.cpu_count() - 1) as pool:
    data = pool.map(p16_missed_species, [i for i in range(ori_data.shape[0])])
p16missed = pd.concat(data, axis=0)
p16missed.to_csv('P16missedTags.csv')