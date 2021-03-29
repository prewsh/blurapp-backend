#
#@KEVIN Authentication module for registartion , login, validation , splashscreen, token Resend 
# Trans_type = 1 send , 2 buy  , 3 sell/withdraw
#
from flask import request
from flask_restful import Resource
from app.auth.model.Auth_DB import db, User,AuthCode, UserSchema ,UserAllSchema, AuthCodeSchema,Settings
from app.wallet.model.Wallet_DB import *
from app.auth.service.resource import random_gentarted,save_changes ,verify_expire_code,sms_token,generate_barcode
from app.auth.util.token import token_required,SECRET_KEY,auth,hash_password ,verify_password as veri_pass,token_decode
import jwt,json,secrets,datetime,uuid,requests
from app.auth.util.__code import *
from marshmallow import ValidationError, post_load
from sqlalchemy import or_, and_,desc
from app.twilio import *
from app.telegram import *
from decimal import *
import datetime



urlPost=""







#
#welcome page  
#
class HomeResource(Resource):
    def get(self):
        return  {'status': "error","data": {"code":202,"message": "Error Pages"}}, 200


#
#Registartion @phone,@device_id 
#

def MessageNotify(user_id,title,message):
    msg=Message(user_id=user_id,title=title,message=message)
    save_changes(msg)


