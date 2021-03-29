#
#@KEVIN Authentication module for registartion , login, validation , splashscreen, token Resend 
#
from flask import request
from flask_restful import Resource
from app.auth.model.Auth_DB import db, User,Banks,AuthCode,Settings, UserSchema ,BanksSchema ,UserAllSchema, AuthCodeSchema,ActivitiesLog,MessageAllSchemaPost
from app.auth.service.resource import random_gentarted,save_changes ,verify_expire_code,sms_token
from app.auth.util.token import token_required,SECRET_KEY,auth,hash_password ,verify_password as veri_pass,token_decode
import jwt,json,secrets,datetime,uuid
from app.auth.util.__code import *
from app.auth.service.resource import  formate_number
from marshmallow import ValidationError, post_load
from sqlalchemy import or_, and_
from app.twilio import *
from app.telegram import *
from app.email import *
from device_detector import SoftwareDetector
from datetime import datetime as datetimer ,date


ua = 'Mozilla/5.0 (Linux; Android 6.0; 4Good Light A103 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36'
device = SoftwareDetector(ua).parse()


users_schema = UserAllSchema(many=True)
banks_schema =BanksSchema(many=True)
user_schema = UserSchema()
user_all_schema = UserAllSchema()
authcode_schema =  AuthCodeSchema()
msg_schema = MessageAllSchemaPost()



#
#password verify @param {phone & passowrd}
#
@auth.verify_password
def verify_password(phone, password):
    user = User.query.filter_by(phone = phone ,status=1).first()
    if not user or not veri_pass(user.password,password):
       return False
    user = user
    return True


@auth.error_handler
def auth_error():
     return  {'status': "error","data": {"code":202,"message": "Invalid Login details"}}, 200
#
#welcome page  
#
class HomeResource(Resource):
    def get(self):
        return {"Facial Biometric API"}, 200

#
#Registartion @phone,@device_id 
#

class RegResource(Resource):
    
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users)
        return {'status': 'success', 'data': users}, 200

    def post(self):
        verify_code = verify_expire_code["code"]= random_gentarted(4) 
        json_data = request.get_json(force=True)
        if not json_data:
            return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided"}}, 200
        try:
            data = authcode_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200

        auth_user_check= AuthCode.query.filter(and_(AuthCode.phone==data['phone'],AuthCode.device_id==data['device_id'],AuthCode.auth_status == 1)).first()
        if auth_user_check:
            return  {'status': "error","data": {"code":FAILED, "message":'Phone Number already in use' }}, 200

        auth_user = AuthCode.query.filter(and_(AuthCode.phone==data['phone'],AuthCode.device_id==data['device_id'],AuthCode.auth_status == 0)).first()
        if not auth_user:
            user = AuthCode(phone=data['phone'],device_id=data['device_id'],activation=verify_code,auth_status=0)
            save_changes(user)
            #remove verify_code on production
            code_msg= "Your Verification code is  :" + str(verify_code)
            #sms_token(str(data['phone']),code_msg)
            SendSMSNg(str(data['phone']),str(verify_code))

            return  {'status': "success","data": {"code":SUCCESSFUL,"verify_code": verify_code}}, 200
        else:
            auth_user.activation=verify_code
            db.session.commit()
            #remove verify_code on production
            code_msg= "Your Verification code is  :" + str(verify_code)
            #sms_token(str(data['phone']),code_msg)
            SendSMSNg(str(data['phone']),str(verify_code))

            return  {'status': "success","data": {"code":SUCCESSFUL,"verify_code": verify_code}}, 200
            
        

        
    #
    #Resend verification code @param {phone,@device_id,activation_code}
    #
    def put(self):
        verify_code = verify_expire_code["code"]= random_gentarted(4) 
        json_data = request.get_json(force=True)
        if not json_data:
               return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided"}}, 200
        try:
            data = authcode_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200 

        auth_user = AuthCode.query.filter(and_(AuthCode.phone==data['phone'],AuthCode.device_id==data['device_id'],AuthCode.auth_status == 0)).first()
        if not auth_user:
            return  {'status': "error","data": {"code":INVALID_CODE_RESEND_DETAILS , "message":'Invalid user details' }}, 200

        auth_user.activation=verify_code
        auth_user =data
        db.session.commit()
        #remove verify_code on production
        code_msg= "Your Verification code is  :" + str(verify_code)
        #sms_token(str(data['phone']),code_msg)
        SendSMSNg(str(data['phone']),str(verify_code))

        return  {'status': "success","data": {"code":SUCCESSFUL,"message":'successful',"verify_code": verify_code}}, 200
     
    #
    #Delete Data Remove on production 
    #
    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided"}}, 200
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200  

        user= User.query.filter_by(phone=data['phone']).delete()
    
        if not user:
            return  {'status': "error","data": {"code":USER_NOT_FOUND, "message":'User does not exist' }}, 200
        db.session.commit()
        return  {'status': "success","data": {"code":SUCCESSFUL,"message":'User data has been deleted'}}, 200
       

