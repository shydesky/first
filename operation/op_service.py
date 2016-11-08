from model import *

def op_get_user(id):
    ret = User.query.filter_by(id=id).one()
    return {'id':ret.id}

def op_signup(**kwargs):
    email = kwargs.get('email','')
    phone = kwargs.get('phone','')
    passwd = kwargs.get('passwd','')
    name = kwargs.get('name','')
    users = User.query.filter_by(email=email).all()
    #import pdb;pdb.set_trace()
    if users:
        return 'user exist'

    user = User(name=name,email=email,phone=phone,passwd=passwd,clientKey='')
    db_session.add(user)
    db_session.commit()
    db_session.close() 
    return True
