from model import *
import hashlib
import time
USER_FUNCTION = ['SIGNUP','SIGNIN']

def process_user(kwargs):
    ret = {}
    data = {}
    function = kwargs.args.get('function','').upper()
    if function not in USER_FUNCTION:
        ret['msg'] = 'param is wrong'
        ret ['data'] = data
        return ret
    elif function == 'SIGNUP':
        ret = op_signup(kwargs)
    elif function == 'SIGNIN':
        ret = op_signin(kwargs)

    return ret


def op_signup(kwargs):
    ret = {}
    data = {}
    email = kwargs.args.get('email','')
    phone = kwargs.args.get('phone','')
    passwd = kwargs.args.get('passwd','')
    name = kwargs.args.get('name','')
    users = User.query.filter_by(email=email).all()
    
    if users:
        ret['msg'] = 'User exist'
        ret['data'] = data
        return ret

    user = User(name=name,email=email,phone=phone,passwd=passwd,clientKey='')
    db_session.add(user)
    db_session.commit()
    db_session.close()
    
    ret['msg'] = 'Signup Success'
    ret['data'] = data
    return ret

def op_signin(kwargs):
    ret = {}
    data = {}
    email = kwargs.args.get('email','')
    passwd = kwargs.args.get('passwd','')
    userip = kwargs.remote_addr
    user = User.query.filter(and_(User.email==email,User.passwd==passwd)).first()
    
    if not user:
        ret['msg'] = 'User not exist'
        ret['data'] = {}
        return ret
    else:
        hash_md5 = hashlib.md5(email + str(time.time()))
        hash_md5 = hash_md5.hexdigest()
        user.clientKey = hash_md5
        user.userip = userip
        db_session.commit()
        db_session.close()
        data['token'] = hash_md5

        ret['msg'] = 'Signin Success'
        ret['data'] = data
        return ret

def process_calc(kwargs):
    arg1 = kwargs.args.get('arg1',0)
    arg2 = kwargs.args.get('arg2',0)
    return op_calc(float(arg1), float(arg2))



def op_calc(arg1, arg2):
    ret = {}
    data = {}

    data['X1'] = round((arg2/arg1*2.0-1)*arg1, 5)
    data['X2'] = round((arg2/arg1*3.0-2)*arg1, 5)
    data['X3'] = round((arg2/arg1*4.0-3)*arg1, 5)
    data['X4'] = round((arg2/arg1*5.0-4)*arg1, 5)
    data['X5'] = round((arg2/arg1*6.0-5)*arg1, 5)
    data['X6'] = round((arg2/arg1*7.0-6)*arg1, 5)
    data['X7'] = round((arg2/arg1*8.0-7)*arg1, 5)
    data['X8'] = round((arg2/arg1*9.0-8)*arg1, 5)

    data['Y1'] = round(arg2/(arg2/arg1*2.0-1), 5)
    data['Y2'] = round(arg2/(arg2/arg1*3.0-2), 5)
    data['Y3'] = round(arg2/(arg2/arg1*4.0-3), 5)
    data['Y4'] = round(arg2/(arg2/arg1*5.0-4), 5)
    data['Y5'] = round(arg2/(arg2/arg1*6.0-5), 5)
    data['Y6'] = round(arg2/(arg2/arg1*7.0-6), 5)
    data['Y7'] = round(arg2/(arg2/arg1*8.0-7), 5)
    data['Y8'] = round(arg2/(arg2/arg1*9.0-8), 5)

    ret['data'] = data
    ret['msg'] ='calc Success'
    return ret
