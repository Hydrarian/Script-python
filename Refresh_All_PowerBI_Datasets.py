import adal
import requests
import json
import pandas
import time

authority_url = 'https://login.windows.net/common'
resource_url = 'https://analysis.windows.net/powerbi/api'
client_id = '2ac99ccf-962b-43e3-b6a0-84c439aa45c6'
username = 'pbiadmin@gberardi.com'
password = 'BI2020!!!'
context = adal.AuthenticationContext(authority=authority_url, validate_authority=True, api_version=None)
token = context.acquire_token_with_username_password(resource=resource_url, client_id=client_id, username=username, password=password)

access_token = token.get('accessToken')

groups_request_url = 'https://api.powerbi.com/v1.0/myorg/groups'

header = {'Authorization': f'Bearer {access_token}'}

groups_request = json.loads(requests.get(url=groups_request_url, headers=header).content)

groups = [d['id'] for d in groups_request['value']]

for group in groups:
    datasets_request_url = 'https://api.powerbi.com/v1.0/myorg/groups/' + group + '/datasets'
    datasets_request = json.loads(requests.get(url=datasets_request_url, headers=header).content)
    datasets = [d['id'] for d in datasets_request['value']]
    for dataset in datasets:
        if dataset!='97c114da-a51d-4313-8a01-f18e52f62c9b': #escludo il report del 2019
            refresh_url = 'https://api.powerbi.com/v1.0/myorg/groups/' + group + '/datasets/' + dataset + '/refreshes'
            r = requests.post(url=refresh_url, headers=header)
    time.sleep(420) #attendo 7 minuti prima di lanciare un altro group (area)
    
final = pandas.DataFrame()