#
#Validation  @param  {@phone,@device_id,@activation_code}
#
class ValidateResource(Resource):
    #CREATE PIN
    @token_required
    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        if not json_data:
            return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided"}}, 200
       
        try:
            data = user_all_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200 

    
        if not 'pin' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (pin) field."}}, 200 

        user = User.query.filter_by(id=self['user_id']).first()
        if  user: 
            user.pin =hash_password(data['pin'])
            db.session.commit()
            return  {'status': "success","data": {"code":LOGIN_SUCCESSFUL,"message": "Transaction pin created "}}, 200
        else:
            pass 
            return { "status": 'error', "data": {'code':FAILED ,'message': 'Action was not successful'}}, 200 
        

    #Verify phone
    def put(self):
        json_data = request.get_json(force=True)
        print(json_data)
        if not json_data:
            return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided"}}, 200
       
        try:
            data = authcode_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200 

    
        if not 'activation_code' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (activation_code) field."}}, 200 

        user = AuthCode.query.filter_by(phone=data['phone'],device_id=data['device_id'],activation=data['activation_code'],auth_status = 0).first()
        if not user:
            return  {'status': "error","data": {"code":INVALID_CODE,"message": "Activation code does not match."}}, 200 
            
        validCode= verify_expire_code.get('code')
        if not validCode:
            return  {'status': "error","data": {"code":EXPIRED_CODE,"message": "Activation code has expired."}}, 200
        else:
            user=User(phone=data['phone'],device_id=data['device_id'],password=hash_password(data['password']),activation=1,level=PHONE_LEVEL,status=1,notify=1,auth2fa=1,verify_me=0, bank="",ref_id=data['ref_id'],first_name="",last_name="")
            save_changes(user)
            if user:
               auth_user = AuthCode.query.filter(and_(AuthCode.phone==data['phone'],AuthCode.device_id==data['device_id'],AuthCode.activation == data['activation_code'])).first() 
               auth_user.auth_status=1
               db.session.commit()
               myNotifyBot("Payscrin Register : New registration  from " +data['phone'])
               return  {'status': "success","data": {"code":SUCCESSFUL,"message":'Activation successful'}}, 200

        return  {'status': "error","data": {"code":ACTIVATION_FAILED ,"message":'Activation  was not successful'}}, 200
        
