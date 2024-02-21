import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, BlogPost, Comment
from prettytable import PrettyTable
from passlib.hash import bcrypt
import getpass
from colorama import init, Fore, Style

LOGO = """
 ██████╗ ██╗   ██╗██╗██╗     ██╗     
██╔═══██╗██║   ██║██║██║     ██║     
██║   ██║██║   ██║██║██║     ██║     
██║▄▄ ██║██║   ██║██║██║     ██║     
╚██████╔╝╚██████╔╝██║███████╗███████╗
 ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝╚══════╝
                                     
 ██████╗██╗     ██╗                  
██╔════╝██║     ██║                  
██║     ██║     ██║                  
██║     ██║     ██║                  
╚██████╗███████╗██║                  
 ╚═════╝╚══════╝╚═╝                  
 """

def display_logo_and_menu():
    print(HEADER_COLOR + LOGO + RESET_STYLE)

# Initialize colorama for text styling
init(autoreset=True)

# Styling constants
HEADER_COLOR = Fore.CYAN + Style.BRIGHT
SUCCESS_COLOR = Fore.GREEN
ERROR_COLOR = Fore.RED
PROMPT_COLOR = Fore.YELLOW
RESET_STYLE = Style.RESET_ALL

# Create an SQLAlchemy engine to interact with the database
engine = create_engine('sqlite:///quillcli.db')

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def get_secure_input(prompt):
    return getpass.getpass(PROMPT_COLOR + prompt + RESET_STYLE)

def sign_up():
    print(HEADER_COLOR + "Sign Up")
    username = input(PROMPT_COLOR + "Enter username: ")
    email = input("Enter email: ")
    password = get_secure_input("Enter password: ")
    hashed_password = bcrypt.hash(password)

    new_user = User.create_user(session, username, email, hashed_password)
    print(SUCCESS_COLOR + "User signed up successfully.")

def sign_in():
    print(HEADER_COLOR + "Sign In")
    username = input(PROMPT_COLOR + "Enter username: ")
    password = get_secure_input("Enter password: ")

    user = User.authenticate(session, username, password)
    if user:
        print(SUCCESS_COLOR + f"Welcome, {user.username}!")
        return user
    else:
        print(ERROR_COLOR + "Invalid username or password.")
        return None

def view_all_blog_posts():
    print(HEADER_COLOR + "View All Blog Posts")
    all_blog_posts = session.query(BlogPost).all()
    
    table = PrettyTable()
    table.field_names = ["ID", "Title", "User", "Created At"]
    for post in all_blog_posts:
        table.add_row([post.id, post.title, post.user.username, post.created_at])
    print(table)

    blog_post_id = input(PROMPT_COLOR + "Enter blog post ID to view details (or 0 to go back): ")
    try:
        blog_post_id = int(blog_post_id)
    except ValueError:
        print(ERROR_COLOR + "Invalid blog post ID.")
        return

    if blog_post_id == 0:
        return

    blog_post = session.query(BlogPost).filter_by(id=blog_post_id).first()
    if blog_post:
        view_blog_post_details(blog_post)

def view_blog_post_details(blog_post):
    print(HEADER_COLOR + "View Blog Post Details")
    print(f"Title: {blog_post.title}")
    print(f"Content: {blog_post.content}")
    print(f"Author: {blog_post.user.username}")
    print(f"Created At: {blog_post.created_at}")

    while True:
        print("\nOptions:")
        print("1. View Comments")
        print("2. Add Comment")
        print("0. Back")

        choice = input(PROMPT_COLOR + "Enter your choice: ")

        if choice == "1":
            view_comments(blog_post)
        elif choice == "2":
            add_comment(blog_post.user, blog_post)
        elif choice == "0":
            break
        else:
            print(ERROR_COLOR + "Invalid choice. Please enter a number from the menu.")

