# STRipy database scraping script
# Version: 1
# Author: Ram Kumar
# Date: 30 Aug 2022 
# Purpose: To scrape the 'Disease(s) and range of repeats' from the locus page e.g.: https://stripy.org/database/ARX_2




import pandas as pd
import requests
from bs4 import BeautifulSoup

def web_scraping_stripy_database(locus):
    response = requests.get('https://stripy.org/database/{}'.format(locus)).text
    soup = BeautifulSoup(response, "html.parser")

    table_content = soup.find('div', {'class' : 'maintable-diseases'})
    table = table_content.find('table')

    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    #column_headers = [i.text.strip() for i in rows[0].find_all('th') ]
    #column_headers.insert(0, 'Locus')

    parsed_data_list = []
    for row in rows[1:]:
        parsed_data = [i.text.strip() for i in row.find_all('td') ]
        parsed_data.insert(0, locus)
        parsed_data_list.append(parsed_data)
    
    return parsed_data_list


if __name__  == '__main__':

    stripy_df_locus_list = pd.read_html('https://stripy.org/database', encoding='utf8')[0]['Locus'].tolist()
     

    scrapped_data_list = []
    for locus in stripy_df_locus_list:
        data = web_scraping_stripy_database(locus) # produces a list of list
        for d in data:
            scrapped_data_list.append(d)  

    print(len(scrapped_data_list))

    df = pd.DataFrame(scrapped_data_list, columns = ['Locus', 'Disease', 'Onset', 'Inheritance', 'Normal', 'Intermediate', 'Pathogenic'])
            
    df.to_excel('STRipy_database_scrapped.xlsx', index=False)
 