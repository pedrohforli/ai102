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

print("===== Batch Read File - remote =====")
# get an image with handwritten text
remote_image_handw_text_url = (
    "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive"
    "-services/Computer-vision/Images/readsample.jpg"
)

# Call API with URL and raw response (allows you to get the operation location)
recognize_handw_results = client.read(remote_image_handw_text_url, raw=True)

# Get the operation location (URL with an ID at the end) from the response
operation_location_remote = recognize_handw_results.headers["Operation-Location"]

# Grab the ID from the URL
operation_id = operation_location_remote.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results
while True:
    get_handw_text_results = client.get_read_result(operation_id)
    if get_handw_text_results.status not in ["notStarted", "running"]:
        break
    time.sleep(1)

# Print the detected text, line by line
if get_handw_text_results.status == OperationStatusCodes.succeeded:
    for text_result in get_handw_text_results.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()

print("===== Detect Printed Text with the Read API - remote =====")
print()
# Get an image with handwritten text
remote_image_handw_text_url = (
    "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive"
    "-services/Computer-vision/Images/readsample.jpg "
)

# Call API with URL and raw response (allows you to get the operation location)
recognize_handw_results = client.read(
    remote_image_handw_text_url, raw=True
)

# Get the operation location (URL with an ID at the end) from the response
operation_location_remote = recognize_handw_results.headers["Operation-Location"]
# Grab the ID from the URL
operation_id = operation_location_remote.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results
while True:
    get_handw_text_results = client.get_read_result(operation_id)
    if get_handw_text_results.status not in ["notStarted", "running"]:
        break
    time.sleep(1)

# Print the detected text, line by line
if get_handw_text_results.status == OperationStatusCodes.succeeded:
    for text_result in get_handw_text_results.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()