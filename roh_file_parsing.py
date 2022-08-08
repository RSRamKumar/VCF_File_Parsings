# ROH metrics file Parsing script
# Version: 1
# Author: Ram Kumar
# Date: 05 July 2022 
# Purpose: To integrate all ROH metrics in one file




import pandas as pd
import re 
import os

roh_files = [file for file in os.listdir() if 'roh_metrics' in file] 

#print(len(roh_files))

def parsing_roh_files(roh_input_file):

    file_name, extension =  os.path.splitext(roh_input_file) 
    sample_id, _ , run_id   = file_name.partition('_wgs_')
    run_id = run_id.split('.')[0]
     


    df = pd.read_csv(roh_input_file, header=None)
    roh_parsed_df = df.iloc[:,2:].T

    roh_parsed_df.columns = roh_parsed_df.iloc[0]
    final_roh_parsed_df = roh_parsed_df[1:].reset_index(drop=True)

    

    final_roh_parsed_df.insert(0,'sample_id',sample_id)
    final_roh_parsed_df.insert(1,'run_id', run_id )
    simplified_sample_id = final_roh_parsed_df['sample_id'].apply(lambda x: int(re.split('\D+', x)[0])) # convert 602924B1a to 602924
    final_roh_parsed_df.insert(2,'simplified_sample_id', simplified_sample_id )
    return  final_roh_parsed_df



parsed_output_files_dfs = []
for file in roh_files:
    out_df = parsing_roh_files(file)
    parsed_output_files_dfs.append(out_df)


df_concat = pd.concat(parsed_output_files_dfs, ignore_index=True)
 
output_file = 'ROH_metrics_parsed_7July.xlsx'  
df_concat.to_excel ( output_file, index = False, header=True)



#roh_parsed_dict = dict(roh_parsed_df.values )
#print(roh_parsed_dict)  

#print(parsing_roh_files('704372W1a_wgs_S5859Nr1.roh_metrics.csv'))
