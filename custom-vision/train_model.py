import time

import yaml
from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from msrest.authentication import ApiKeyCredentials

# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    training_key = data["cv_t_subscription_key"]
    endpoint = data["cv_t_endpoint"]

# load the credentials
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})

# create a client
trainer = CustomVisionTrainingClient(endpoint, credentials)

# find the project
project_name = f"waterfalls"
projects = trainer.get_projects()
for project in projects:
    if project.name == project_name:
        project_id = project.id

# run the training process
print("Training...")
iteration = trainer.train_project(project_id, force_train=True)
time.sleep(30)
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training status: " + iteration.status)
    print("Waiting 10 seconds...")
    time.sleep(10)
