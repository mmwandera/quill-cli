from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, BlogPost, Comment
from sqlalchemy.sql import func
import ipdb

# Create an SQLAlchemy engine to interact with the database
engine = create_engine('sqlite:///quillcli.db')

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Load the models and the session into IPython debugger
ipdb.set_trace()


#######################################################

# QUERIES

#######################################################

# RETRIEVE ALL USERS 1:
# all_users = session.query(User).all()

# for user in all_users:
#     num_blog_posts = len(user.blog_posts)
#     num_comments = len(user.comments)

#     print(f"Username: {user.username}")
#     print(f"Number of Blog Posts: {num_blog_posts}")
#     print(f"Number of Comments: {num_comments}")
#     print("-" * 40)

# RETRIEVE ALL USERS 2 (__repr__):
# all_users = session.query(User).all()
# print(all_users)


#######################################################


# RETRIEVE ALL BLOG POSTS 1:
# all_blog_posts = session.query(BlogPost).all()

# for post in all_blog_posts:
#     print(f"Blog Post Title: {post.title}")
#     print(f"User: {post.user.username}")
#     print(f"Number of Comments: {len(post.comments)}")
#     print("-" * 40)

# RETRIEVE ALL BLOG POSTS 2 (__repr__):
# all_blog_posts = session.query(BlogPost).all()
# print(all_blog_posts)


#######################################################


# RETRIEVE ALL COMMENTS 1:
# all_comments = session.query(Comment).all()

# for comment in all_comments:
#     print(f"Comment: {comment.text[:50]}...") 
#     print(f"User: {comment.user.username}")
#     print(f"Blog Post: {comment.blog_post.title}")
#     print("-" * 40)

# RETRIEVE ALL COMMENTS 2 (__repr__):
# all_comments = session.query(Comment).all()
# print(all_comments)


#######################################################

# RETRIEVE ALL BLOG POSTS WITH THEIR ASSOCIATED USER 1:
# blog_posts_with_users = session.query(BlogPost).join(User).all()

# for post in blog_posts_with_users:
#     print(f"Blog Post Title: {post.title}")
#     print(f"User: {post.user.username}")
#     print(f"Number of Comments: {len(post.comments)}")
#     print("-" * 40)

# RETRIEVE ALL BLOG POSTS WITH THEIR ASSOCIATED USER 2 (__repr__):
# blog_posts_with_users = session.query(BlogPost).join(User).all()
# for post in blog_posts_with_users:
#     print(f"Blog Post Title: {post.title}, User: {post.user.username}")


#######################################################

# RETRIEVE ALL COMMENTS WITH THEIR ASSOCIATED USER AND BLOG POST 1:
# for comment in comments_with_user_post:
#     print(f"Username: {comment.user.username}\n"
#           f"{'-'*30}\n"
#           f"Comment: {comment.text[:100]}...\n"
#           f"{'-'*30}\n"
#           f"Blog Post: {comment.blog_post.title}\n"
#           f"{'='*60}\n")

# RETRIEVE ALL COMMENTS WITH THEIR ASSOCIATED USER AND BLOG POST 2 (__repr__):
# comments_with_user_post = session.query(Comment).join(User).join(BlogPost).all()
# for comment in comments_with_user_post:
#     print(f"Comment: {comment.text}, User: {comment.user.username}, Blog Post: {comment.blog_post.title}")


