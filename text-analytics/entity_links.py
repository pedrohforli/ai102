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
      "language": "en",
      "id": "1",
      "text": "I saw Venus shining in the sky"
    }
]

# extract entities
response = client.recognize_linked_entities(documents=documents)

# Output the result
for document in response:
    print("Document Id: ", document.id)
    print("Entities:")
    for idx, entity in enumerate(document.entities):
        print(f"\tEntity {idx}")
        print("\t\tLanguage:", entity.language)
        print("\t\tURL:", entity.url)
        print("\t\tSource:", entity.data_source)
        print("\t\tMatches:")
        for idx2, match in enumerate(entity.matches):
            print("\t\t\tMatch:", idx2)
            print("\t\t\t\tText:", match.text)
            print("\t\t\t\tConfidence Score:", match.confidence_score)
