import yaml
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    subscription_key = data["ta_subscription_key"]
    endpoint = data["ta_endpoint"]

# authenticate user
credentials = AzureKeyCredential(subscription_key)
client = TextAnalyticsClient(endpoint=endpoint, credential=credentials)

# variable to store a JSON formatted document that contains two entries in a JSON array.
documents = [
    {"id": "1", "text": "This is a document written in English."},
    {"id": "2", "text": "Este es un document escrito en Español."},
    {"id": "3", "text": "这是一个用中文写的文件"}
]

# extract entities
response = client.detect_language(documents=documents)

# Output the result
for document in response:
    print("Document Id:", document.id)
    print("Language:", document.primary_language["name"])
    print("Confidence Score:", document.primary_language["confidence_score"])
    print()