from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

engine = create_engine('sqlite:///quillcli.db', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(60), nullable=False)  # Store hashed passwords

    # Relationship to BlogPost
    blog_posts = relationship('BlogPost', back_populates='user')

    # Relationship to Comment
    comments = relationship('Comment', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to User
    user = relationship('User', back_populates='blog_posts')

    # Relationship to Comment
    comments = relationship('Comment', back_populates='blog_post')

    def __repr__(self):
        return f"<BlogPost(id={self.id}, title={self.title}, user_id={self.user_id})>"

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    blog_post_id = Column(Integer, ForeignKey('blog_posts.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to User
    user = relationship('User', back_populates='comments')

    # Relationship to BlogPost
    blog_post = relationship('BlogPost', back_populates='comments')

    def __repr__(self):
        return f"<Comment(id={self.id}, text={self.text}, user_id={self.user_id}, blog_post_id={self.blog_post_id})>"