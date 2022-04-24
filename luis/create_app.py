import time

import yaml
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.authoring.models import ApplicationCreateObject
from msrest.authentication import CognitiveServicesCredentials


def get_grandchild_id(model, child_name, grand_child_name):
    these_children = next(
        filter((lambda child: child.name == child_name), model.children)
    )
    these_grand_children = next(
        filter((lambda child: child.name == grand_child_name), these_children.children)
    )

    grand_child_id = these_grand_children.id

    return grand_child_id


# get the information about the connection
with open("../account_configs.yml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    authoring_key = data["luis_authoring_key"]
    authoring_endpoint = data["luis_authoring_endpoint"]


# setup the app configurations
app_name = "Contoso Pizza Company"
version_id = "0.1"
intent_name = "OrderPizzaIntent"

# create a connection to the authoring endpoint
client = LUISAuthoringClient(
    authoring_endpoint, CognitiveServicesCredentials(authoring_key)
)

# ########################## CREATE APP ########################## #
app_definition = ApplicationCreateObject(name=app_name, initial_version_id=version_id, culture='en-us')
app_id = client.apps.add(app_definition)
print("Created LUIS app with ID {}".format(app_id))

# ########################## ADD INTENT ########################## #
client.model.add_intent(app_id, version_id, intent_name)

# ########################## ADD ENTITIES ########################## #
client.model.add_prebuilt(app_id, version_id, prebuilt_extractor_names=["number"])

# define machine-learned entity
ml_entity_definition = [
    {
        "name": "Pizza",
        "children": [{"name": "Quantity"}, {"name": "Type"}, {"name": "Size"}],
    },
    {"name": "Toppings", "children": [{"name": "Type"}, {"name": "Quantity"}]},
]

# add entity to app
model_id = client.model.add_entity(
    app_id, version_id, name="Pizza order", children=ml_entity_definition
)

# define phrase_list - add phrases as significant vocabulary to app
phrase_list = {
    "enabledForAllModels": False,
    "isExchangeable": True,
    "name": "QuantityPhraselist",
    "phrases": "few,more,extra",
}

# add phrase list to app
client.features.add_phrase_list(app_id, version_id, phrase_list)

# Get entity and sub-entities
model_object = client.model.get_entity(app_id, version_id, model_id)
topping_quantity_id = get_grandchild_id(model_object, "Toppings", "Quantity")
pizza_quantity_id = get_grandchild_id(model_object, "Pizza", "Quantity")

# add model as feature to sub-entity model
prebuilt_feature_required_definition = {"model_name": "number", "is_required": True}
client.features.add_entity_feature(
    app_id, version_id, pizza_quantity_id, prebuilt_feature_required_definition
)

# add model as feature to sub-entity model
prebuilt_feature_not_required_definition = {"model_name": "number"}
client.features.add_entity_feature(
    app_id, version_id, topping_quantity_id, prebuilt_feature_not_required_definition
)

# add phrase list as feature to sub-entity model
phrase_list_feature_definition = {
    "feature_name": "QuantityPhraselist",
    "model_name": None,
}
client.features.add_entity_feature(
    app_id, version_id, topping_quantity_id, phrase_list_feature_definition
)

# ########################## LABELED EXAMPLES ########################## #
labeled_example_utterance_with_ml_entity = {
    "text": "I want two small seafood pizzas with extra cheese.",
    "intentName": intent_name,
    "entityLabels": [
        {
            "startCharIndex": 7,
            "endCharIndex": 48,
            "entityName": "Pizza order",
            "children": [
                {
                    "startCharIndex": 7,
                    "endCharIndex": 30,
                    "entityName": "Pizza",
                    "children": [
                        {
                            "startCharIndex": 7,
                            "endCharIndex": 9,
                            "entityName": "Quantity",
                        },
                        {
                            "startCharIndex": 11,
                            "endCharIndex": 15,
                            "entityName": "Size",
                        },
                        {
                            "startCharIndex": 17,
                            "endCharIndex": 23,
                            "entityName": "Type",
                        },
                    ],
                },
                {
                    "startCharIndex": 37,
                    "endCharIndex": 48,
                    "entityName": "Toppings",
                    "children": [
                        {
                            "startCharIndex": 37,
                            "endCharIndex": 41,
                            "entityName": "Quantity",
                        },
                        {
                            "startCharIndex": 43,
                            "endCharIndex": 48,
                            "entityName": "Type",
                        },
                    ],
                },
            ],
        }
    ],
}

print("Labeled Example Utterance:", labeled_example_utterance_with_ml_entity)

# Add an example for the entity.
# Enable nested children to allow using multiple models with the same name.
# The quantity sub-entity and the phrase_list could have the same exact name if this is set to True
client.examples.add(
    app_id=app_id,
    version_id=version_id,
    example_label_object=labeled_example_utterance_with_ml_entity,
    enable_nested_children=True,
)

# ########################## TRAIN MODEL ########################## #
client.train.train_version(app_id, version_id)
waiting = True
while waiting:
    info = client.train.get_status(app_id, version_id)

    # get_status returns a list of training statuses, one for each model. Loop through them and make sure all are
    # done.
    waiting = any(
        map(
            lambda x: "Queued" == x.details.status or "InProgress" == x.details.status,
            info,
        )
    )
    if waiting:
        print("Waiting 10 seconds for training to complete...")
        time.sleep(10)
    else:
        print("trained")
        waiting = False

# ########################## PUBLISH MODEL ########################## #
client.apps.update_settings(app_id, is_public=True)
response_endpoint_info = client.apps.publish(app_id, version_id, is_staging=False)
print("Response Endpoint Info:", response_endpoint_info)
