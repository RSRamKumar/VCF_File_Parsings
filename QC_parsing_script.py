# QC Parsing script
# Version: 1
# Author: Ram Kumar
# Date: 04 and 05 July 2022 
# Purpose: Generation of QC report from cegat data

import os
import pandas as pd
#import humanize

 
os.chdir(r'C:\Users\RamKumarRuppaSurulin\OneDrive - Arcensus GmbH\Desktop\parsing_files' )

mapping_metrics_files = [ file for file in os.listdir() if 'mapping_metrics' in file]

ploidy_estimation_files = [ file for file in os.listdir() if 'ploidy_estimation' in file]

 

mapping_fields = [ 'Total input reads', 
    'Number of duplicate marked reads', 
    'Mapped reads', 
    'Properly paired reads', 
    'Paired reads mapped to different chromosomes' ,
    'Reads with MAPQ [40:inf)',
    'Reads with MAPQ NA (Unmapped reads)',
    'Insert length: mean',
    'Insert length: median',
    'Insert length: standard deviation',
    ]


mapping_fields_integer = [ 'Total input reads', 
    'Number of duplicate marked reads', 
    'Mapped reads', 
    'Properly paired reads', 
    'Paired reads mapped to different chromosomes' ,
    'Reads with MAPQ [40:inf)',
    'Reads with MAPQ NA (Unmapped reads)',
     ]

ploidy_fields = [ 'Autosomal median coverage', 
        'X median coverage', 
        'Y median coverage', 
        'Ploidy estimation', 
        ]


  
def parsing_mapping_and_ploidy_metrics(input_file,required_fields):
    """takes the input file to be parsed and outputs the parsed datframe in horizontal manner"""

    metrics_df = pd.read_csv(input_file, header=None)

    if 'mapping_metrics' in input_file:

        parsed_df = metrics_df.loc[(metrics_df[0] =='MAPPING/ALIGNING SUMMARY') & (metrics_df[2].isin(required_fields))].iloc[:,[2,3]] 
    
        final_metrics_df = parsed_df.T    # transpose function
        final_metrics_df.columns = final_metrics_df.iloc[0]
        final_metrics_df = final_metrics_df[1:].reset_index(drop=True)

        #percentage column
        mapping_df_percentage = metrics_df.loc[(metrics_df[2].isin(mapping_fields_integer)) & (metrics_df[0] =='MAPPING/ALIGNING SUMMARY')] .iloc [:,[2,4] ]
        mapping_df_percentage_dict = dict(mapping_df_percentage.values )
        
        #million column
        mapping_df_million   =  metrics_df.loc[(metrics_df[0] =='MAPPING/ALIGNING SUMMARY') & (metrics_df[2].isin(mapping_fields_integer)  )  ] .iloc [:,[2,3] ]
        mapping_df_million_dict = dict(mapping_df_million.values )
    
        
        for field in mapping_df_percentage_dict: # add to the dataframe
            final_metrics_df[field +' percentage'] =  mapping_df_percentage_dict[field]

        #for field in mapping_df_million_dict:
         #   final_metrics_df[field + ' in millions'] =  humanize.intword(mapping_df_million_dict[field]).split()[0]
        return final_metrics_df

 
    elif 'ploidy_estimation_metrics' in input_file: 

        parsed_df = metrics_df.loc[(metrics_df[0] =='PLOIDY ESTIMATION') & (metrics_df[2].isin(required_fields)  )  ] .iloc [:,[2,3] ] 
    
        final_metrics_df = parsed_df.T    # transpose function
        final_metrics_df.columns = final_metrics_df.iloc[0]
        final_metrics_df = final_metrics_df[1:].reset_index(drop=True)
 
        return final_metrics_df

  
parsed_output_files_dfs = []

for mapping_file in mapping_metrics_files:
    
     
    file_name, extension =  os.path.splitext(mapping_file) 
    sample_id, _ , run_id   = file_name.partition('_wgs_')
    run_id = run_id.split('.')[0]

    
    ploidy_file = [file for file in ploidy_estimation_files if sample_id in file ][0]  # matching mapping_metrics and ploidy file
     
    
    mapping_df = parsing_mapping_and_ploidy_metrics(mapping_file, mapping_fields) # actual parsing

    ploidy_df = parsing_mapping_and_ploidy_metrics(ploidy_file, ploidy_fields)

     
    df_concat = pd.concat([mapping_df, ploidy_df], axis=1)  # combining 2 dataframes

    df_concat.insert(0,'sample_id',sample_id) # adding sample id and run id column
    df_concat.insert(1,'run_id', run_id )
     

    #print(df_concat.head())
    parsed_output_files_dfs.append(df_concat)


#merging all the individual results
final_df = pd.concat(parsed_output_files_dfs, ignore_index=True)
#print(final_df.columns)
col  = ['sample_id', 'run_id', 
'Total input reads',    
       'Number of duplicate marked reads', 'Number of duplicate marked reads percentage', 
       'Mapped reads',  'Mapped reads percentage',  
        'Properly paired reads',  'Properly paired reads percentage',  
        'Paired reads mapped to different chromosomes', 'Paired reads mapped to different chromosomes percentage',  
        'Reads with MAPQ [40:inf)', 'Reads with MAPQ [40:inf) percentage',  
        'Reads with MAPQ NA (Unmapped reads)','Reads with MAPQ NA (Unmapped reads) percentage',  
       'Insert length: mean', 'Insert length: median',  'Insert length: standard deviation', 
       'Autosomal median coverage', 'X median coverage', 'Y median coverage','Ploidy estimation',
       ]


df = pd.DataFrame(final_df,columns= col  )
print(df.head())
df.to_excel ( 'final_parsed_file.xlsx', index = False, header=True)
