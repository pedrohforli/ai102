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
    {
        "id": "1",
        "language": "en",
        "text": "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell "
        "BASIC interpreters for the Altair 8800.",
    },
    {
        "id": "2",
        "language": "es",
        "text": "La sede principal de Microsoft se encuentra en la ciudad de Redmond, a 21 kilómetros de "
        "Seattle.",
    },
]

# extract entities
response = client.recognize_entities(documents=documents)

# Output the result
for document in response:
    print("Document Id: ", document.id)
    print("\tEntities:")
    for idx, entity in enumerate(document.entities):
        print(f"\t\tEntity {idx}")
        print("\t\t\tName:", entity.text)
        print("\t\t\tType:", entity.category)
        if entity.subcategory is not None:
            print("\t\t\tSub-Type:", entity.subcategory)
        print("\t\t\tConfidence Score:", entity.confidence_score)
