# Expansion Hunter VCF file Parsing script
# Version: 1
# Author: Ram Kumar
# Date: 06 July 2022 
# Purpose: To integrate all the EH's VCF file 



import pandas as pd

import os
os.chdir(r'C:\Users\RamKumarRuppaSurulin\Arcensus GmbH\Research and Development - General\RepeatExpansion\ExpansionHunterOutput')

eh_files = [file for file in os.listdir()]

#print(len(eh_files))

df = pd.read_csv( eh_files[0], sep='\t', comment='#' , header=None)
df.columns = ['#CHROM', 'POS', 'ID', 'REF',	'ALT',	'QUAL',	'FILTER','INFO', 'FORMAT','META' ]

fields = ['#CHROM', 'POS', 'REF_VALUE', 'REGION' ]

df['REF_VALUE'] = df['INFO'].str.split(';').str[1].str.replace('REF=', '')   

df['REGION'] = df['INFO'].str.split(';').str[-1].str.replace('REPID=', '')   

# #df['alt_value'] = df['ALT'].str.split(',').str[-1].str.replace('<', '').str.replace('>', '')

reduced_df = pd.DataFrame(df, columns= fields)

#print(reduced_df.head())


def paring_ALT_column(input_file):

    # parsing the file name for getting the sample ID
    file_name, extension = os.path.splitext(input_file)
    sample_ID , _ , _ = file_name.partition('_wgs_')
     
    # reading the file
    input_df = pd.read_csv( input_file, sep='\t', comment='#' , header=None)
    input_df.columns = ['#CHROM', 'POS', 'ID', 'REF',	'ALT',	'QUAL',	'FILTER','INFO', 'FORMAT','META' ]
    
    #input_df[sample_ID] = input_df['ALT'].str.split(',').str[-1].str.replace('<', '').str.replace('>', '')
    reduced_df[sample_ID] = input_df['ALT'].str.split(',').str[-1].str.replace('<', '').str.replace('>', '').str.replace('STR','')

    return reduced_df

for file in eh_files:
    #print(file)
    paring_ALT_column(file)

#print(paring_ALT_column('602925B1a_wgs_S5695Nr2-ExpHunter.vcf'))

print(reduced_df.head())
print(reduced_df.shape)


reduced_df.to_excel ( 'eh_vcf_parsed_output.xlsx', index = False, header=True)
