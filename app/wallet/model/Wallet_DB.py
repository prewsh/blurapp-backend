#
#@KEVIN DataBase Module
#
from flask import Flask
from app import  db,ma
from marshmallow import Schema, fields, pre_load, validate,ValidationError
from datetime import datetime



class Deposit(db.Model):
    __tablename__ = 'deposit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    deposit_ref = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.String(200), nullable=False)
    charges = db.Column(db.String(200), nullable=False)
    pre_amount = db.Column(db.String(200), nullable=False)
    deposit_token = db.Column(db.Text, nullable=False)
    deposit_status = db.Column(db.Integer, nullable=True)
    ref_id = db.Column(db.Integer, nullable=True)
    deposit_link = db.Column(db.Text, nullable=True)
    per_cent= db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)



   


     


