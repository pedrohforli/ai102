import os

import yaml
from azure.cognitiveservices.vision.face import FaceClient
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

# get the large person group
large_person_group_id = "business"
person_list = face_client.large_person_group_person.list(
    large_person_group_id=large_person_group_id
)

# find all the persons on group
person_map = {}
for person in person_list:
    person_map[person.person_id] = person.name

# for each file on test
for file in os.listdir("test"):
    # print the testing file
    pretty_print(f"Testing File: {file}")

    # go through urls in the file
    for url in open(f"test/{file}").readlines():
        # detect faces from the group
        pretty_print(f"URL: {url}", 2)
        faces_detected = face_client.face.detect_with_url(
            url=url, detection_model="detection_03"
        )

        # for each face detected
        for face in faces_detected:
            # get the face id
            face_id = face.face_id

            # check if the face matches one in our group
            response = face_client.face.identify(
                face_ids=[face_id], large_person_group_id=large_person_group_id
            )

            # if we find a response, get the person id
            person_id_recognized = (
                response[0].candidates[0].person_id
                if len(response[0].candidates) > 0
                else None
            )

            # print which person was recognized
            if person_id_recognized:
                pretty_print(
                    f"Person: {person_map[person_id_recognized]} was recognized", 4
                )
