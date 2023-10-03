<<<<<<< HEAD
from app import app, db
from models import User, JobListing, JobApplication
from datetime import datetime


# Function to seed data
def seed_data():
    with app.app_context():
        # Create sample users
        user1 = User(username='user1', email='user1@example.com', password='password1')
        user2 = User(username='user2', email='user2@example.com', password='password2')

        # Create sample job listings
        job1 = JobListing(
            title='Job 1',
            description='Description for Job 1',
            location='Location 1',
            company_name='Company 1',
            posted_at=datetime.utcnow() 
        )
        job2 = JobListing(
            title='Job 2',
            description='Description for Job 2',
            location='Location 2',
            company_name='Company 2',
            posted_at=datetime.utcnow() 
        )

        # Create sample job applications
        application1 = JobApplication(
            cover_letter='Cover letter for Application 1',
            resume_url='resume_url_1',
            user=user1,
            job=job1,
            applied_at = datetime.utcnow() 
        )
        application2 = JobApplication(
            cover_letter='Cover letter for Application 2',
            resume_url='resume_url_2',
            user=user2,
            job=job2,
            applied_at = datetime.utcnow() 
        )

        user1.jobs.append(job1)
        user2.jobs.append(job2)

        # Add the sample data to the database
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(job1)
        db.session.add(job2)
        db.session.add(application1)
        db.session.add(application2)

        # Commit the changes to the database
        db.session.commit()

if __name__ == '__main__':
    seed_data()
=======
from server.app import app, db
from server.models import User, JobListing, JobApplication

def create_users():
    user1 = User(username='user1', email='user1@example.com', password='password1')
    user2 = User(username='user2', email='user2@example.com', password='password2')
    db.session.add(user1)
    db.session.add(user2)

def create_job_listings():
    job1 = JobListing(title='Job 1', description='Description for Job 1', location='Location 1', company_name='Company A', posted_at='2023-10-01')
    job2 = JobListing(title='Job 2', description='Description for Job 2', location='Location 2', company_name='Company B', posted_at='2023-10-02')
    db.session.add(job1)
    db.session.add(job2)

def create_job_applications():
    app1 = JobApplication(job_id=1, applicant_name='Applicant 1')
    app2 = JobApplication(job_id=2, applicant_name='Applicant 2')
    db.session.add(app1)
    db.session.add(app2)

if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
        create_users()
        create_job_listings()
        create_job_applications()
        db.session.commit()
>>>>>>> e806444177c79986960926c5c021fd555d6e52b3
