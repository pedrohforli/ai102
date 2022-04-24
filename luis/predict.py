import json

import yaml
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    authoring_key = data["luis_authoring_key"]
    authoring_endpoint = data["luis_authoring_endpoint"]
    prediction_key = data["luis_prediction_key"]
    prediction_endpoint = data["luis_prediction_endpoint"]


# setup the app configurations
app_name = "Contoso Pizza Company"
prediction_request = {"query": "I want two small pepperoni pizzas with more salsa"}

# create a connection to the prediction and authoring endpoint
client = LUISAuthoringClient(
    authoring_endpoint, CognitiveServicesCredentials(authoring_key)
)
client_runtime = LUISRuntimeClient(
    endpoint=prediction_endpoint,
    credentials=CognitiveServicesCredentials(prediction_key),
)

# find the app id
app_id = [app.id for app in client.apps.list() if app.name == app_name][0]

# get the prediction response
prediction_response = client_runtime.prediction.get_slot_prediction(
    app_id, "Production", prediction_request
)

# get the top intent and sentiment
print("Top intent: {}".format(prediction_response.prediction.top_intent))
print("Sentiment: {}".format(prediction_response.prediction.sentiment))

# extract intents
print("Intents: ")
for intent in prediction_response.prediction.intents:
    print("\t{}".format(json.dumps(intent)))

# extract entities
print("Entities: {}".format(prediction_response.prediction.entities))
