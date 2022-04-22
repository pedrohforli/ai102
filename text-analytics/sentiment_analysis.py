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
        "text": "I really enjoy the new XBox One S. It has a clean look, it has 4K/HDR resolution and it is affordable.",
    },
    {
        "id": "2",
        "language": "es",
        "text": "Si usted quiere comunicarse con Carlos, usted debe de llamarlo a su telefono movil. Carlos es muy "
        "responsable, pero necesita recibir una notificacion si hay algun problema.",
    },
    {
        "id": "3",
        "language": "en",
        "text": "The Grand Hotel is a new hotel in the center of Seattle. It earned 5 stars in my review, and has the "
        "classiest decor I've ever seen.",
    },
]

# extract entities
response = client.analyze_sentiment(documents=documents)

# Output the result
for document in response:
    print("Document Id:", document.id)
    print("Sentiment:", document.sentiment)
    for idx, sentence in enumerate(document.sentences):
        print(f"\tSentence {idx}")
        print("\t\tText:", sentence.text)
        print("\t\tSentiment:", sentence.sentiment)
        print("\t\tConfidence Score:", sentence.confidence_scores)
