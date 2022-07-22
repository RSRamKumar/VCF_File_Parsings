# VCF file allele frequency calculating script
# Version: 1
# Author: Ram Kumar
# Date: 13 and 14 July 2022 
# Purpose: To count the variant identifiers for the variant database

import pandas as pd
import os
from collections import Counter
import time


os.chdir(r'C:\Users\RamKumarRuppaSurulin\Arcensus GmbH\Research and Development - General\Ram\VCF\large_vcf_files')

large_vcf_files = [file for file in os.listdir() if file.endswith('.gz')]

 

#print(large_vcf_files)

def reading_zip_and_converting_to_hd5(input_zip_file):
    filename, extension = os.path.splitext(input_zip_file)
    large_vcf = pd.read_csv(input_zip_file, comment= '#', sep= '\t', header=None, usecols=[0,1,3,4])
    large_vcf.columns = ['#CHROM', 'POS',   'REF',	'ALT']
    
    #large_vcf.columns = ['#CHROM', 'POS', 'ID', 'REF',	'ALT',	'QUAL',	'FILTER','INFO', 'FORMAT','META' ]
    
    h5_filename = '{}.h5'.format(filename)
     
    large_vcf.to_hdf(h5_filename, key='large_vcf', mode='w')  
    return h5_filename


variants_list = []

def reading_h5_file_and_calculating_allele_freq(input_h5_File):
    large_h5 =   pd.read_hdf(input_h5_File)  
    large_h5['ALT'] = large_h5['ALT'].str.replace(',', '__')
       
    #large_h5 = large_h5.drop(large_h5[(~ large_h5['#CHROM'].str.startswith('chr')) | (large_h5['#CHROM'].str.startswith('chrUn')| (large_h5['#CHROM'].str.count('_') != 0) )].index)
    
    ##drop rows not starting with 'chr'
    large_h5 = large_h5.drop(large_h5[ ~ large_h5['#CHROM'].str.startswith('chr')].index)
    ## removing such lines: chrUn 
    large_h5 = large_h5.drop(large_h5[large_h5['#CHROM'].str.startswith('chrUn')].index)
    ## removing such lines: chr6_GL000256v2_alt
    large_h5 = large_h5.drop(large_h5[large_h5['#CHROM'].str.count('_') != 0  ].index)
    
    # convert chr6_GL000256v2 to chr6
    #large_h5['#CHROM'] = large_h5['#CHROM'].apply(lambda x: x.split('_')[0] if x.startswith('chr') else x)  
    variant_identifier = large_h5['#CHROM'] +'_'+large_h5['POS'].astype(str) +'_'+ large_h5['REF'] +'_'+ large_h5['ALT']
    
    variants_list.extend(variant_identifier.values.tolist())

program_start_time =  time.time()
       
for vcf_file in large_vcf_files:
    print('Starting with the file {}'.format(vcf_file))
    start_time =  time.time()

    h5_filename = reading_zip_and_converting_to_hd5(vcf_file)
    reading_h5_file_and_calculating_allele_freq(h5_filename)

    end_time =  time.time()
    print('The time took for processing the {} is {:.2f} seconds'.format(vcf_file, end_time-start_time))
 

 
print('execution done')

pd.DataFrame.from_dict(data= dict(reversed(Counter(variants_list).most_common())) , orient='index').to_csv('variantcounts_file.csv', header=False) 

program_end_time =  time.time()

print('The time took for the entire process is {:.2f} seconds.'.format( program_end_time-program_start_time))



#https://stackoverflow.com/questions/20950650/how-to-sort-counter-by-value-python   