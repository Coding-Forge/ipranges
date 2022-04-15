from turtle import screensize
import pandas as pd
from lib.authentication import Authenticate
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


class Firewall(Authenticate):
    def __init__(self, subscription_id, account_name, resource_group, secret, tenant_id, client_id):
        self.subscription_id = subscription_id
        self.account_name = account_name
        self.resource_group = resource_group
        super().__init__(secret, tenant_id, client_id)

    def get_client(self, credentials):
        self.resource_client = ResourceManagementClient(credentials, self.subscription_id)
        self.storage_client = StorageManagementClient(credentials, self.subscription_id)

    def get_storage_account(self):
        self.storage_account = self.storage_client.storage_accounts.get_properties(self.resource_group,self.account_name)

    def update_rules(self, ip_ranges, df, region):

        ip = df[df['region_name']==region]['CIDR']

        str_ip_rules = ""
        ip_ranges = []

        # /31 and /32 are not allowed to be entered as IP Ranges using CIDR
        # must be entered as an IP
        for address in ip:
            if ":" not in address:
                if "31" in address:
                    val = address.replace("/31","")
                    str_ip_rules += f"IPRule(ip_address_or_range='{val}', action='Allow')|"
                    ip_ranges.append(IPRule(ip_address_or_range=val, action='Allow'))
                    val = val.rsplit(".",1)
                    val = val[0] + "." + str(int(val[1])+1)
                    str_ip_rules += f"IPRule(ip_address_or_range='{val}', action='Allow')|"
                    ip_ranges.append(IPRule(ip_address_or_range=val, action='Allow'))
                else:
                    str_ip_rules += f"IPRule(ip_address_or_range='{address}', action='Allow')|"
                    ip_ranges.append(IPRule(ip_address_or_range=address, action='Allow'))


        str_ip_rules=str_ip_rules[0:-1]
        ip_rules = list(str_ip_rules.split("|"))                    

        storage_account = self.storage_client.storage_accounts.update(
            self.resource_group, self.account_name,
            StorageAccountUpdateParameters (
                network_rule_set = NetworkRuleSet(
                    default_action='Deny',
                    ip_rules = ip_ranges
                )
            )
        )