#  Consanguinity analysis script
# Version: 1
# Author: Ram Kumar
# Date: 07 July 2022 
# Purpose: To match the samples from ROH metrics parsed with their consangunity result 


import pandas as pd
import os
 
os.chdir(r'C:\Users\RamKumarRuppaSurulin\Arcensus GmbH\Research and Development - General\ROH') 

consanguinity_meta_df = pd.read_excel('MetaData_Consanguinity.xlsx')
 
roh_metrics_parsed_df = pd.read_excel(r'C:\Users\RamKumarRuppaSurulin\Arcensus GmbH\Research and Development - General\ROH\output_files\ROH_metrics_parsed_7July.xlsx')



consanguinity_dict = {}
for ID in roh_metrics_parsed_df['simplified_sample_id']:
    if ID in consanguinity_meta_df['Order ID'].values:
        #print(ID,  consanguinity_meta_df.loc[consanguinity_meta_df['Order ID'].isin([ID])]['Consanguinity'].values)
        consanguinity_dict[ID] = (consanguinity_meta_df.loc[consanguinity_meta_df['Order ID'].isin([ID])]['Consanguinity'].values[0])
#print(consanguinity_dict)
  
roh_metrics_parsed_df['consanguinity'] = roh_metrics_parsed_df['simplified_sample_id'].apply(lambda x: consanguinity_dict.get(x,0))


roh_metrics_parsed_df.to_excel ( 'ROH_metrics_parsed_7July_consanguinity.xlsx', index = False, header=True)