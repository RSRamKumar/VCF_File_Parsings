# ROH bed file Parsing script
# Version: 1
# Author: Ram Kumar
# Date: 06 July 2022 
# Purpose: To interpret BED file of ROH with a condition of score greater than 100


import pandas as pd

import os

roh_bed_files = [file for file in os.listdir() if file.endswith('.bed') ] 

#print(len(roh_bed_files))

def roh_bed_file_parsing_with_condition(input_roh_bed_file):


    file_name, extension =  os.path.splitext(input_roh_bed_file)
    sample_ID, _, _ = file_name.partition('_wgs_')
     

    df = pd.read_csv( input_roh_bed_file, sep= '\t', header=None)
    df.columns = [ 'chr', 'start', 'stop', 'score', 'no. of homozygous variants', 'no. of heterozygous variants' ]

    parsed_df = df [ df ['score'] > 100]
    parsed_df.insert(0,'sample_ID',sample_ID  ) 

    return parsed_df 


parsed_output_files_dfs = []
for file in roh_bed_files:
    out_df = roh_bed_file_parsing_with_condition(file)
    parsed_output_files_dfs.append(out_df)


df_concat = pd.concat(parsed_output_files_dfs, ignore_index=True)
print(df_concat.head())
df_concat.to_excel ( 'Roh_bed_file_parsed_7July.xlsx', index = False, header=True)

#print(roh_bed_file_parsing_with_condition('602924B1a_wgs_S5695Nr1.roh.bed'))
