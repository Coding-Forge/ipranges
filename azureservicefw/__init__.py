import urllib.request
import requests
import json
import logging
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
from lib.reverse_ip_lookup import find_my_location
from lib.blob_storage import Firewall

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    azure_service = req.params.get('azure_service')
    account_name = req.params.get('account_name')
    resource_group = req.params.get('resource_group')
    region = req.params.get('region')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
            azure_service = req_body.get('azure_service')
            account_name = req_body.get('account_name')
            resource_group = req_body.get('resource_group')
            region = req_body.get('region')



    ipranges = get_data(azure_service=azure_service)
    logging.info(f"The following are the ip ranges for {azure_service} {ipranges}")


    # Authenticate against Azure
    logging.info("Authenticating")
    bs_firewall = Firewall(
        client_id = 'a888b9fe-38ff-4551-844f-7416e1cbb89f',
        secret=os.getenv("ECOLAB_ADF_SP_SECRET"),
        tenant_id=os.getenv("TENANT_ID"),
        subscription_id = os.getenv("SUBSCRIPTION_ID"),
        account_name = "ecolabgen2",
        resource_group = "ecolab-rg"
    )
    
    # get the credentials that will be used in conjunction with the service client
    logging.info("Getting credentials")
    credentials = bs_firewall.get_credentials()

    # probably want to call key vault to get this value
    API_KEY="D54MEY6ZMD"

    # defines what will be returned from the REST API
    PACKAGE="WS5"

    logging.info("doing the reverse lookup using IP addresses")
    fml = find_my_location(package=PACKAGE, api_key=API_KEY)

    logging.info("getting the ipranges and the pandas dataframe")
    data, ipranges = fml.get_azure_ip(ipranges=ipranges)

    if data.shape[0]!=0:
        bs_firewall.update_rules(ip_ranges=ipranges,df=data,region="Iowa", credentials=credentials)
    else:
        raise Exception("dataframe is empty")


    if azure_service:
        return func.HttpResponse(f"Hello, {name}. I was able to see that you want to update azure service {azure_service} located in the resource group {resource_group} for the following region {region}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
