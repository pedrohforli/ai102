import os
import time

import yaml
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    subscription_key = data["fc_subscription_key"]
    endpoint = data["fc_endpoint"]


# Do not worry about this function, it is for pretty printing the attributes!
def pretty_print(klass, indent=0):
    if "__dict__" in dir(klass):
        print(" " * indent + type(klass).__name__ + ":")
        indent += 4
        for k, v in klass.__dict__.items():
            if "__dict__" in dir(v):
                pretty_print(v, indent)
            elif isinstance(v, list):
                print(" " * indent + k + ":")
                for item in v:
                    pretty_print(item, indent)
            else:
                print(" " * indent + k + ": " + str(v))
    else:
        indent += 4
        print(" " * indent + klass)


# Authenticate
face_client = FaceClient(endpoint, CognitiveServicesCredentials(subscription_key))

# setup a large person group
large_person_group_id = "business"
face_client.large_person_group.create(
    large_person_group_id=large_person_group_id, name="businesspeople"
)

# go through the files within the faces directory
for person_file in os.listdir("faces"):
    # extract the person name for the file name
    person_name = person_file.split(".")[0]

    # add the person to the group
    person = face_client.large_person_group_person.create(
        large_person_group_id=large_person_group_id, name=person_name
    )

    # go through the images urls in the person txt file
    for image_url in open(f"faces/{person_file}", "r").readlines():
        # add the face to the person
        face_client.large_person_group_person.add_face_from_url(
            large_person_group_id=large_person_group_id,
            person_id=person.person_id,
            url=image_url,
        )

# print the person registered in the person group
for person in face_client.large_person_group_person.list(
    large_person_group_id=large_person_group_id
):
    pretty_print(person)

# train the person group model
face_client.large_person_group.train(large_person_group_id=large_person_group_id)
for i in range(10):
    response = face_client.large_person_group.get_training_status(
        large_person_group_id=large_person_group_id
    )
    if response.status != TrainingStatusType.succeeded:
        time.sleep(5)
    else:
        print("Training Succeeded")
        break
print("Done")

# face_client.large_person_group.delete(large_person_group_id=large_person_group_id)
