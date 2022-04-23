import yaml
from azure.cognitiveservices.speech import CancellationReason
from azure.cognitiveservices.speech import ResultReason
from azure.cognitiveservices.speech import SpeechConfig
from azure.cognitiveservices.speech import SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    subscription_key = data["sp_subscription_key"]
    location = data["sp_location"]
    endpoint = data["sp_endpoint"]

# create a speech configuration
speech_config = SpeechConfig(subscription=subscription_key, region=location)
speech_config.speech_synthesis_voice_name = "pt-BR-AntonioNeural"

# Creates an audio configuration that points to an audio file.
# Replace with your own audio filename.
audio_filename = "media/text-to-speech-py.wav"
audio_output = AudioOutputConfig(filename=audio_filename)

# Creates a speech synthesizer using the default speaker as audio output.
speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)
speech_output = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

# Receives a text from console input.
text = input("Type some text that you want to speak...")

# Synthesizes the received text to speech.
_ = speech_synthesizer.speak_text_async(text).get()

# Synthesizes the received text to speech.
result = speech_output.speak_text_async(text).get()

# Checks result.
if result.reason == ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized to [{}] for text [{}]".format(audio_filename, text))
elif result.reason == ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
