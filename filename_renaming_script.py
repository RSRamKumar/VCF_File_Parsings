# Script for renaming the filenames
# Version:1
# Author: Ram Kumar
# Date: 3rd November
# Purpose: Script for renaming the filename based on the IDs given in the file
 
"""
dict.txt:
varvis sample ID	subject
100391_wgs_S4159Nr21_S01	arc000001
100394_wgs_S4159Nr22_S01	arc000002
100402_wgs_S4159Nr23_S01	arc000003
100405_wgs_S4159Nr24_S01	arc000004
100409_wgs_S4159Nr25_S01	arc000005

file_change.log:
100405_wgs_S4159Nr24_S01-ready.R2.fq.gz gets renamed as arc000004.R2.fq.gz.
100391_wgs_S4159Nr21_S01-ready.R1.fq.gz gets renamed as arc000001.R1.fq.gz.
100391_wgs_S4159Nr21_S01-ready.K2report.txt gets renamed as arc000001.K2report.txt.
100401_wgs_S4574Nr10_S01-ready.R2.fq.gz is skipped for renaming as it didn't find its subject ID.
100394_wgs_S4159Nr22_S01-ready.kraken.gz gets renamed as arc000002.kraken.gz.
100409_wgs_S4159Nr25_S01-ready.kraken.gz gets renamed as arc000005.kraken.gz.
100391_wgs_S4159Nr21_S01-ready.kraken.gz gets renamed as arc000001.kraken.gz.
100394_wgs_S4159Nr22_S01-ready.K2report.txt gets renamed as arc000002.K2report.txt.

"""
import pandas as pd
import os


def changing_filename(input_filename,old_file_id, new_file_id):
         
        return  input_filename.replace(old_file_id, new_file_id).replace('-ready','')
        
 
        
if __name__ == '__main__':

      
      new_file_names_df = pd.read_csv('dict.txt', sep='\t')
       
      
      input_files_list = [file for file in os.listdir() if '_wgs_' in file]
       
      fout = open('file_change.log', 'w')
      
      for input_file in input_files_list:
              old_file_id, *_ = input_file.split('-')
              try:
                new_file_id = new_file_names_df[ new_file_names_df['varvis sample ID']==old_file_id]['subject'].values[0]
                renamed_filename = changing_filename(input_file,old_file_id, new_file_id)
                os.rename(input_file,renamed_filename)
                fout.write('{} gets renamed as {}.\n'.format(input_file, renamed_filename))
              except :
                fout.write('{} is skipped for renaming as it didn\'t find its subject ID.\n'.format(input_file))
               
      fout.close()
       
