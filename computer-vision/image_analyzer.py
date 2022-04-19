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

