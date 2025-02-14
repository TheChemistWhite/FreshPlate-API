from flask_restful import Api
import json
from flask import Flask
from imageAnalyzer import ImageAnalyzer


app = Flask(__name__)
api = Api(app)

api.add_resource(ImageAnalyzer, '/api/v1/findRecipe')

if __name__ == "__main__":
     app.run(host='0.0.0.0',port=5001 ,debug=True)