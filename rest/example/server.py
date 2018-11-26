
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

import requests

import pdb

#from flask.ext.jsonpify import jsonify

app = Flask(__name__)
api = Api(app)


class PSGAlg(Resource):

    def post(self):
        print(request.form)
        return ""


api.add_resource(PSGAlg , "/")


if __name__ == '__main__':
    app.run()