#
#Password Check @phone,@device_id,@recovery_phone
#
class PasswordSetResource(Resource):
    #
    #Password Reset code @param {phone,@device_id}
    #
    def get(self):
        verify_code = verify_expire_code["code"]= random_gentarted(4)
        # json_data = request.get_json(force=True)
        getPhone=request.args['phone']
        getDevice_id=request.args['device_id']
        if not getPhone:
            return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided"}}, 200

        if not getDevice_id:
            return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided"}}, 200


        users = User.query.filter_by(phone=getPhone,device_id=getDevice_id).first()
        if not users:
            return  {'status': "error","data": {"code":INVALID_CODE_RESEND_DETAILS , "message":'User details does not exist' }}, 200 


        auth_user = AuthCode.query.filter(and_(AuthCode.phone==getPhone,AuthCode.auth_status == 0)).first()
        if not auth_user:
            user = AuthCode(phone=getPhone,device_id=getDevice_id,activation=verify_code,auth_status=0)
            save_changes(user)
            user = ActivitiesLog(phone=getPhone,device_id=getDevice_id,user_id=users.id,activities="Start Password Change ")
            save=save_changes(user)
            #remove verify_code on production and send code to recovery number 
            code_msg= "Your password reset code is  :" + str(verify_code)
            #sms_token(str(data['phone']),code_msg)
            SendSMSNg(str(getPhone),str(verify_code))
            return  {'status': "success","data": {"code":SUCCESSFUL,"verify_code": verify_code,"message":"successful"}}, 200
        else:
            auth_user.activation=verify_code
            db.session.commit()
            user = ActivitiesLog(phone=getPhone,device_id=getDevice_id,user_id=users.id,activities="Start Password Change ")
            save=save_changes(user)
            #remove verify_code on production and send code to recovery number
            code_msg= "Your Password Reset Code is  :" + str(verify_code)
            #sms_token(str(getPhone),code_msg)
            SendSMSNg(str(getPhone),str(verify_code))

            return  {'status': "success","data": {"code":SUCCESSFUL,"verify_code": verify_code,"message":"successful"}}, 200

    #
    #Password Reset verification @param {phone,@device_id,code, password }
    #
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided"}}, 200
       
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200 

    
        if not 'activation_code' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (activation_code) field."}}, 200 

        if not 'password' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (password) field."}}, 200 

        user = AuthCode.query.filter_by(phone=data['phone'],device_id=data['device_id'],activation=data['activation_code'],auth_status = 0).first()
        if not user:
            return  {'status': "error","data": {"code":INVALID_CODE,"message": "Verification code does not match."}}, 200 
            
        validCode= verify_expire_code.get('code')
        if not validCode:
            return  {'status': "error","data": {"code":EXPIRED_CODE,"message": "Verification code has expired."}}, 200
        else:
            user = User.query.filter_by(phone=data['phone']).first()
            user.password =hash_password(data['password'])
            user.device_id=data['device_id']
            db.session.commit()
            if user:
               auth_user = AuthCode.query.filter(and_(AuthCode.phone==data['phone'],AuthCode.device_id==data['device_id'],AuthCode.activation == data['activation_code'])).first() 
               auth_user.auth_status=1
               db.session.commit()
               return { "status": 'success', "data": {'code':PASSWORD_SUCCESSFUL,'message': 'Your assword reset was successful'}}, 200

        return  {'status': "error","data": {"code":PASSWORD_NOT_SET ,"message":'password reset  was not successful'}}, 200





        
  #
