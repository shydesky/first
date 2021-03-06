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

    def __init__(self, name=None, email=None, passwd=None, phone=None, clientKey=None, userip=None, usertype=0, create_time=None):
        self.name = name
        self.email = email
        self.passwd = passwd
        self.phone = phone
        self.clientKey = clientKey
        self.userip = userip
        self.usertype = usertype
        if create_time is None:
            create_time = datetime.datetime.now()
        self.create_time = create_time
        self.valid_time = create_time + datetime.timedelta(days=10)

    def __repr__(self):
        return '<User %r>' % (self.name)

class VerifyCode(Base):
    __tablename__ = 'verifycode'
    id = Column(Integer, primary_key=True) 
    userid = Column(Integer)
    code = Column(String(50))
    code_type = Column(Integer)
    create_time = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, userid=0, code='000000', code_type=0, create_time=None):
        self.userid = userid
        self.code = code
        if create_time is None:
            create_time = datetime.datetime.now()
        self.create_time = create_time
        self.code_type = code_type

    def __repr__(self):
        return '<VerifyCode %r>' % (self.code)

class Deposit(Base):
    __tablename__ = 'deposit'
    id = Column(Integer, primary_key=True) 
    userid = Column(Integer)
    card_id = Column(String(32))
    create_time = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, userid, card_id, create_time=None):
        self.userid = userid
        self.card_id = card_id
        if create_time is None:
            create_time = datetime.datetime.now()
        self.create_time = create_time

    def __repr__(self):
        return '<Deposit %r>' % (self.userid)


class Card(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    number = Column(String(32))
    password = Column(String(32))
    type = Column(Integer)
    status = Column(Integer, default=0)

    def __init__(self, number, password, type, status):
        self.number = number
        self.type = type
        self.status = status
        self.password = password


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
