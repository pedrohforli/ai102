import os
import yaml

from azure.cognitiveservices.vision.customvision.training import (
    CustomVisionTrainingClient,
)
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateBatch,
    ImageFileCreateEntry,
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

# Create a new project
print("Creating project...")
domains = trainer.get_domains()
for domain in domains:
    if domain.name.startswith("Landmark"):
        domain_id = domain.id
project_name = f"waterfalls"
project = trainer.create_project(
    name=project_name, domain_id=domain_id, classification_type="Multiclass"
)
print("Adding images...")

for root, dirs, files in os.walk("images", topdown=False):
    try:
        root_dir, category = root.split("\\")
        if category != "Test":
            image_list = []
            tag_type = "Regular" if category != "Negative" else "Negative"
            category_tag = trainer.create_tag(
                project.id, category.lower(), type=tag_type
            )
            for image in files:
                if image != ".DS_Store":
                    print(f"Dealing with {category}/{image}")
                    with open(
                        os.path.join(root_dir, category, image), "rb"
                    ) as image_contents:
                        image_entry = ImageFileCreateEntry(
                            name=image,
                            contents=image_contents.read(),
                            tag_ids=[category_tag.id],
                        )
                        image_list.append(image_entry)

            print(f"Going to upload images from {category}")
            upload_result = trainer.create_images_from_files(
                project.id, ImageFileCreateBatch(images=image_list)
            )
            if not upload_result.is_batch_successful:
                print("Image batch upload failed.")
                for image in upload_result.images:
                    if image.status != "OK":
                        print(image)
                    print("Image status: ", image.status)

    except ValueError:
        pass  # base directory
