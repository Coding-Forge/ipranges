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
import os


class Authenticate():
    def __init__(self, secret, tenant_id, client_id):
        self.tenant_id = tenant_id
        self.secret = secret
        self.client_id = client_id

    def get_credentials(self, spc=False):
        '''
        This function can provide credentials for a Service Principal or Client
        It is defaulted to return credentials for a Service Principal
        '''

        if spc:
            credentials = ServicePrincipalCredentials(
                client_id = self.client_id,
                secret=self.secret,
                tenant=self.tenant_id
            )
        else:
            credentials = ClientSecretCredential(
                client_id = self.client_id,
                client_secret=self.secret,
                tenant_id=self.tenant_id
            )

        return credentials