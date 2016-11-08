from sqlalchemy import Column, Integer, String
from sqlalchemy import and_
from database import Base, db_session

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) 
    email = Column(String(120), unique=True)
    name = Column(String(50))
    passwd = Column(String(120))
    phone = Column(String(11))
    clientKey = Column(String(120))

    def __init__(self, name=None, email=None, passwd=None, phone=None, clientKey=None):
        self.name = name
        self.email = email
        self.passwd = passwd
        self.phone = phone
        self.clientKey = clientKey

    def __repr__(self):
        return '<User %r>' % (self.name)