import time

import yaml
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    subscription_key = data["cv_subscription_key"]
    endpoint = data["cv_endpoint"]


# create a client to connect with the API
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

print("===== Detect Printed Text with OCR - local =====")
print()
# Get an image with printed text
local_image_printed_text_path = "images/printed_text.jpg"
with open(local_image_printed_text_path, "rb") as local_image_printed_text:
    ocr_result_local = client.recognize_printed_text_in_stream(local_image_printed_text)
    for region in ocr_result_local.regions:
        for line in region.lines:
            print("Bounding box: {}".format(line.bounding_box))
            s = ""
            for word in line.words:
                s += word.text + " "
            print(s)
print()

print("===== Detect Printed Text with OCR - remote =====")
print()
remote_printed_text_image_url = (
    "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files"
    "/master/ComputerVision/Images/printed_text.jpg "
)

ocr_result_remote = client.recognize_printed_text(remote_printed_text_image_url)
for region in ocr_result_remote.regions:
    for line in region.lines:
        print("Bounding box: {}".format(line.bounding_box))
        s = ""
        for word in line.words:
            s += word.text + " "
        print(s)
print()