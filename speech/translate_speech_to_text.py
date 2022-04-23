import yaml
from azure.cognitiveservices.speech import CancellationReason
from azure.cognitiveservices.speech import ResultReason
from azure.cognitiveservices.speech import SpeechConfig
from azure.cognitiveservices.speech.translation import SpeechTranslationConfig
from azure.cognitiveservices.speech.translation import TranslationRecognizer


# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    subscription_key = data["sp_subscription_key"]
    location = data["sp_location"]
    endpoint = data["sp_endpoint"]

# Creates an instance of a speech translation config with specified subscription key and service region.
translation_config = SpeechTranslationConfig(
    subscription=subscription_key, region=location
)
speech_config = SpeechConfig(subscription=subscription_key, region=location)

# Sets source and target languages
fromLanguage = "pt-BR"
translation_config.speech_recognition_language = fromLanguage

# Add more than one language to the collection.
# using the add_target_language() method
translation_config.add_target_language("en-US")
translation_config.add_target_language("it-IT")
translation_config.add_target_language("tlh-Latn")

# Creates a translation recognizer using and audio file as input.
recognizer = TranslationRecognizer(translation_config=translation_config)

# Starts translation, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed. It returns the recognized text as well as the translation.
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query.
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
print("Say something...")
result = recognizer.recognize_once()

# Check the result
if result.reason == ResultReason.TranslatedSpeech:
    print("RECOGNIZED '{}': {}".format(fromLanguage, result.text))
    for key in result.translations:
        print("TRANSLATED into {}: {}".format(key, result.translations[key]))
elif result.reason == ResultReason.RecognizedSpeech:
    print("RECOGNIZED: {} (text could not be translated)".format(result.text))
elif result.reason == ResultReason.NoMatch:
    print("NOMATCH: Speech could not be recognized: {}".format(result.no_match_details))
elif result.reason == ResultReason.Canceled:
    print("CANCELED: Reason={}".format(result.cancellation_details.reason))
    if result.cancellation_details.reason == CancellationReason.Error:
        print(
            "CANCELED: ErrorDetails={}".format(
                result.cancellation_details.error_details
            )
        )
