# VCF file variant count calculating script
# Version: 3
# Author: Ram Kumar
# Date: 27 July 2022 
# Purpose: To count the variant identifiers for the variant database (parallelization included)

import pandas as pd
import os
from collections import Counter
import time
import logging 
import gc
import concurrent.futures 


logger = logging.getLogger(__name__)

project_dir =  os.getcwd() 
log_dir = os.path.join(project_dir,'logs')
os.makedirs(log_dir,exist_ok=True)

log_file_path = os.path.join(log_dir,'variant_af_log.log')
   

logging.basicConfig(filename=log_file_path,
                    format = '%(asctime)s -%(name)s - %(levelname)s -%(message)s',
                    level = logging.DEBUG)

large_vcf_files = [file for file in os.listdir() if file.endswith('.gz')][:50]
 
 

def reading_zip_and_converting_to_hd5(input_zip_file):
    try:
        filename, extension = os.path.splitext(input_zip_file)
        large_vcf = pd.read_csv(input_zip_file, comment= '#', sep= '\t', header=None, usecols=[0,1,3,4])
        large_vcf.columns = ['#CHROM', 'POS',   'REF',	'ALT']
        h5_filename = '{}.h5'.format(filename)
        large_vcf.to_hdf(h5_filename, key='large_vcf', mode='w') 
        gc.collect() 
        return h5_filename
    except EOFError:
        logging.info('This {} is skipped because of EOFError'.format(input_zip_file))
        return None

         


def reading_h5_file_and_finding_variants(input_h5_File):
    try:
        variant_identifiers_list = []
        
        large_h5 =   pd.read_hdf(input_h5_File)  
        large_h5['ALT'] = large_h5['ALT'].str.replace(',', '__')
        ##drop rows not starting with 'chr'
        large_h5 = large_h5.drop(large_h5[ ~ large_h5['#CHROM'].str.startswith('chr')].index)
        ## removing such lines: chrUn 
        large_h5 = large_h5.drop(large_h5[large_h5['#CHROM'].str.startswith('chrUn')].index)
        ## removing such lines: chr6_GL000256v2_alt
        large_h5 = large_h5.drop(large_h5[large_h5['#CHROM'].str.count('_') != 0  ].index)
        # convert chr6_GL000256v2 to chr6
        #large_h5['#CHROM'] = large_h5['#CHROM'].apply(lambda x: x.split('_')[0] if x.startswith('chr') else x)  
        variant_identifier = large_h5['#CHROM'] +'_'+large_h5['POS'].astype(str) +'_'+ large_h5['REF'] +'_'+ large_h5['ALT']
        
        variant_identifiers_list.extend(variant_identifier.values.tolist())
        gc.collect()
        return  variant_identifiers_list 
    except:
        return []

 
def calculating_complete_variant_list(vcf_file):
    logger.info('Starting with the file {}'.format( vcf_file))
    variant_identifiers_list = reading_h5_file_and_finding_variants(reading_zip_and_converting_to_hd5(vcf_file))
    gc.collect()
    return variant_identifiers_list

def calculating_variant_frequency(variants_list):  
    pd.DataFrame.from_dict(data= dict(reversed(Counter(variants_list).most_common())) , orient='index').to_csv(r'C:\Users\RamKumarRuppaSurulin\OneDrive - Arcensus GmbH\Desktop\testVCF\variantcounts_file.csv', header=False) 
    gc.collect()
 

if __name__ == '__main__':
    #print(len(large_vcf_files))
    program_start_time =  time.time()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        k=list(executor.map(calculating_complete_variant_list ,large_vcf_files ))
    
    final_variants_list = []
    for i in k:
        final_variants_list.extend(i)
    gc.collect()
    #print(len(final_variants_list))

    logger.info('Counting Process starts here:')
    counting_start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(calculating_variant_frequency ,[final_variants_list] )
    counting_end_time = time.time()
    
    gc.collect()
    program_end_time =  time.time()

    logger.info('The time took for the counting process is {:.2f} seconds.'.format( counting_end_time-counting_start_time))
    logger.info('The time took for the entire process is {:.2f} seconds.'.format( program_end_time-program_start_time))


    
      

#print(reading_h5_file_and_finding_variants(reading_zip_and_converting_to_hd5('603740W1a_wgs_S5786Nr12.hard-filtered.vcf.gz')))
