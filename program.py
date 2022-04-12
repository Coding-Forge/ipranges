import urllib.request
import requests
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

def get_data(r):
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    for link in soup.find_all('a'):
        if "ServiceTags_Public" in link.get('href'):
            data = json.loads(requests.get(link.get('href')).text)

    return data


def main():

    confirmation_url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
    
    # Making a GET request
    r = requests.get(confirmation_url)
    
    data = get_data(r)
    df_tags = pd.json_normalize(data, record_path=['values'], meta=['changeNumber','cloud'],errors='ignore')

    # set an empty dataframe to be concatenated with all 
    # the data being retrieved
    df = pd.DataFrame()

    # probably want to call key vault to get this value
    API_KEY="D54MEY6ZMD"

    # defines what will be returned from the REST API
    PACKAGE="WS5"
    ipranges=list(df_tags[df_tags['properties.systemService']=="PowerBI"]['properties.addressPrefixes'])[0]

    response=""
    for ip in ipranges:
        my_request = f"https://api.ip2location.com/v2/?ip={ip.split('/')[0]}&key={API_KEY}&package={PACKAGE}"
        r = urllib.request.urlopen(my_request)
        response = r.read().decode('utf-8')
        df_temp = pd.json_normalize(json.loads(response))
        df_temp['CIDR']=ip
        
        df=pd.concat([df,df_temp])
        break
        # probably want to save this to OneDrive or Sharepoint online
    
    df.to_excel("/mnt/c/Users/brcampb/Documents/powerbi_ipranges.xlsx")


if __name__ == "__main__":
    main()