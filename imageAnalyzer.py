
##################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the URL
# of the image we want as an input. Change these strings to run your own example.
#################################################################################################

# Your PAT (Personal Access Token) can be found in the Account's Security section
PAT = 'YOUR-TOKEN-HERE'
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'clarifai'
APP_ID = 'main'
# Change these to whatever model and image URL you want to use
MODEL_ID = 'food-item-v1-recognition'
MODEL_VERSION_ID = 'dfebc169854e429086aceb8368662641'
#IMAGE_URL = 'https://samples.clarifai.com/food-high-res/pexels-valeriya-27819688.jpg'

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

from email.mime import image
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from flask_restful import Resource
from flask import make_response, jsonify, request
from recipesResearcher import recipes_researcher

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

class ImageAnalyzer(Resource):

    def get(self):
        parameters = request.json
        if not parameters['image_url']:
            return make_response(jsonify("Please provide an image URL"), 400)
        else:
            return make_response(parameters['image_url'], 200)

    def post(self):
        parameters = request.json
        print(parameters)
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            image=resources_pb2.Image(
                                url=parameters['image_url']  # Change this to the URL of the image you want to use
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        # Since we have one input, one output will exist here
        output = post_model_outputs_response.outputs[0]

        print("Predicted concepts:")
        ingredients = []
        for concept in output.data.concepts:
            print("%s %.2f" % (concept.name, concept.value))
            ingredients.append(concept.name)
        my_ingredients = ','.join(ingredients)
        print(my_ingredients)
        recipe = recipes_researcher(my_ingredients)
        return make_response(jsonify(recipe), 200)

