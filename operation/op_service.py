from model import *

def process_calc(kwargs):
    arg1 = kwargs.get('arg1',0)
    arg2 = kwargs.get('arg2',0)
    return op_calc(float(arg1), float(arg2))

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
    ret['X1'] = round((arg2/arg1*2.0-1)*arg1, 4)
    ret['X2'] = round((arg2/arg1*3.0-2)*arg1, 4)
    ret['X3'] = round((arg2/arg1*4.0-3)*arg1, 4)
    ret['X4'] = round((arg2/arg1*5.0-4)*arg1, 4)
    ret['X5'] = round((arg2/arg1*6.0-5)*arg1, 4)
    ret['X6'] = round((arg2/arg1*7.0-6)*arg1, 4)
    ret['X7'] = round((arg2/arg1*8.0-7)*arg1, 4)
    ret['X8'] = round((arg2/arg1*9.0-8)*arg1, 4)

    ret['Y1'] = round(arg2/(arg2/arg1*2.0-1), 4)
    ret['Y2'] = round(arg2/(arg2/arg1*3.0-2), 4)
    ret['Y3'] = round(arg2/(arg2/arg1*4.0-3), 4)
    ret['Y4'] = round(arg2/(arg2/arg1*5.0-4), 4)
    ret['Y5'] = round(arg2/(arg2/arg1*6.0-5), 4)
    ret['Y6'] = round(arg2/(arg2/arg1*7.0-6), 4)
    ret['Y7'] = round(arg2/(arg2/arg1*8.0-7), 4)
    ret['Y8'] = round(arg2/(arg2/arg1*9.0-8), 4)
    
    return ret
