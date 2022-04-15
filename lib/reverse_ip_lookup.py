import pandas as pd
import urllib.request
import requests
import json


class find_my_location():
    def __init__(self, azure_service, package, api_key, data):
        self.azure_service = azure_service
        self.package = package
        self.api_key = api_key
        self.data = data


    def get_azure_ip (self):
        df = pd.DataFrame()
        df_tags = pd.json_normalize(self.data, record_path=['values'], meta=['changeNumber','cloud'],errors='ignore')

        ipranges=list(df_tags[df_tags['properties.systemService']==self.azure_service]['properties.addressPrefixes'])[0]

        response=""
        # don't need to write to a local file anymore
        #with open('iprange_doc.json', 'w') as f:
        for ip in ipranges:
            my_request = f"https://api.ip2location.com/v2/?ip={ip.split('/')[0]}&key={self.api_key}&package={self.package}"
            r = urllib.request.urlopen(my_request)
            response = r.read().decode('utf-8')
            df_temp = pd.json_normalize(json.loads(response))
            df_temp['CIDR']=ip
            
            df=pd.concat([df,df_temp])