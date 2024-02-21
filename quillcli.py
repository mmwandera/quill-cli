import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, BlogPost, Comment
from prettytable import PrettyTable
from passlib.hash import bcrypt
import getpass  # Import getpass for secure password input

# Create an SQLAlchemy engine to interact with the database
engine = create_engine('sqlite:///quillcli.db')

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def get_secure_input(prompt):
    return getpass.getpass(prompt)

def sign_up():
    print("Sign Up")
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = get_secure_input("Enter password: ")
    hashed_password = bcrypt.hash(password)

    new_user = User.create_user(session, username, email, hashed_password)
    print("User signed up successfully.")

def sign_in():
    print("Sign In")
    username = input("Enter username: ")
    password = get_secure_input("Enter password: ")

    user = User.authenticate(session, username, password)
    if user:
        print(f"Welcome, {user.username}!")
        return user
    else:
        print("Invalid username or password.")
        return None

def main():
    user = None

    while not user:
        print("\nMenu:")
        print("1. Sign Up")
        print("2. Sign In")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            user = sign_in()
        elif choice == "0":
            exit()
        else:
            print("Invalid choice. Please enter a number from the menu.")

    while True:
        print("\nMenu:")
        print("3. View Blog Posts")
        print("4. Add Blog Post")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "3":
            view_blog_posts(user)
        elif choice == "4":
            add_blog_post(user)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")

def view_blog_posts(user):
    print("View Blog Posts")
    blog_posts = BlogPost.get_all_blog_posts(session)
    
    table = PrettyTable()
    table.field_names = ["ID", "Title", "User"]
    for post in blog_posts:
        table.add_row([post.id, post.title, post.user.username])
    print(table)

    blog_post_id = input("Enter blog post ID to view details (or 0 to go back): ")
    try:
        blog_post_id = int(blog_post_id)
    except ValueError:
        print("Invalid blog post ID.")
        return

    if blog_post_id == 0:
        return

    blog_post = session.query(BlogPost).filter_by(id=blog_post_id).first()
    if blog_post:
        view_blog_post_details(user, blog_post)

def view_blog_post_details(user, blog_post):
    print("View Blog Post Details")
    print(f"Title: {blog_post.title}")
    print(f"Content: {blog_post.content}")
    print(f"Author: {blog_post.user.username}")
    print(f"Created At: {blog_post.created_at}")

    # Add this line to print the length of the content
    print(f"Content Length: {len(blog_post.content)}")
    
    while True:
        print("\nOptions:")
        print("1. View Comments")
        print("2. Add Comment")
        print("0. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_comments(blog_post)
        elif choice == "2":
            add_comment(user, blog_post)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")

def view_comments(blog_post):
    print("View Comments")
    comments = Comment.get_comments_for_blog_post(session, blog_post.id)
    
    table = PrettyTable()
    table.field_names = ["ID", "Text", "User", "Created At"]
    for comment in comments:
        table.add_row([comment.id, comment.text, comment.user.username, comment.created_at])
    print(table)

def add_comment(user, blog_post):
    print("Add Comment")
    text = input("Enter your comment: ")
    
    new_comment = Comment.create_comment(session, text, user.id, blog_post.id)
    print("Comment added successfully.")

def add_blog_post(user):
    print("Add Blog Post")
    title = input("Enter blog post title: ")
    content = input("Enter blog post content: ")

    new_blog_post = BlogPost.create_blog_post(session, title, content, user.id)
    print("Blog post added successfully.")

if __name__ == "__main__":
    main()
