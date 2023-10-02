from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

user_joblisting_association = db.Table('user_joblisting_association',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('jobs_id', db.Integer, db.ForeignKey('job_lists.id'))
    )


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phonenumber = db.Column(db.Integer())

    applications = db.relationship('JobApplication', backref='user')
    jobs = db.relationship('JobListing', secondary=user_joblisting_association, back_populates='applicants')
    added_jobs = db.relationship('AddJob', backref='user')


class JobListing(db.Model, SerializerMixin):
    __tablename__ = "job_lists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False)

    applications = db.relationship('JobApplication', backref='job')
    applicants = db.relationship('User', secondary=user_joblisting_association, back_populates='jobs')


class JobApplication(db.Model, SerializerMixin):
    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)
    cover_letter = db.Column(db.Text, nullable=False)
    resume_url = db.Column(db.String(255), nullable=False)
    applied_at = db.Column(db.DateTime, nullable=False)

    job_listing_id = db.Column(db.Integer, db.ForeignKey('job_lists.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
 

class AddJob(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))