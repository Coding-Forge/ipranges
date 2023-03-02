import requests
from bs4 import BeautifulSoup
import json
import logging
import pandas as pd


def get_data(azure_service):
    '''
    this function goes out to the download page for Azure Tags and Services and retrieves the latest publication of IP Ranges per service
    '''

    #create a logger
    logger = logging.getLogger('urlLogger')

    confirmation_url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
    
    # Making a GET request
    response = requests.get(confirmation_url)

    # Parsing the HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    for link in soup.find_all('a'):
        if "ServiceTags_Public" in link.get('href'):
            logger.info(f"this is the link it found: {link.get('href')}")
            data = json.loads(requests.get(link.get('href')).text)
            break

    df_tags = pd.json_normalize(data, record_path=['values'], meta=['changeNumber','cloud'],errors='ignore')

    ipranges=list(df_tags[df_tags['properties.systemService']==azure_service]['properties.addressPrefixes'])[0]
    logger.info(f'This is the first ip from the ranges {ipranges[0]}')
    return ipranges