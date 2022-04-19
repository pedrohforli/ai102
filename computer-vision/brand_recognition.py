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
logo = "https://www.vw.com.br/content/dam/onehub_pkw/importers/br/models/my20/polo/stage/polo_alta.jpg"

# describe the image
response = client.analyze_image(logo, visual_features=["Brands"], max_candidates=1)
print([brand.name for brand in response.brands])

