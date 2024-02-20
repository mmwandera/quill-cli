from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Base, User, BlogPost, Comment
import random
import os

# Create an SQLAlchemy engine to interact with the database
engine = create_engine('sqlite:///quillcli.db')

# Check if the database file exists
if not os.path.exists('quillcli.db'):
    print("Database file 'quillcli.db' does not exist. Please create it.")
    exit()

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a Faker instance
fake = Faker()

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Delete existing data
session.query(Comment).delete()
session.query(BlogPost).delete()
session.query(User).delete()
session.commit()

# Create fake users
def create_fake_users(num_users=5):
    for _ in range(num_users):
        while True:
            username = fake.user_name()
            email = fake.email()
            
            # Check if username and email are unique
            if not session.query(User).filter_by(username=username).first() and not session.query(User).filter_by(email=email).first():
                break

        user = User(
            username=username,
            email=email,
            password=fake.password()
        )
        try:
            session.add(user)
            session.commit()
        except IntegrityError:
            session.rollback()
            continue

# Create fake blog posts
def create_fake_blog_posts(num_posts=5, num_comments_per_post=3):
    users = session.query(User).all()

    for _ in range(num_posts):
        post = BlogPost(
            title=fake.sentence(),
            content=fake.text(),
            user=random.choice(users)
        )
        try:
            session.add(post)
            session.commit()

            # Create fake comments for each post
            for _ in range(num_comments_per_post):
                comment = Comment(
                    text=fake.text(),
                    user=random.choice(users),
                    blog_post=post
                )
                session.add(comment)
            session.commit()

        except IntegrityError:
            session.rollback()
            continue

if __name__ == "__main__":
    create_fake_users()
    create_fake_blog_posts()