def view_comments(blog_post):
    print(HEADER_COLOR + "View Comments")
    comments = Comment.get_comments_for_blog_post(session, blog_post.id)
    
    table = PrettyTable()
    table.field_names = ["ID", "Text", "User", "Created At"]
    for comment in comments:
        table.add_row([comment.id, comment.text, comment.user.username, comment.created_at])
    print(table)

def add_comment(user, blog_post):
    print(HEADER_COLOR + "Add Comment")
    text = input(PROMPT_COLOR + "Enter your comment: ")
    
    new_comment = Comment.create_comment(session, text, user.id, blog_post.id)
    print(SUCCESS_COLOR + "Comment added successfully.")

def add_blog_post(user):
    print(HEADER_COLOR + "Add Blog Post")
    title = input(PROMPT_COLOR + "Enter blog post title: ")
    content = input("Enter blog post content: ")

    new_blog_post = BlogPost.create_blog_post(session, title, content, user.id)
    print(SUCCESS_COLOR + "Blog post added successfully.")

def delete_blog_post(user):
    print(HEADER_COLOR + "Delete Blog Post")
    user_blog_posts = BlogPost.get_blog_posts_by_user(session, user.id)

    if not user_blog_posts:
        print("You have no blog posts to delete.")
        return

    table = PrettyTable()
    table.field_names = ["ID", "Title", "Created At"]
    for post in user_blog_posts:
        table.add_row([post.id, post.title, post.created_at])
    print(table)

    blog_post_id = input(PROMPT_COLOR + "Enter blog post ID to delete (or 0 to go back): ")
    try:
        blog_post_id = int(blog_post_id)
    except ValueError:
        print(ERROR_COLOR + "Invalid blog post ID.")
        return

    if blog_post_id == 0:
        return

    blog_post = session.query(BlogPost).filter_by(id=blog_post_id, user_id=user.id).first()
    if blog_post:
        session.delete(blog_post)
        session.commit()
        print(SUCCESS_COLOR + "Blog post deleted successfully.")
    else:
        print(ERROR_COLOR + "Invalid blog post ID or you do not have permission to delete this post.")

def main():
    user = None

    while not user:

        display_logo_and_menu()

        print("\nMenu:")
        print("1. Sign Up")
        print("2. Sign In")
        print("0. Exit")

        choice = input(PROMPT_COLOR + "Enter your choice: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            user = sign_in()
        elif choice == "0":
            exit()
        else:
            print(ERROR_COLOR + "Invalid choice. Please enter a number from the menu.")

    while True:
        print("\nMenu:")
        print("3. View All Blog Posts")
        print("4. View Your Blog Posts")
        print("5. Add Blog Post")
        print("6. Delete Blog Post")
        print("0. Exit")

        choice = input(PROMPT_COLOR + "Enter your choice: ")

        if choice == "3":
            view_all_blog_posts()
        elif choice == "4":
            user_blog_posts = BlogPost.get_blog_posts_by_user(session, user.id)

            if not user_blog_posts:
                print("You have no blog posts.")
            else:
                table = PrettyTable()
                table.field_names = ["ID", "Title", "Created At"]
                for post in user_blog_posts:
                    table.add_row([post.id, post.title, post.created_at])
                print(table)

                blog_post_id = input(PROMPT_COLOR + "Enter blog post ID to view details (or 0 to go back): ")
                try:
                    blog_post_id = int(blog_post_id)
                except ValueError:
                    print(ERROR_COLOR + "Invalid blog post ID.")
                    continue

                if blog_post_id != 0:
                    blog_post = session.query(BlogPost).filter_by(id=blog_post_id, user_id=user.id).first()
                    if blog_post:
                        view_blog_post_details(blog_post)
                    else:
                        print(ERROR_COLOR + "Invalid blog post ID or you do not have permission to view this post")
        elif choice == "5":
            add_blog_post(user)
        elif choice == "6":
            delete_blog_post(user)
        elif choice == "0":
            break
        else:
            print(ERROR_COLOR + "Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    main()
