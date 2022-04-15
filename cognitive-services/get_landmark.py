import os

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# get the information about the connection
subscription_key = os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]
endpoint = os.environ["COMPUTER_VISION_ENDPOINT"]

# create a client to connect with the API
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# select the image to process
cristo = "https://visit.rio/wp-content/uploads/2015/10/28128553253_4e763a380e_k-250x250.jpg"

# describe the image
response = client.analyze_image(cristo, details=["Landmarks"], max_candidates=1)
print(
    set(
        [
            land.name
            for cat in response.categories
            if cat.detail is not None
            for land in cat.detail.landmarks
        ]
    )
)

