from flask import Flask,Blueprint
from flask_restful import reqparse, abort, Api, Resource
from app.chat.chat import chat_service

chat = Api(chat_service)

##
## Actually setup the chat Api resource routing here
##
##chat.add_resource(SplashSetResource, '/v1/splashscreen')
