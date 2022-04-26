from asyncio.log import logger
import pandas as pd
import urllib.request
import requests
import json


class find_my_location():
    def __init__(self, package, api_key):
        self.package = package
        self.api_key = api_key

    def get_azure_ip (self, ipranges):
        df = pd.DataFrame()

        response=""
        # don't need to write to a local file anymore
        #with open('iprange_doc.json', 'w') as f:
        for ip in ipranges:
            my_request = f"https://api.ip2location.com/v2/?ip={ip.split('/')[0]}&key={self.api_key}&package={self.package}"
            logger.info(f'This is the request url {my_request}')
            r = urllib.request.urlopen(my_request)
            response = r.read().decode('utf-8')
            df_temp = pd.json_normalize(json.loads(response))
            df_temp['CIDR']=ip
            
            df=pd.concat([df,df_temp])
            logger.info(f"what is the size of my dataframe {df.shape}")    
        return df, ipranges