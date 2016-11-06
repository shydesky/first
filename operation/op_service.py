from model import *

def op_get_user(id):
    ret = User.query.filter_by(id=id).one()
    return {'id':ret.id}

def op_signup(**kwargs):
    email = kwargs.get('email','')
    phone = kwargs.get('phone','')
    passwd= kwargs.get('passwd','')
    user = User.query.filter_by(email=email).one()
    import pdb;pdb.set_trace()
    if user:
        return 'user exist'
    clientKey = generate_clientKey()
    user = User(email=email,phone=phone,passwd=passwd,clientKey='')
    db_session.add(user)
    db_session.commit()
    
    return True