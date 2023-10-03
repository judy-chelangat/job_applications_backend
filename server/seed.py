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
