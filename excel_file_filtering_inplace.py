# Name: excel_file_filtering_inplace.py
# Version: 1
# Author: Ram Kumar
# Date: 29th September
# Purpose: To filter the files inplace without losing original content

 
import pandas as pd
import xlwings as xw
import os 


def filtering_files(input_file):
    df = xw.Book(input_file)
    df.sheets[0].api.Range('A1').CurrentRegion.Replace(".", 0)     # replace . as 0 in entire file
    df.sheets[0].api.Range('A1').CurrentRegion.AutoFilter( 21,'full')  # filter for Annotation_mode
    df.sheets[0].api.Range('A1').CurrentRegion.AutoFilter( 6,Criteria1:= '<=10') # filter for freq4
    df.sheets[0].api.Range('A1').CurrentRegion.AutoFilter( 2, Criteria1:= '>0') # filter for Overlapped_CDS_percent_max
    if 'FreqCNV' in input_file:
        df.sheets[0].api.Range('A1').CurrentRegion.AutoFilter( 16, Criteria1:= '>=10') # filter for QUAL 
    elif 'FreqMantaSV' in input_file:
        df.sheets[0].api.Range('A1').CurrentRegion.AutoFilter( 16, Criteria1:= '>=75') # filter for QUAL 

    df.close()







if __name__ == '__main__':
    path = os.getcwd() 

    CNV_files_list = [ os.path.join(path,'02_bam', file) for file in os.listdir() if 'FreqCNV' in file]
    SV_files_list = [ os.path.join(path,'02_bam', file) for file in os.listdir() if 'FreqMantaSV' in file]

     

    for input_file in CNV_files_list+SV_files_list:
        filtering_files(input_file)

      #https://youtu.be/-w4D1NGn_FA
