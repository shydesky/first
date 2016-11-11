from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import and_
from database import Base, db_session

import time

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) 
    email = Column(String(120), unique=True)
    name = Column(String(50))
    passwd = Column(String(120))
    phone = Column(String(11))
    clientKey = Column(String(120))
    userip = Column(String(20))
    usertype = Column(String(2))
    def __init__(self, name=None, email=None, passwd=None, phone=None, clientKey=None, userip=None, usertype=0):
        self.name = name
        self.email = email
        self.passwd = passwd
        self.phone = phone
        self.clientKey = clientKey
        self.userip = userip
        self.usertype = usertype

    def __repr__(self):
        return '<User %r>' % (self.name)

class VerifyCode(Base):
    __tablename__ = 'verifycode'
    id = Column(Integer, primary_key=True) 
    userid = Column(Integer)
    code = Column(String(50))
    create_time = Column(DateTime, default=time.time())
    
    def __init__(self, userid=0, code='000000', create_time=datetime.datetime.now):
        self.userid = userid
        self.code = code
        self.create_time = create_time

    def __repr__(self):
        return '<VerifyCode %r>' % (self.code)