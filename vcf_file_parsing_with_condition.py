# Name: vcf_file_parsing_with_condition.py
# Version: 1
# Author: Ram Kumar
# Date: 27th September
# Purpose: To separate the count of ALT greater and less than 50

 
import pandas as pd
import os


def parsing_VCF_file(input_vcf_file):
    filename, ext = os.path.splitext(input_vcf_file)
    vcf_df = pd.read_csv(input_vcf_file, sep='\t', comment='#',  header=None)
    vcf_df.columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'META' ]

    vcf_df [vcf_df['ALT'].str.len().ge(50)].to_csv('{}.cnv'.format(filename), index=False)
    vcf_df [vcf_df['ALT'].str.len().lt(50)].to_csv('{}.csv'.format(filename), index=False)

    print('{} processing is done'.format(input_vcf_file))  


if __name__ == '__main__':
    vcf_files_list = [file for file in os.listdir() if file.endswith('vcf')]

    for vcf_file in vcf_files_list:
        parsing_VCF_file(vcf_file)
        
        
        
        
        
#vcf_df[vcf_df ['ALT'].apply(lambda x: len(x)< 50) ].to_excel('vcf_alt_lt50.xlsx', index=False)
#vcf_df[vcf_df ['ALT'].apply(lambda x: len(x)>= 50) ].to_excel('vcf_alt_gt50.xlsx', index=False)

