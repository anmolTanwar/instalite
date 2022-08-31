from datetime import datetime
from sqlalchemy import Column, Integer, String,ForeignKey
from instalite.db import Base,relationship
from werkzeug.security import generate_password_hash,check_password_hash



class Profile(Base):
    __tablename__ = 'profiles'
    profile_id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(100),nullable=False)
    email = Column(String(100),nullable=False,unique=True)
    password = Column(String(100),nullable=False)
    phone_no = Column(String(100))
    about_me =Column(String(200))
    profile_pic =Column(String(200))
    profile_date = Column(String)
    profile_time = Column(String)
    posts = relationship('Post',backref='profiles',cascade='all, delete-orphan')

    def __init__(self,username,email,password):
        x = datetime.now()
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.profile_date = x.strftime('%d %b %y')
        self.profile_time = x.strftime('%I:%M %p')

    def verify_password(self,pwd):
        return check_password_hash(self.password,pwd)

    def __repr__(self):
        return f'<Profile {self.email}>'


class Post(Base):

    __tablename__ = 'posts'

    post_id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(100),nullable=False)
    desc = Column(String(200),nullable=False)
    post_pic = Column(String(200))
    post_date = Column(String)
    post_time = Column(String)
    uploaded_by = Column(String)
    profile_id = Column(ForeignKey('profiles.profile_id',ondelete='CASCADE'))

    def __init__(self,title,desc,post_pic,profile_id,uploaded_by):
        x = datetime.now()
        self.title= title
        self.desc = desc
        self.post_pic = post_pic
        self.post_date = x.strftime('%d %b %y')
        self.post_time = x.strftime('%I:%M %p')
        self.uploaded_by = uploaded_by
        self.profile_id = profile_id

    def __repr__(self):
        return f'<Post {self.post_id}>'


    


