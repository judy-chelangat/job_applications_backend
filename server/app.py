#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,render_template,request
from flask_migrate import Migrate
from flask_restful import Api,Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,Email,Length
from datetime import datetime
from flask_cors import CORS


from models import db, JobApplication,JobListing,User

app= Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

app.config['WTF_CSRF_ENABLED'] = False

jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://my_name:obBw505hbh8jIfdSwuB3rkwXW8gMbrev@dpg-ckcjhqciibqc73cd0b7g-a.oregon-postgres.render.com/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact =False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4,max=80)])
    email = StringField('Email', validators=[DataRequired(),Email(),Length(max=120)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=3)])
    
class UserRegistrationResource(Resource):
    def post(self):
        data = request.get_json()
        form = RegistrationForm(data=data)
        
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            if User.query.filter(User.username == username).first() is not None:
                return {'message': 'Username already exists'}, 400
            
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity=new_user.id)

            return {
                'message': "User registered successfully",
                'access_token': access_token
            }, 201
        else:
            return {'message': 'Validation errors', 'errors': form.errors}, 400

api.add_resource(UserRegistrationResource, '/register')


class UserLogInResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return{'message':'username and password required'},400
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token= create_access_token(indentity=user.id)
            return {'access token':access_token},200
        else:
            return {'message':'Invalid credentials'},401
        
api.add_resource(UserLogInResource,'/log in')

class UserResource(Resource):
    @jwt_required()
    def get(self):
        users = [{'id':user.id,'username':user.username,'email':user.email} for user in User.query.all()]
        response = make_response(jsonify(users),200)
        return response
    
api.add_resource(UserResource,'/user')

class UserById(Resource):
    @jwt_required()
    def get(self,id):
        user = User.query.filter(User.id == id).first()
        if not user:
            user_dict={'error':'job not found'}
            response = make_response(jsonify(user_dict),404)
            return response
        response = make_response(user.serialize(),200)
        return response

api.add_resource(UserById, '/user/<int:id>')


    
class JobListResource(Resource):
    @jwt_required()
    def get(self):
        joblists = [{'id':job.id,'title':job.title,'description':job.description,'location':job.location,'company_name':job.company_name,'datetime':job.posted_at}  for job in JobListing.query.all()]
        response = make_response(jsonify(joblists),200)
        return response
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        new_job = JobListing(title=data['title'],description=data['description'],location=data['location'],company_name=data['company_name'])
        db.session.add(new_job)
        db.session.commit()
        response = make_response(new_job.to_dict(),201)
        return response


api.add_resource(JobListResource,'/Available jobs')

class JobListByIdResource(Resource):
    @jwt_required()
    def get(self, id):  # Changed parameter name to 'id'
        job = JobListing.query.filter(JobListing.id == id).first()
        if not job:
            job_dict = {'error': 'Job not found'}
            response = make_response(jsonify(job_dict), 404)
            return response
        response = make_response(jsonify(job.serialize()), 200)
        return response

api.add_resource(JobListByIdResource, '/SearchJob/<int:id>')  # Updated endpoint to '/SearchJob/<int:id>'


class JobApplicationResource(Resource):
    @jwt_required()
    def get(self):
        job_applications = [{"id":application.id,"cover_letter":application.cover_letter,"resume_url":application.resume_url,"applied_at":application.applied_at} for application in JobApplication.query.all()]
        response = make_response(jsonify(job_applications), 200)
        return response
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        application = JobApplication(cover_letter=data['cover_letter'],resume_url=data['resume_url'],applied_at=datetime.utcnow(),user_id=data['user_id'],job_listing_id=data['job_listing_id'])
        db.session.add(application)
        db.session.commit()

        response = make_response(application.to_dict(), 201)
        return response

api.add_resource(JobApplicationResource, '/job-applications')


class JobApplicationByIdResource(Resource):
    
    @jwt_required()
    def get(self, id):
        application = JobApplication.query.filter(JobApplication.id == id).first()
        if not application:
            return {'error': 'Job application not found'}, 404
        response = make_response(application.serialize(), 200)
        return response
    
    @jwt_required()
    def delete(self, id):
        application = JobApplication.query.get(id)
        if not application:
            return {'error': 'Job application not found'}, 404
        db.session.delete(application)
        db.session.commit()
        return {'message': 'Job application deleted'}, 200
    
    @jwt_required()
    def patch(self, id):
        application = JobApplication.query.get(id)
        if not application:
            return {'error': 'Job application not found'}, 404
        data = request.get_json()
        application.resume_url = data["resume_url"]
        db.session.commit()
        response = make_response(application.serialize(),200)
        return response
        

api.add_resource(JobApplicationByIdResource, '/job-application/<int:id>')



    
    
