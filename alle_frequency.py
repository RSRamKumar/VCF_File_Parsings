# Allele frequency Expansion hunter file Parsing script
# Version: 1
# Author: Ram Kumar
# Date: 08 July 2022 
# Purpose: To look at the allele frequency (chr-ref-pos) for all Expansion Hunter vcf metrics in one file


import pandas as pd

import os
 
eh_files =[file for file in os.listdir() if file.endswith('.vcf')]  
 
variant_ID_dict = {}
for file in eh_files:

    df = pd.read_csv( file, sep='\t', comment='#' , header=None,  )
     
    df.columns = ['#CHROM', 'POS', 'ID', 'REF',	'ALT',	'QUAL',	'FILTER','INFO', 'FORMAT','META' ]

    #print(df.loc[10]['POS']) 
    #print(df [['#CHROM',    'REF' ,'POS' 	 ]]  )
    variant_ID  = df['#CHROM'] + '_' + df['REF']+ '_' +df['POS'].astype(str)        

    #print( dict(df['variant_ID'].value_counts()))
    for var in variant_ID.values:
        variant_ID_dict[var] = variant_ID_dict.get(var, 0) + 1
             
print(variant_ID_dict)
print(set (variant_ID_dict.values()))





 #https://stackoverflow.com/questions/40950905/find-count-of-characters-within-the-string-in-python
