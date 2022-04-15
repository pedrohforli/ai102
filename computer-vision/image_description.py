import os

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# get the information about the connection
subscription_key = os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]
endpoint = os.environ["COMPUTER_VISION_ENDPOINT"]

# create a client to connect with the API
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# select the image to process
image_url = "https://pbs.twimg.com/media/FPBAfjxXMAQN2uh.jpg"

# describe the image
response = client.describe_image(image_url, max_candidates=1)
print(response.captions[0])