#Login @param {@phone , @device_id, @lat, @log }
#
class LoginSetResource(Resource):
    @token_required
    def get(self):
        SETTING = Settings.query.first()
        user = User.query.filter_by(id=self['user_id']).first()
        
        if user:
            token=jwt.encode({'user_id': user.id,'ref_id': user.ref_id,'phone': user.phone,'email': user.email,'password': user.password,'first_name': user.first_name,'last_name': user.last_name, 'device_id': user.device_id,'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=20)},SECRET_KEY,algorithm='HS256')
            
            return  {'status': "success","data": {"code":LOGIN_SUCCESSFUL,"message": "Login successful",'user_id': user.id,'ref_id': user.ref_id,"level": user.level,"username":user.username,"pin":user.pin ,'email': user.email ,'phone': user.phone,"first_name":user.first_name,'last_name': user.last_name, 'bank': user.bank,'bank_account': user.bank_account,'referral':SETTING.referral,'notify': user.notify,'auth2fa': user.auth2fa,'verify_me': user.verify_me,"token":token.decode('UTF-8')}}, 200

        return  {'status': "error","data": {"code":INVALID_LOGIN ,"message": "Invalid Login details"}}, 200

    

    @auth.login_required
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided." }}, 200
   
        try:
            data = user_all_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200 

        SETTING = Settings.query.first()

        user = User.query.filter_by(phone=data['phone'],device_id=data['device_id']).first()
        if user:
            userActive = ActivitiesLog(phone=user.phone,device_id=user.device_id,user_id=user.id,activities="New Login",client_name=device.client_name(),device_name=device.client_type(),os_name=device.os_name())
            save=save_changes(userActive)
            token=jwt.encode({'user_id': user.id,'ref_id': user.ref_id,'phone': user.phone,'email': user.email,'password': user.password,'first_name': user.first_name,'last_name': user.last_name, 'device_id': user.device_id,'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=20)},SECRET_KEY,algorithm='HS256')
           
            return  {'status': "success","data": {"code":LOGIN_SUCCESSFUL,"message": "Login successful", 'user_id': user.id,'ref_id': user.ref_id,"level": user.level,"username":user.username ,"pin":user.pin,'email': user.email ,'phone': user.phone,"first_name":user.first_name,'last_name': user.last_name, 'bank': user.bank,'bank_account': user.bank_account,'referral':SETTING.referral,'notify': user.notify,'auth2fa': user.auth2fa,'verify_me': user.verify_me,"token":token.decode('UTF-8')}}, 200

        return  {'status': "error","data": {"code":INVALID_LOGIN ,"message": "Invalid Login details"}}, 200

#
# Auth UserUpdate{ @phone,@device_id,@data @token } 
#
class ProfileUpdateSetResource(Resource):
    #GET BANK
    def get(self):
        banks= Banks.query.all()
        banks = banks_schema.dump(banks)
        return {'status': 'success', 'data': banks}, 200

    @token_required
    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided." }}, 200
        try:
            data = user_all_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200  

        if not 'first_name' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (first_name field.)"}}, 200
        if not 'last_name' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (last_name field.)"}}, 200
        if not 'email' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (email field.)"}}, 200

        
        user = User.query.filter_by(id=self['user_id']).first()
        if  user: 
            user.first_name =data['first_name']
            user.last_name =data['last_name']
            user.level = DASHBOARD_LEVEL
            user.email=data['email']
            db.session.commit()
            token=jwt.encode({'user_id': user.id,'phone': user.phone,'email': user.email,'password': user.password,'first_name': user.first_name,'last_name': user.last_name, 'device_id': user.device_id,'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=525600)},SECRET_KEY,algorithm='HS256') 
            return  {'status': "success","data": {"code":LOGIN_SUCCESSFUL,"message": "Profile update was successful","level": user.level,"username":user.username ,'email': user.email ,'phone': user.phone,"first_name":user.first_name,'last_name': user.last_name, 'bank': user.bank,'bank_account': user.bank_account,'notify': user.notify,'auth2fa': user.auth2fa,'verify_me': user.verify_me,"token":token.decode('UTF-8')}}, 200
        else:
            pass 
            return { "status": 'error', "data": {'code':FAILED ,'message': 'Action was not successful'}}, 200 

    @token_required
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided." }}, 200
        try:
            data = user_all_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200  

        if not 'bank' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (bank field.)"}}, 200
        if not 'bank_account' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (bank_account field.)"}}, 200
        
        user = User.query.filter_by(id=self['user_id']).first()
        if  user: 
            user.bank =data['bank']
            user.bank_account =data['bank_account']
            db.session.commit()
           
            token=jwt.encode({'user_id': user.id,'phone': user.phone,'email': user.email,'password': user.password,'first_name': user.first_name,'last_name': user.last_name, 'device_id': user.device_id,'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=525600)},SECRET_KEY,algorithm='HS256') 
            return  {'status': "success","data": {"code":LOGIN_SUCCESSFUL,"message": "Bank update was successful","level": user.level,"username":user.username ,'email': user.email ,'phone': user.phone,"first_name":user.first_name,'last_name': user.last_name, 'bank': user.bank,'bank_account': user.bank_account,'notify': user.notify,'auth2fa': user.auth2fa,'verify_me': user.verify_me,"token":token.decode('UTF-8')}}, 200
        else:
            pass 
            return { "status": 'error', "data": {'code':FAILED ,'message': 'Action was not successful'}}, 200 

#
# Google Signup Acount { @recovery_phone,@device_id} 
#
class SettingSetResource(Resource):
    @token_required
    def post(self):
            json_data = request.get_json(force=True)
            if not json_data:
                return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided." }}, 200
            try:
                data = user_all_schema.load(json_data)
            except ValidationError as err:
                return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200  

            if not 'auth2fa' in request.json:
                return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (auth2fa field.)"}}, 200
            if not 'notify' in request.json:
                return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (notify field.)"}}, 200
            if not 'verify_me' in request.json:
                return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (verify_me field.)"}}, 200
            
            user = User.query.filter_by(id=self['user_id']).first()
            if  user: 
                user.auth2fa =data['auth2fa']
                user.notify =data['notify']
                user.verify_me =data['verify_me']
                db.session.commit()
                token=jwt.encode({'user_id': user.id,'phone': user.phone,'email': user.email,'password': user.password,'first_name': user.first_name,'last_name': user.last_name, 'device_id': user.device_id,'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=525600)},SECRET_KEY,algorithm='HS256') 
                return  {'status': "success","data": {"code":LOGIN_SUCCESSFUL,"message": "Your setting has been updated successfully","level": user.level,"username":user.username ,'email': user.email ,'phone': user.phone,"first_name":user.first_name,'last_name': user.last_name, 'bank': user.bank,'bank_account': user.bank_account,'notify': user.notify,'auth2fa': user.auth2fa,'verify_me': user.verify_me,"token":token.decode('UTF-8')}}, 200
            else:
                pass 
                return { "status": 'error', "data": {'code':FAILED ,'message': 'Action was not successful'}}, 200


#
# Recovery Acount { @recovery_phone,@device_id} 
#
class RecoverySetResource(Resource):
    def put(self):
        verify_code = verify_expire_code["code"]= random_gentarted(4)
        json_data = request.get_json(force=True)
        if not json_data:
            return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided"}}, 200
       
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200 


        user = User.query.filter_by(phone=data['phone']).first()
        if not user:
            return  {'status': "error","data": {"code":INVALID_CODE_RESEND_DETAILS , "message":'User details does not exist' }}, 200 


        auth_user = AuthCode.query.filter(and_(AuthCode.phone==data['phone'],AuthCode.auth_status == 0)).first()
        if not auth_user:
            userAuth = AuthCode(phone=data['phone'],device_id=data['device_id'],activation=verify_code,auth_status=0)
            save_changes(userAuth)
            #remove verify_code on production and send code to recovery number 
            code_msg= "Your Recovery code is  :" + str(verify_code)
            sms_token(str(data['phone']),code_msg)
            return  {'status': "success","data": {"code":SUCCESSFUL,"verify_code": verify_code,"recovery_phone":user.recovery_phone}}, 200
        else:
            auth_user.activation=verify_code
            db.session.commit()
            #remove verify_code on production and send code to recovery number
            code_msg= "Your Recovery code is  :" + str(verify_code)
            sms_token(str(data['phone']),code_msg)
            return  {'status': "success","data": {"code":SUCCESSFUL,"verify_code": verify_code,"recovery_phone":user.recovery_phone}}, 200





    #
# Email { @to,subject,body} 
#
class EMailSetResource(Resource):

    @auth.login_required
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return  {'status': "error","data": {"code":REQUIRED,"message": "No input data provided"}}, 200
       
        try:
            data = msg_schema.load(json_data)
        except ValidationError as err:
            return  {'status': "error","data": {"code":REQUIRED,"message": err.messages }}, 200 


        if not 'message' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (message field.)"}}, 200

        if not 'to' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (to field.)"}}, 200

        if not 'sender' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (sender field.)"}}, 200

        if not 'subject' in request.json:
            return  {'status': "error","data": {"code":REQUIRED,"message": "Missing (subject field.)"}}, 200


        res=send_simple_message(data['to'],data['subject'],data['sender'],data['message'])

        return { "status": 'success', "data": {'code':SUCCESSFUL ,'message': res}}, 200