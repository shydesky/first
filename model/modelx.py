from sqlalchemy import Column, Integer, String
from database import Base, db_session

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    passwd = Column(String(120), unique=True)
    phone = Column(String(11), unique=True)
    clientKey = Column(String(120), unique=True)

    def __init__(self, name=None, email=None, passwd=None, phone=None, clientKey=None):
        self.name = name
        self.email = email
        self.passwd = passwd
        self.phone = phone
        self.clientKey = clientKey

    def __repr__(self):
        return '<User %r>' % (self.name)