# ROH bed file summary statistics script
# Version: 1
# Author: Ram Kumar
# Date: 07, 08 July 2022 
# Purpose: To interpret BED file of ROH using basic summary statistics


import pandas as pd

import os

os.chdir(r'C:\Users\RamKumarRuppaSurulin\Arcensus GmbH\Research and Development - General\ROH\ROH_data') 

roh_bed_files = [file for file in os.listdir() if file.endswith('.bed') ] 

df = pd.read_csv('602924B1a_wgs_S5695Nr1.roh.bed', sep= '\t', header=None)
df.columns = [ 'chr', 'start', 'stop', 'score', 'no. of homozygous variants', 'no. of heterozygous variants' ]

 
def creating_summary_stat_bed_score(input_roh_bed_file):


    file_name, extension =  os.path.splitext(input_roh_bed_file)
    sample_ID, _, _ = file_name.partition('_wgs_')
     

    df = pd.read_csv( input_roh_bed_file, sep= '\t', header=None)
    df.columns = [ 'chr', 'start', 'stop', 'score', 'no. of homozygous variants', 'no. of heterozygous variants' ]

    stat_series = df['score'].describe().tolist()

     
    for threshold in [100, 200, 300, 400, 500]:
          stat_series.append(df['score'].gt(threshold).sum())
    return   sample_ID, stat_series  


roh_stat_dict = {}
for file in roh_bed_files:
    sample_ID, dic = creating_summary_stat_bed_score(file)
    roh_stat_dict[sample_ID] = dic 

     
print(roh_stat_dict)

stat_df = pd.DataFrame(roh_stat_dict.values(), index =roh_stat_dict.keys() , columns=['count', 'mean','std', 'min', '25%', '50%', '75%', 'max', 
                                            'times>100','times>200', 'times>300', 'times>400', 'times>500' ] )
 
 
stat_df.to_excel ( 'Roh_bed_file_summary_stat_8July.xlsx',  header=True)


#print(creating_summary_stat_bed_score('602924B1a_wgs_S5695Nr1.roh.bed'))