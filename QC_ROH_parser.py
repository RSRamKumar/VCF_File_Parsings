# QC, ROH Parsing script
# Version:4
# Author: Ram Kumar
# Date: 2nd November
# Purpose: Generation of QC, ROH report from cegat data



import os
import pandas as pd
 

def parsing_filename(input_filename):
    filename = input_filename.rsplit('/')[-1]
    sample_id, run_id = filename.split('_wgs_')
    run_id = run_id.split('.')[0]
    run_id = run_id [:run_id.index('Nr')]
    return sample_id, run_id
    
 

def parsing_mapping_metrics_files(mapping_metrics_input_file):
    sample_id, run_id = parsing_filename(mapping_metrics_input_file)
    
    mapping_metrics_df = pd.read_csv(mapping_metrics_input_file, sep=',', header=None)
    required_columns = ['Total input reads', 'Number of duplicate marked reads', 'Mapped reads', 'Properly paired reads', 'Paired reads mapped to different chromosomes', 
                        'Reads with MAPQ [40:inf)', 'Reads with MAPQ NA (Unmapped reads)', 'Insert length: mean', 'Insert length: median', 'Insert length: standard deviation',
                        'Number of duplicate marked reads', 'Mapped reads', 'Properly paired reads', 'Paired reads mapped to different chromosomes', 'Reads with MAPQ [40:inf)',
                        'Reads with MAPQ NA (Unmapped reads)']
    
    values_column = required_columns[:-6]
    percentage_column = required_columns[-6:]
    df_a = mapping_metrics_df[(mapping_metrics_df[2].isin(values_column)) & (mapping_metrics_df[0] =='MAPPING/ALIGNING SUMMARY')] [[2,3]].T.reset_index(drop=True)
    df_a = df_a.rename(columns=df_a.iloc[0]).drop(df_a.index[0]) 
    df_b = mapping_metrics_df[(mapping_metrics_df[2].isin(percentage_column)) & (mapping_metrics_df[0] =='MAPPING/ALIGNING SUMMARY')] [[2,4]].T.reset_index(drop=True)
    df_b = df_b.rename(columns=df_b.iloc[0]).drop(df_b.index[0]).add_suffix('_percentage')
    mapping_metrics_parsed_df = pd.concat([df_a,df_b], axis=1)
    mapping_metrics_parsed_df.insert(0,'sample_id',sample_id) # adding sample id and run id column
    mapping_metrics_parsed_df.insert(1,'run_id', run_id )
    return mapping_metrics_parsed_df


def parsing_ploidy_estimation_files(ploidy_estimation_input_file):
    sample_id, run_id = parsing_filename(ploidy_estimation_input_file)
    ploidy_estimation_df = pd.read_csv(ploidy_estimation_input_file, sep=',', header=None)
    required_columns = ['Autosomal median coverage', 'X median coverage', 'Y median coverage', 'Ploidy estimation' ]
    ploidy_estimation_parsed_df = ploidy_estimation_df[(ploidy_estimation_df[2].isin(required_columns)) & (ploidy_estimation_df[0] =='PLOIDY ESTIMATION')] [[2,3]].T.reset_index(drop=True)
    ploidy_estimation_parsed_df = ploidy_estimation_parsed_df.rename(columns=ploidy_estimation_parsed_df.iloc[0]).drop(ploidy_estimation_parsed_df.index[0])
    ploidy_estimation_parsed_df.insert(0,'sample_id',sample_id) # adding sample id and run id column
    ploidy_estimation_parsed_df.insert(1,'run_id', run_id )
    return ploidy_estimation_parsed_df 


def parsing_roh_files(roh_input_file):
     
    sample_id, run_id = parsing_filename(roh_input_file)
    df = pd.read_csv(roh_input_file, header=None)
    roh_parsed_df = df.iloc[:,2:].T
    roh_parsed_df.columns = roh_parsed_df.iloc[0]
    final_roh_parsed_df = roh_parsed_df[1:].reset_index(drop=True)
    final_roh_parsed_df.insert(0,'sample_id',sample_id) # adding sample id and run id column
    final_roh_parsed_df.insert(1,'run_id', run_id )
    return final_roh_parsed_df 


if __name__ == '__main__':
    path = r'/cegatbucket/cegatsamples/S6423/'

    os.chdir(path)
    
    mapping_metrics_files_list = [ os.path.join(path,'02_bam', file) for file in os.listdir('02_bam') if file.endswith('mapping_metrics.csv')]
    
    ploidy_estimation_files_list = [ os.path.join(path,'02_bam', file) for file in os.listdir('02_bam') if file.endswith('ploidy_estimation_metrics.csv')]

    roh_files_list = [os.path.join(path,'03_snvs', file) for file in os.listdir('03_snvs') if  file.endswith('roh_metrics.csv')] 
    
    assert len(mapping_metrics_files_list) == len(ploidy_estimation_files_list) == len(roh_files_list)
    
    combined_mapping_metrics_df = pd.concat(list(map(parsing_mapping_metrics_files,mapping_metrics_files_list)), ignore_index=True)
    combined_ploidy_estimation_df = pd.concat(list(map(parsing_ploidy_estimation_files,ploidy_estimation_files_list)), ignore_index=True)
    combined_roh_df = pd.concat(list(map(parsing_roh_files,roh_files_list)), ignore_index=True)
    
    df = combined_mapping_metrics_df.merge(combined_ploidy_estimation_df,on = ['sample_id', 'run_id']).merge(combined_roh_df,on = ['sample_id', 'run_id'])
    
    df.columns = [col.lower().replace(' ','_').replace('(','').replace(')','').replace('[','').replace(':','').strip()  for col in df.columns]
    df.rename(columns={"percent_snvs_in_large_roh__>=_3000000": "Prct_snvs_largeROH3M", "number_of_large_roh__>=_3000000": "No_largeROH3M"}, inplace=True)

    _,runID = parsing_filename(mapping_metrics_files_list[0])
    df.to_excel('{}_QC_ROH_report1.xlsx'.format(runID), index=False, float_format="%.2f")
    
    
    
#https://stackoverflow.com/questions/23668427/pandas-three-way-joining-multiple-dataframes-on-columns
    