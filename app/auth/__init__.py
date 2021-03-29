import os
from flask import Flask,Blueprint
from flask_restful import reqparse, abort, Api, Resource

from app.auth.controller.Auth import *
app_service = Blueprint('api', __name__)
api = Api(app_service)


##
## Actually setup the Api resource routing here
##

api.add_resource(RegResource, '/v1/registration')
api.add_resource(ValidateResource, '/v1/validate')
api.add_resource(PasswordSetResource, '/v1/password_set')
api.add_resource(LoginSetResource, '/v1/login')
api.add_resource(ProfileUpdateSetResource, '/v1/profile_update')
api.add_resource(SettingSetResource, '/v1/setting_update')
api.add_resource(RecoverySetResource, '/v1/account_recovery')

##
## Other endpoint resource routing here
##
api.add_resource(EMailSetResource, '/v1/email')


