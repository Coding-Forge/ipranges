from configparser import InterpolationMissingOptionError
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
from lib.reverse_ip_lookup import find_my_location
from utils.helper import get_data
from lib.blob_storage import Firewall


with open('./logging.yaml') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

logging.config.dictConfig(config)
logger = logging.getLogger('simpleExample')
import argparse

def main():
    parser = argparse.ArgumentParser(description="A python script that retrieves IP Addresses and updates Azure Service Firewalls")
    parser.add_argument("--azure_service", help="Pick which azure service you would like to know the ip ranges for")
    args = parser.parse_args()
    azure_service=args.azure_service

    # get the JSON document with Azure Services and their associated IPs
    ipranges = get_data(azure_service=azure_service)
    logger.info(f"The following are the ip ranges for {azure_service} {ipranges}")


    # Authenticate against Azure
    logger.info("Authenticating")
    bs_firewall = Firewall(
        client_id = 'a888b9fe-38ff-4551-844f-7416e1cbb89f',
        secret=os.getenv("ECOLAB_ADF_SP_SECRET"),
        tenant_id=os.getenv("TENANT_ID"),
        subscription_id = os.getenv("SUBSCRIPTION_ID"),
        account_name = "ecolabgen2",
        resource_group = "ecolab-rg"
    )
    
    # get the credentials that will be used in conjunction with the service client
    logger.info("Getting credentials")
    credentials = bs_firewall.get_credentials()

    # probably want to call key vault to get this value
    API_KEY="D54MEY6ZMD"

    # defines what will be returned from the REST API
    PACKAGE="WS5"

    logger.info("doing the reverse lookup using IP addresses")
    fml = find_my_location(package=PACKAGE, api_key=API_KEY)

    logger.info("getting the ipranges and the pandas dataframe")
    data, ipranges = fml.get_azure_ip(ipranges=ipranges)

    if data.shape[0]!=0:
        bs_firewall.update_rules(ip_ranges=ipranges,df=data,region="Iowa", credentials=credentials)
    else:
        raise Exception("dataframe is empty")


if __name__ == "__main__":
    main()