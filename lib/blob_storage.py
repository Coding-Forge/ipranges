from turtle import screensize
from lib.authentication import Authenticate


class Firewall(Authenticate):
    def __init__(self, subscription_id, account_name, resource_group, secret, tenant_id, client_id):
        self.subscription_id = subscription_id
        self.account_name = account_name
        self.resource_group = resource_group
        super().__init__(secret, tenant_id, client_id)


    