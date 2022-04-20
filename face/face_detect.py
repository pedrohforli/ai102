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
    print(" " * indent + type(klass).__name__ + ":")
    indent += 4
    for k, v in klass.__dict__.items():
        if "__dict__" in dir(v):
            pretty_print(v, indent)
        elif isinstance(v, list):
            for item in v:
                pretty_print(item, indent)
        else:
            print(" " * indent + k + ": " + str(v))


# Authenticate
face_client = FaceClient(endpoint, CognitiveServicesCredentials(subscription_key))
face_image_url = "https://raw.githubusercontent.com/axel-sirota/build-face-recognition-azure/main/images/business.jpeg"

# run the face recognition to find faces
detected_faces = face_client.face.detect_with_url(url=face_image_url)
print("Detected faces from image:")
for face in detected_faces:
    pretty_print(face)


# select specific attributes
detected_faces = face_client.face.detect_with_url(
    url=face_image_url,
    return_face_landmarks=True,
    return_face_attributes=["Age", "Gender", "HeadPose", "Emotion", "Glasses", "Hair"],
)
print("Detected faces from image:")
for face in detected_faces:
    pretty_print(face)
