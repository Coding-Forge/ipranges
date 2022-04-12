import requests
from bs4 import BeautifulSoup
import json
import logging


def get_data():

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

    return data