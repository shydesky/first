from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import and_
from sqlalchemy import desc
from database import Base, db_session

import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) 
    email = Column(String(120), unique=True)
    name = Column(String(50),default='')
    passwd = Column(String(120),default='')
    phone = Column(String(11),default='')
    clientKey = Column(String(120),default='')
    userip = Column(String(20),default='')
    usertype = Column(String(2),default='0')
    create_time = Column(DateTime, default=datetime.datetime.now())
    valid_time = Column(DateTime, default=datetime.datetime.now() + datetime.timedelta(days=10))

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
    code_type = Column(Integer)
    create_time = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, userid=0, code='000000', code_type=0, create_time=datetime.datetime.now()):
        self.userid = userid
        self.code = code
        self.create_time = create_time
        self.code_type = code_type

    def __repr__(self):
        return '<VerifyCode %r>' % (self.code)

class Deposit(Base):
    __tablename__ = 'deposit'
    id = Column(Integer, primary_key=True) 
    userid = Column(Integer)
    type = Column(String(10))
    create_time = Column(DateTime, default=datetime.datetime.now())
    
    def __init__(self, userid=0, type='month', create_time=datetime.datetime.now()):
        self.userid = userid
        self.type = type
        self.create_time = create_time

    def __repr__(self):
        return '<Deposit %r>' % (self.userid)


class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    number = Column(String(32))
    type = Column(Integer)
    status = Column(Integer, default=0)

    def __init__(self, number, type):
        self.number = number
        self.type = type
        self.status = status


class AdminUser(Base):
    __tablename__ = 'adminusers'
    id = Column(Integer, primary_key=True) 
    name = Column(String(50))
    passwd = Column(String(120))
    key = Column(String(120))

    def __init__(self, name=None, passwd=None, key=None):
        self.name = name
        self.passwd = passwd
        self.key = key

    def __repr__(self):
        return '<AdminUser %r>' % (self.name)