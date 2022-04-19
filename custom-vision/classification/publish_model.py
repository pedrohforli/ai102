import yaml
from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from msrest.authentication import ApiKeyCredentials


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


# get the information about the connection
with open("../../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    training_key = data["cv_t_subscription_key"]
    endpoint = data["cv_t_endpoint"]
    prediction_resource_id = data["cv_p_resource_id"]

# load the credentials
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})

# create a client
trainer = CustomVisionTrainingClient(endpoint, credentials)

# find the project
project_name = f"waterfalls"
publish_iteration_name = "basic_waterfall_model"
project_id = None
projects = trainer.get_projects()
for project in projects:
    if project.name == project_name:
        project_id = project.id

if project_id is None:
    raise ValueError("Project does not exist")

# The iteration is now trained. Publish it to the project endpoint
iterations = trainer.get_iterations(project_id=project_id)
for iteration in iterations:
    pretty_print(iteration)
trainer.publish_iteration(
    project_id, iterations[0].id, publish_iteration_name, prediction_resource_id
)
print("Done!")
