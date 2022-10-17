# to check if the given set of variants are present in the VCF file


import pandas as pd
import os
 


def variant_notation_list(input_zip_file):
    try:
        df = pd.read_csv( input_zip_file, sep='\t', comment= '#', header=None, usecols=[0,1,3,4])

        df['variant_notation'] = df[0]+'_'+df[1].astype(str)+'_'+df[3] +'_'+df[4]

        variant_notation_list = df['variant_notation'].tolist()
        return variant_notation_list 
    except:
        print('This {} is skipped because of error'.format(input_zip_file))
        return None


if __name__ == '__main__':


    input_coordinates_list =[
    'chrM_8697_G_A',
    'chrM_8701_A_G',
    'chrM_10463_T_C',
    'chrM_13368_G_A',
    'chrM_15607_A_G',
    'chrM_15884_G_A',
    'chrM_15928_G_A',
    ]

    vcf_files_list = []
    for path, subdirs, files in os.walk(r'/varvisbucket/'):
        for name in files:
            if name.endswith('.gz'):
                vcf_files_list.append(os.path.join(path, name))
                #print(os.path.join(path, name))

    #chrM_files = [file for file in os.listdir() if file.endswith('.gz')]

    for f in vcf_files_list:
        #print(f)
        variant_list = variant_notation_list(f)
        if variant_list:
        #  print(set(input_coordinates_list).issubset(variant_notation_list))
            match_found = set(input_coordinates_list).issubset(variant_list)
            if match_found:
                print(f)


#https://stackoverflow.com/questions/3931541/how-to-check-if-all-of-the-following-items-are-in-a-list
#https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files
