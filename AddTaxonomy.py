import pandas as pd
import multiprocess as mp

filename = "221117-1910.P16N-S.16S.dna-sequences.tsv"
full_len = pd.read_csv(filename, sep='\t', header=None)


def addtax(row):
    import pandas as pd
    filename = "221117-1910.P16N-S.16S.dna-sequences.tsv"
    full_data_blast_output=pd.read_csv(filename,sep='\t', header=None)

    tax_filename = "TaxInfo.tsv"
    tax_data=pd.read_csv(tax_filename,sep='\t')
    i = row
    row_tax = tax_data[tax_data.iloc[:,0] == full_data_blast_output.iloc[i,0]].index.values
    if len(row_tax) == 0:
        print("No tax found for " + str(full_data_blast_output.iloc[i,0]))
        tax_kingdom = 'NA'
    else:
        tax_name_full = tax_data.iloc[row_tax,1].values[0]
        tax_name = tax_name_full.split(";")[0]
        if tax_name == 'd__Bacteria':
            tax_kingdom = 'Bacteria'
        elif tax_name == 'd__Archaea':
            tax_kingdom = 'Archaea'
        else:
            tax_kingdom = 'Eukaryota'
    return tax_kingdom

with mp.Pool(processes = (16)) as pool:
    Kingdom = pool.map(addtax, [ii for ii in range(full_len.shape[0])])


full_len.insert (2, "Kingdom", Kingdom)
full_len.to_csv("221117-1910.P16N-S.16S.dna-sequences.tax.tsv", sep='\t', index=False, header=False)