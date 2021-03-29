#
#@KEVIN DataBase Module
#
from flask import Flask
from app import  db,ma
from marshmallow import Schema, fields, pre_load, validate,ValidationError
from datetime import datetime



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    ref_id = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=True)
    first_name = db.Column(db.String(200), nullable=True)
    last_name = db.Column(db.String(200), nullable=True)
    password = db.Column(db.Text, nullable=True)
    pin = db.Column(db.Text, nullable=True)
    dob = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(200),  nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=True)
    uid = db.Column(db.Text, nullable=True)
    device_id = db.Column(db.Text, nullable=False)
    country = db.Column(db.String(100), nullable=True)
    photo = db.Column(db.String(100), nullable=True)
    level = db.Column(db.Integer, nullable=True)
    activation = db.Column(db.Integer, nullable=True)
    recovery_phone = db.Column(db.String(20), nullable=True)
    bank = db.Column(db.String(200), nullable=False)
    bank_account = db.Column(db.String(200), nullable=True)
    status= db.Column(db.Integer,nullable=True)
    notify = db.Column(db.Integer, nullable=True)
    auth2fa = db.Column(db.Integer, nullable=True)
    verify_me = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    
    
class AuthCode(db.Model):
    __tablename__ = 'auth_codes'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    device_id = db.Column(db.Text, nullable=False)
    activation = db.Column(db.Integer, nullable=True)
    auth_status= db.Column(db.Integer,nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

class Banks(db.Model):
    __tablename__ = 'banks'
    id = db.Column(db.Integer, primary_key=True)
    b_code = db.Column(db.Integer, nullable=False)
    bank_name = db.Column(db.String(200), nullable=False)

class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    dollar_rate = db.Column(db.Integer, nullable=True)
    sell_btc = db.Column(db.Integer, nullable=True)
    sell_eth = db.Column(db.Integer, nullable=True)
    btc_rate = db.Column(db.Integer, nullable=True)
    eth_rate = db.Column(db.Integer, nullable=True)
    eth_to_dollar = db.Column(db.String(100), nullable=True)
    debit_id = db.Column(db.Integer, nullable=True)
    credit_id = db.Column(db.Integer, nullable=True)
    referral = db.Column(db.Integer, nullable=True)
    btc_limit = db.Column(db.Integer, nullable=True)
    local_limit = db.Column(db.Integer, nullable=True)
    eth_limit = db.Column(db.Integer, nullable=True)


class ActivitiesLog(db.Model):
    __tablename__ = 'activitieslogs'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    device_id = db.Column(db.Text, nullable=False)
    activities = db.Column(db.Text, nullable=False)
    device_name = db.Column(db.String(100), nullable=True)
    os_name = db.Column(db.String(100), nullable=True)
    client_name = db.Column(db.String(100), nullable=True)
    activities_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('activitieslogs', lazy='dynamic' ))


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")
    


class UserSchema(ma.Schema):
    id = fields.Integer()
    ref_id= fields.Integer()
    phone = fields.String(required=True,validate=must_not_be_blank)
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    password = fields.String()
    dob=fields.String()
    gender=fields.String()
    email=fields.String()
    uid = fields.String()
    pin = fields.String()
    device_id = fields.String(required=True,validate=must_not_be_blank)
    photo = fields.String()
    country=fields.String()
    activation_code = fields.String()
    recovery_phone = fields.String()
    status = fields.String()
    biometric_id =fields.String()
    notify = fields.Integer()
    auth2fa = fields.Integer()
    verify_me = fields.Integer()


class AuthCodeSchema(ma.Schema):
    id = fields.Integer()
    ref_id= fields.Integer()
    phone = fields.String(required=True,validate=must_not_be_blank)
    device_id = fields.String(required=True,validate=must_not_be_blank)
    password = fields.String()
    new_phone = fields.Integer()
    activation_code  = fields.Integer()
    auth_status= fields.Integer()


class UserAllSchema(ma.Schema):
    id = fields.Integer()
    ref_id= fields.Integer()
    phone = fields.String()
    username = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    password = fields.String()
    dob=fields.String()
    gender=fields.String()
    email=fields.String()
    uid = fields.String()
    pin = fields.String()
    device_id = fields.String()
    country=fields.String()
    photo = fields.String()
    activation_code = fields.String()
    recovery_phone = fields.String()
    status = fields.String()
    bank = fields.String()
    bank_account = fields.String()
    notify = fields.Integer()
    auth2fa = fields.Integer()
    verify_me = fields.Integer()

class BanksSchema(ma.Schema):
    id = fields.Integer()
    b_code = fields.String()
    bank_name =fields.String()

class SettingSchema(ma.Schema):
    id = fields.Integer()
    dollar_rate = fields.Integer()
    sell_btc= fields.Integer()
    sell_eth= fields.Integer()
    btc_rate = fields.Integer()
    eth_rate = fields.Integer()
    eth_to_dollar = fields.Integer()
    debit_id = fields.Integer()
    credit_id = fields.String()
    referral = fields.String()
    btc_limit = fields.Integer()
    local_limit = fields.Integer()
    eth_limit = fields.Integer()
  
   
class MessageAllSchemaPost(ma.Schema):
    title = fields.String()
    message = fields.String()
    to = fields.String()
    subject = fields.String()
    sender = fields.String()
  
  

     


