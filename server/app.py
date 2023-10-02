#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,render_template,request
from flask_migrate import Migrate
from flask_restful import Api,Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_wtf import FlaskForm
from 
from models import db, JobApplication,JobListing,User

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact =False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class RegistrationForm(FlaskForm):
    username = 



