import os
from flask import Flask,Blueprint
from flask_restful import reqparse, abort, Api, Resource

from app.wallet.controller.Wallet import *


wallet_service = Blueprint('wallet', __name__)
wallet = Api(wallet_service)


##
## Actually setup the Api resource routing here
##

wallet.add_resource(HomeResource, '/v1/home')
















