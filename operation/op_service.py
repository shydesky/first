from model import *

def process_calc(kwargs):
    arg1 = kwargs.get('arg1',0)
    arg2 = kwargs.get('arg2',0)
    return op_calc(arg1, arg2)

def process_user(kwargs):
    pass

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

def op_calc(arg1, arg2):
    ret = {}
    ret['X1'] = (arg2/arg1*2.0-1)*arg1
    ret['X2'] = (arg2/arg1*3.0-2)*arg1
    ret['X3'] = (arg2/arg1*4.0-3)*arg1
    ret['X4'] = (arg2/arg1*5.0-4)*arg1
    ret['X5'] = (arg2/arg1*6.0-5)*arg1
    ret['X6'] = (arg2/arg1*7.0-6)*arg1
    ret['X7'] = (arg2/arg1*8.0-7)*arg1
    ret['X8'] = (arg2/arg1*9.0-8)*arg1

    ret['Y1'] = arg2/(arg2/arg1*2.0-1)
    ret['Y2'] = arg2/(arg2/arg1*3.0-2)
    ret['Y3'] = arg2/(arg2/arg1*4.0-3)
    ret['Y4'] = arg2/(arg2/arg1*5.0-4)
    ret['Y5'] = arg2/(arg2/arg1*6.0-5)
    ret['Y6'] = arg2/(arg2/arg1*7.0-6)
    ret['Y7'] = arg2/(arg2/arg1*8.0-7)
    ret['Y8'] = arg2/(arg2/arg1*9.0-8)
    
    return ret
