import yaml
from azure.cognitiveservices.speech import CancellationReason
from azure.cognitiveservices.speech import ResultReason
from azure.cognitiveservices.speech import SpeechConfig
from azure.cognitiveservices.speech import SpeechSynthesizer
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

# Creates a speech synthesizer using the configured voice for audio output.
speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)

# Sets source and target languages
fromLanguage = "pt-BR"
translation_config.speech_recognition_language = fromLanguage

# Add more than one language to the collection.
# using the add_target_language() method
translation_config.add_target_language("en-US")
translation_config.add_target_language("it-IT")

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
    # Output the text for the recognized speech input
    print("RECOGNIZED '{}': {}".format(fromLanguage, result.text))

    # Loop through the returned translation results
    for key in result.translations:

        # Using the Key and Value components of the returned dictionary for the translated results
        # The first portion gets the key (language code) while the second gets the Value
        # which is the translated text for the language specified
        # Output the language and then the translated text
        print("TRANSLATED into {}: {}".format(key, result.translations[key]))

        if key == "en-US":
            speech_config.speech_synthesis_voice_name = "en-US-SaraNeural"

            # Update the speech synthesizer to use the proper voice
            speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)

            # Use the proper voice, from the speech synthesizer configuration, to narrate the translated result
            # in the native speaker voice.
            speech_synthesizer.speak_text_async(result.translations[key]).get()
        elif key == "it-IT":
            speech_config.speech_synthesis_voice_name = "it-IT-DiegoNeural"

            # Update the speech synthesizer to use the proper voice
            speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)

            # Use the proper voice, from the speech synthesizer configuration, to narrate the translated result
            # in the native speaker voice.
            speech_synthesizer.speak_text_async(result.translations[key]).get()
        else:
            raise NotImplementedError
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
