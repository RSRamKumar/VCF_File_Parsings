# Expansion Hunter parsing script
# Version: 1
# Author: Ram Kumar
# Date: 23 Aug 2022 
# Purpose: To parse the EH vcf file and combine the STRipy  https://stripy.org/database


import pandas as pd

import os
import re
 
stripy_df = pd.read_html('https://stripy.org/database', encoding='utf8')[0]

 
eh_files = [ file for file in os.listdir() if file.endswith('ExpHunter.vcf')]

def parsing_eh_files(input_eh_file):
    filename, _ = os.path.splitext(input_eh_file)
    eh_df = pd.read_csv(input_eh_file, sep='\t', comment='#', header=None)
    eh_df.columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'META' ]

    #eh_df [['STR_min', 'STR_max']]= eh_df['ALT'].str.split(',', expand=True)
    eh_df.insert(4,'STR_min',eh_df['ALT'].str.split(',', expand=True)[0] )
    eh_df ['STR_min'] = eh_df ['STR_min'].str.replace('<STR', '').str.findall(r'\d+').str[0]
    eh_df.insert(5,'STR_max',eh_df['ALT'].str.split(',', expand=True)[1] )
    eh_df ['STR_max'] = eh_df ['STR_max'].str.replace('<STR', '').str.findall(r'\d+').str[0]
    eh_df.drop(columns='ALT', inplace=True)
    eh_df.dropna(subset=['STR_min', 'STR_max'], inplace=True, how='all')
    eh_df['Locus'] = eh_df['INFO'].str.rsplit('=').str[-1]  

    return  filename, eh_df

if __name__  == '__main__':

    for ehfile in eh_files:
        filename,eh_df = parsing_eh_files(ehfile)
        merged_df = pd.merge(eh_df, stripy_df, on="Locus",)
        merged_df['Path. repeats'] = merged_df['Path. repeats'].str.replace('&GreaterEqual;', ' ≥')
        columns = ['#CHROM', 'POS', 'ID', 'REF', 'STR_min', 'STR_max', 'QUAL', 'FILTER',
        'Locus', 'Repeat type', 'Motif', 'Region', 'Path. repeats', 'Disease',
        'INFO', 'FORMAT', 'META']
        merged_df = merged_df[ columns]  # changing the position of the columns

        output_filename = '{}_parsed.xlsx'.format(filename)
        merged_df.to_excel(output_filename, index=False)


#https://stackoverflow.com/questions/13148429/how-to-change-the-order-of-dataframe-columns

#https://stackoverflow.com/questions/43297589/merge-two-data-frames-based-on-common-column-values-in-pandas


 
 
 