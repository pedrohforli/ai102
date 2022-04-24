import json

import yaml
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from azure.cognitiveservices.speech import CancellationReason
from azure.cognitiveservices.speech import ResultReason
from azure.cognitiveservices.speech import SpeechConfig
from azure.cognitiveservices.speech.intent import IntentRecognizer
from azure.cognitiveservices.speech.intent import LanguageUnderstandingModel
from msrest.authentication import CognitiveServicesCredentials

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    authoring_key = data["luis_authoring_key"]
    authoring_endpoint = data["luis_authoring_endpoint"]
    authoring_location = data["luis_authoring_location"]
    prediction_key = data["luis_prediction_key"]
    prediction_endpoint = data["luis_prediction_endpoint"]
    prediction_location = data["luis_prediction_location"]

# setup the app configurations
app_name = "Clock"
version_id = "0.1"

# create a connection to the prediction and authoring endpoint
client = LUISAuthoringClient(
    endpoint=authoring_endpoint, credentials=CognitiveServicesCredentials(authoring_key)
)

# find the app id
app_id = [app.id for app in client.apps.list() if app.name == app_name][0]

# create a speech configuration
speech_config = SpeechConfig(subscription=authoring_key, region=authoring_location)

# get the intent recognizer
speech_recognizer = IntentRecognizer(speech_config)

# if we want to create an intent recognizer from an audio file we add it
# audio_input = AudioConfig(filename="<path to audio file>")
# recognizer = IntentRecognizer(speech_config, audio_input)

# get the language understanding model
model_object = LanguageUnderstandingModel(
    subscription=prediction_key,
    region=prediction_location,
    app_id=app_id,
)

# add intents
for m in client.model.list_models(app_id, version_id):
    speech_recognizer.add_intent(model_object, m.name, m.id)

print("Say something...")
result = speech_recognizer.recognize_once()

# check the results
if result.reason == ResultReason.RecognizedIntent:
    print('Recognized: "{}" with intent id `{}`'.format(result.text, result.intent_id))
elif result.reason == ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))

    prediction_request = {"query": result.text}

    client_runtime = LUISRuntimeClient(
        endpoint=prediction_endpoint,
        credentials=CognitiveServicesCredentials(prediction_key),
    )

    prediction_response = client_runtime.prediction.get_slot_prediction(
        app_id, "Production", prediction_request
    )

    print("Top intent: {}".format(prediction_response.prediction.top_intent))
    print("Sentiment: {}".format(prediction_response.prediction.sentiment))
    print("Intents: ")
    for intent in prediction_response.prediction.intents:
        print("\t{}".format(json.dumps(intent)))
    print("Entities: {}".format(prediction_response.prediction.entities))

elif result.reason == ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == ResultReason.Canceled:
    print("Intent recognition canceled: {}".format(result.cancellation_details.reason))
    if result.cancellation_details.reason == CancellationReason.Error:
        print("Error details: {}".format(result.cancellation_details.error_details))
