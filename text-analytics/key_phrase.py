import yaml
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    subscription_key = data["ta_subscription_key"]
    endpoint = data["ta_endpoint"]


credentials = AzureKeyCredential(subscription_key)
client = TextAnalyticsClient(endpoint=endpoint, credential=credentials)

try:
    documents = [
        {"id": "1", "language": "ja", "text": "猫は幸せ"},
        {
            "id": "2",
            "language": "de",
            "text": "Fahrt nach Stuttgart und dann zum Hotel zu Fu.",
        },
        {
            "id": "3",
            "language": "en",
            "text": "My cat might need to see a veterinarian.",
        },
        {"id": "4", "language": "es", "text": "A mi me encanta el fútbol!"},
    ]

    for document in documents:
        print(
            "Asking key-phrases on '{}' (id: {})".format(
                document["text"], document["id"]
            )
        )

    response = client.extract_key_phrases(documents=documents)

    for document in response:
        print("Document Id: ", document.id)
        print("\tKey Phrases:")
        for phrase in document.key_phrases:
            print("\t\t", phrase)

except Exception as err:
    print("Encountered exception. {}".format(err))
