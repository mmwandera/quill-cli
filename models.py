from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from passlib.hash import bcrypt

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

    @classmethod
    def create_user(cls, session, username, email, password):
        new_user = cls(username=username, email=email, password=password)
        session.add(new_user)
        session.commit()
        return new_user

    @classmethod
    def authenticate(cls, session, username, password):
        user = session.query(cls).filter_by(username=username).first()
        if user and bcrypt.verify(password, user.password):
            return user
        return None
    
    def get_user_blog_posts(self, session):
        return session.query(BlogPost).filter_by(user_id=self.id).all()

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

    @classmethod
    def create_blog_post(cls, session, title, content, user_id):
        new_blog_post = cls(title=title, content=content, user_id=user_id)
        session.add(new_blog_post)
        session.commit()
        return new_blog_post
    
    @classmethod
    def get_all_blog_posts(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def get_blog_posts_by_user(cls, session, user_id):
        return session.query(cls).filter_by(user_id=user_id).all()

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

    @classmethod
    def create_comment(cls, session, text, user_id, blog_post_id):
        new_comment = cls(text=text, user_id=user_id, blog_post_id=blog_post_id)
        session.add(new_comment)
        session.commit()
        return new_comment
    
    @classmethod
    def get_comments_for_blog_post(cls, session, blog_post_id):
        return session.query(cls).filter_by(blog_post_id=blog_post_id).all()

    def __repr__(self):
        return f"<Comment(id={self.id}, text={self.text}, user_id={self.user_id}, blog_post_id={self.blog_post_id})>"