import uuid
from pprint import pprint

import requests
import yaml

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    subscription_key = data["tl_subscription_key"]
    endpoint = data["tl_text_endpoint"]

print("------- Using REST API setup -------")
# Add your location, also known as region. The default is global.
# This is required if using a Cognitive Services resource.
location = "brazilsouth"

# setup the path
params = {
    'api-version': '3.0',
    'from': 'en',
    'to': ['de', 'it', 'pt'],
}

# build the url
constructed_url = f"{endpoint}/translate?api-version={params['api-version']}&from={params['from']}"
for ln in params["to"]:
    constructed_url += f"&to={ln}"

# setup the request headers
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4()),
}

# pass text to be translated
body = [{'text': 'Hello World!'}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()
pprint(response)
