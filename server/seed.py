from app import app, db
from models import User, JobListing, JobApplication
from datetime import datetime
from faker import Faker

fake = Faker()

# List of tech-related job titles and descriptions
tech_job_data = [
   {
        'title': 'Senior Software Engineer',
        'description': 'We are looking for an experienced Senior Software Engineer to join our team. In this role, you will be responsible for designing and developing software solutions that meet our clients\' needs. You will work closely with cross-functional teams to deliver high-quality software products.',
        'image_url': 'https://pngimg.com/uploads/meta/meta_PNG12.png'
    },
    {
        'title': 'UI/UX Designer',
        'description': 'As a UI/UX Designer, you will be responsible for creating user-friendly and visually appealing interfaces for our web and mobile applications. You will collaborate with our development team to ensure that our products provide the best possible user experience.',
        'image_url': 'https://freepngimg.com/thumb/google/66904-logo-now-google-plus-home-free-png-hq.png'
    },
    {
        'title': 'Data Scientist',
        'description': 'We are seeking a Data Scientist with a strong background in machine learning and data analysis. In this role, you will work on complex data projects, develop predictive models, and provide data-driven insights to support business decisions.',
        'image_url': 'https://png.pngtree.com/element_our/png/20181011/twitter-social-media-icon-design-template-vector-png_126985.jpg'
    },
    {
        'title': 'Product Manager',
        'description': 'Join our team as a Product Manager and lead the development and launch of innovative products. You will define product strategies, prioritize features, and collaborate with cross-functional teams to deliver successful products to market.',
        'image_url': 'https://pngimg.com/uploads/meta/meta_PNG12.png'
    },
    {
        'title': 'DevOps Engineer',
        'description': 'As a DevOps Engineer, you will be responsible for automating and streamlining our development and operations processes. You will work on maintaining and improving our deployment pipelines, infrastructure, and monitoring systems.',
        'image_url': 'https://freepngimg.com/thumb/google/66904-logo-now-google-plus-home-free-png-hq.png'
    },
]

# Function to seed data
def seed_data():
    with app.app_context():
        User.query.delete()
        JobListing.query.delete()
        JobApplication.query.delete()
        # Create sample users
        users = []
        for _ in range(5):
            username = fake.user_name()
            email = fake.email()
            password = 'password'  # You can use a common password for all users for simplicity
            user = User(username=username, email=email, password=password)
            users.append(user)
            db.session.add(user)

        # Create sample job listings with realistic titles and descriptions
        tech_companies = ['Meta', 'Google', 'Twitter']
        job_listings = []
        for company in tech_companies:
            for job_data in tech_job_data:
                title = job_data['title']
                description = job_data['description']
                image_url = job_data['image_url']
                location = fake.address()
                company_name = company
                posted_at = datetime.utcnow()
                job = JobListing(title=title, description=description, location=location, company_name=company_name, posted_at=posted_at,company_image=image_url)
                job_listings.append(job)
                db.session.add(job)

        # Create sample job applications
        for user in users:
            for i in range(1, 6):
                cover_letter = fake.text()
                resume_url = fake.url()
                job = job_listings[i - 1]  # Assign each user to a specific job
                applied_at = datetime.utcnow()
                application = JobApplication(cover_letter=cover_letter, resume_url=resume_url, user=user, job=job, applied_at=applied_at)
                db.session.add(application)

                # Populate the user_joblisting_association table
                user.jobs.append(job)

        # Commit the changes to the database
        db.session.commit()

if __name__ == '__main__':
    seed_data()
    print("Data seeding completed.")


