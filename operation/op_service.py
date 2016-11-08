from model import *
USER_FUNCTION = ['SIGNUP','SIGNIN']

def process_user(kwargs):
    ret = {}
    data = {}
    msg = 'Success'
    function = kwargs.get('function','').upper()
    if function not in USER_FUNCTION:
        msg = 'param is wrong'
    elif function == 'SIGNUP':
        data = op_signup(kwargs)
    elif function == 'SIGNIN':
        data = op_signin(kwargs)
    
    ret['data'] = data
    ret['msg'] = msg
    return ret

def op_get_user(id):
    ret = User.query.filter_by(id=id).one()
    return {'id':ret.id}

def op_signup(kwargs):
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

def op_signin(kwargs):
    pass

def process_calc(kwargs):
    arg1 = kwargs.get('arg1',0)
    arg2 = kwargs.get('arg2',0)
    return op_calc(float(arg1), float(arg2))



def op_calc(arg1, arg2):
    ret = {}
    data = {}
    msg = 'Success'
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

    ret['msg'] = msg
    ret['data'] = data
    return ret
