import logging

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




    if azure_service:
        return func.HttpResponse(f"Hello, {name}. I was able to see that you want to update azure service {azure_service} located in the resource group {resource_group} for the following region {region}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
