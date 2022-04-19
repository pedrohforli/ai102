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

# Generate a thumbnail from a URL image
# URL of faces
remote_image_url_thumb = (
    "https://raw.githubusercontent.com/gottagetgit/AI102Files/main/Computer_Vision"
    "/Analyze_images_using_Computer_Vision_API/Images/Faces.jpg "
)

print("Generating thumbnail from a URL image...")
# Returns a Generator object, a thumbnail image binary (list).
thumb_remote = client.generate_thumbnail(
    100, 100, remote_image_url_thumb, True
)

# Write the image binary to file
with open("thumb_remote.png", "wb") as f:
    for chunk in thumb_remote:
        f.write(chunk)

print("Thumbnail saved to local folder.")

