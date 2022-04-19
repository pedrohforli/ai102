import yaml

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    subscription_key = data["cv_subscription_key"]
    endpoint = data["cv_endpoint"]

# create a client to connect with the API
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# select the image to process
image_url = "https://pbs.twimg.com/media/FPBAfjxXMAQN2uh.jpg"

# describe the image
response = client.describe_image(image_url, max_candidates=1)
print(response.captions[0])
