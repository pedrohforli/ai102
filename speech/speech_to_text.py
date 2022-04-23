import yaml
from azure.cognitiveservices.speech import AudioConfig
from azure.cognitiveservices.speech import CancellationReason
from azure.cognitiveservices.speech import ResultReason
from azure.cognitiveservices.speech import SpeechConfig
from azure.cognitiveservices.speech import SpeechRecognizer

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    subscription_key = data["sp_subscription_key"]
    location = data["sp_location"]
    endpoint = data["sp_endpoint"]

# create a speech configuration
speech_config = SpeechConfig(subscription=subscription_key, region=location)
speech_config.enable_dictation()

# setup an audio input file
audio_input = AudioConfig(filename="media/Speech_Media_narration.wav")

# generate the speech recognizer
speech_recognizer = SpeechRecognizer(
    speech_config=speech_config, audio_config=audio_input
)

# run the recognition api
result = speech_recognizer.recognize_once()

# print the text output according to the result
if result.reason == ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
