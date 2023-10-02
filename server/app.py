#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,render_template,request
from flask_migrate import Migrate
from flask_restful import Api,Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired,Email,Length


from models import db, JobApplication,JobListing,User

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact =False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4,max=80)])
    email = StringField('Email', validators=[DataRequired(),Email(),Length(max=120)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=3)])
    
class UserRegistrationResource(Resource):
    def post(self):
        data=request.get_json()
        form = RegistrationForm(data=data)
        
        if form.validate():
            username = form.username.data
            email=form.email.data
            password = form.password.data

            if User.query.filter_by(username=username).first is not None:
                return {'message':'Email already exists'},400
            
            new_user = User(username=username,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(indentity=new_user.id)

            return {
                'message':"user registered succesfully",
                'access_token': access_token
            },201
        else:
            return {'message':'validation errors','errors':form.errors},400

api.add_resource(UserRegistrationResource,'/register')

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
    
class JobListResource(Resource):
    def get(self):
        joblists = [{'id':job.id,'title':job.title,'description':job.description,'location':job.location,'company_name':job.company_name,'datetime':job.posted_at}  for job in JobListing.query.all()]
        response = make_response(jsonify(joblists),200)
        return response

    def post(self):
        data = request.get_json()
        new_job = JobListing(title=data['title'],description=data['description'],location=data['location'],company_name=data['company_name'],posted_at=data['posted_at'])
        db.session.add(new_job)
        db.session.commit()
        response = make_response(new_job.to_dict(),201)
        return response


api.add_resource(JobListResource,'/Available jobs')

class JobListByIdResource(Resource):
    def get(self,id):
        job = JobListing.query.filter_by(JobListing.id == id).first()
        if not job:
            job_dict={'error':'job not found'}
            response = make_response(jsonify(job_dict),404)
            return response
        response = make_response(jsonify(job),200)
        return response
    
api.add_resource(JobListByIdResource,'/Search Job/<int:id>')

class JobApplication(Resource):
    def get(self):
        pass
    def post(self):
        pass
    

api.add_resource(JobApplication,'/job applications')

class JobApplicationById(Resource):
    def delete(self,id):
        pass
    def patch(self,id):
        pass

api.add_resource(JobApplicationById,'/job application/<int:id>')

    
    
