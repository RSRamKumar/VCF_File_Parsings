
# to retrieve HPO terms for Gene names

import pandas as pd
import requests
import json

hpo_df = pd.read_csv('genes_to_phenotype_202203.txt', sep='\t', comment='#', header=None)
hpo_df.columns = ['entrez-gene-id',
                'entrez-gene-symbol', 
                'HPO-Term-ID', 
                'HPO-Term-Name',
                'Frequency-Raw', 
                'Frequency-HPO',
                'Additional Info from G-D source',
                'G-D source', 
                'disease-ID for link']
                
                
def parse_hpo_id_for_gene_symbol(gene_symbol):
    return hpo_df[hpo_df['entrez-gene-symbol'] == gene_symbol]['HPO-Term-ID'].to_list()

def parse_hpo_term_for_gene_symbol(gene_symbol):
    return hpo_df[hpo_df['entrez-gene-symbol'] == gene_symbol]['HPO-Term-Name'].to_list()
    
    
print(parse_hpo_term_for_gene_symbol('DMD'))



# Input file from the database
# https://hpo.jax.org/app/download/annotation 
