import urllib.request
import requests
import pandas as pd
import json
import logging
import logging.config
import yaml
import os

from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import ClientSecretCredential
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    StorageAccountCreateParameters,
    NetworkRuleSet,
    IPRule,
    StorageAccountUpdateParameters,
    Sku,
    SkuName,
    Kind
)
from utils.helper import get_data
from lib.blob_storage import Firewall


with open('./logging.yaml') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

logging.config.dictConfig(config)
logger = logging.getLogger('simpleExample')


def main():

    data = get_data()
    df_tags = pd.json_normalize(data, record_path=['values'], meta=['changeNumber','cloud'],errors='ignore')

    # set an empty dataframe to be concatenated with all 
    # the data being retrieved
    df = pd.DataFrame()

    bs_firewall = Firewall(
        client_id = 'a888b9fe-38ff-4551-844f-7416e1cbb89f',
        secret=os.getenv("ECOLAB_ADF_SP_SECRET"),
        tenant_id=os.getenv("TENANT_ID"),
        subscription_id = os.getenv("SUBSCRIPTION_ID"),
        account_name = "ecolabgen2",
        resource_group = "ecolab-rg"
    )
    
    #creds = bs_firewall.get_credentials()
    #print(creds)

    exit

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