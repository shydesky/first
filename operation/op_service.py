from model import *
import hashlib
import datetime,time
from decorator import permission_check_admin

USER_FUNCTION = ['SIGNUP','SIGNIN','RESETPWD','SENDCODE','GETUSERS']
ADMIN_FUNCTION = ['ADMINLOGIN','GETUSERS']
def process_admin(kwargs):
    ret = {}
    data = {}
    function = kwargs.args.get('function','').upper()
    if function not in ADMIN_FUNCTION:
        ret['msg'] = 'param is wrong'
        ret ['data'] = data
        return ret
    elif function == 'GETUSERS':
        ret = op_get_all_user()
    elif function == 'ADMINLOGIN':
        ret = op_admin_login(kwargs)

    return ret
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
    elif function == 'RESETPWD':
        ret = op_resetpwd(kwargs)
    elif function == 'SENDCODE':
        ret = op_send_verifycode(kwargs)

    return ret


def op_signup(kwargs):
    ret = {}
    data = {}
    email = kwargs.args.get('email','')
    phone = kwargs.args.get('phone','')
    passwd = kwargs.args.get('passwd','')
    name = kwargs.args.get('name','')
    usertype = kwargs.args.get('usertype','')
    users = User.query.filter_by(email=email).all()

    if users:
        ret['msg'] = 'User exist'
        ret['data'] = data
        return ret

    user = User(name=name,email=email,phone=phone,passwd=passwd,clientKey='',usertype=usertype)
    db_session.add(user)
    db_session.commit()
    
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
        data['token'] = hash_md5
        data['email'] = user.email
        data['usertype'] = user.usertype

        ret['msg'] = 'Signin Success'
        ret['data'] = data
        return ret

def op_resetpwd(kwargs):
    ret = {}
    data = {}
    email = kwargs.args.get('email','')
    passwd = kwargs.args.get('passwd','')
    verifycode = kwargs.args.get('verifycode','')

    user = User.query.filter(User.email==email).first()
    if not user:
       ret['msg'] = 'User not Exist'
       return ret

    vcode = VerifyCode.query.filter(VerifyCode.userid==user.id).order_by(desc(VerifyCode.create_time)).first()
    if vcode and (vcode.code == verifycode) and ((datetime.datetime.now() - vcode.create_time).seconds < 600):
        user = User.query.filter(User.email==email).first()
        user.passwd = passwd
        db_session.commit()
        ret['msg'] = 'Password Reset Success'
        ret['data'] = data
    else:
        ret['msg'] = 'Verifycode is invalid'
        ret['data'] = data
    return ret

def op_send_verifycode(kwargs):
    import random,string
    ret={}
    email = kwargs.args.get('email','')
    code = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    user = User.query.filter(User.email==email).first()

    if not user:
       ret['msg'] = 'User not Exist'
       return ret

    ins = VerifyCode(userid=user.id, code=code)
    db_session.add(ins)
    db_session.commit()
    ret['msg'] = 'Verifycode is Send'
    ret['data'] = {}

    return ret

def op_deposit(kwargs):
    ret={}
    email = kwargs.args.get('email','')
    deposit_type = kwargs.args.get('deposit_type','')
    user = User.query.filter(User.email==email).first()
    if not user:
       ret['msg'] = 'User not Exist'
       return ret

    ins = Deposit(userid=user.id, type=deposit_type)
    db_session.add(ins)
    db_session.commit()
    
    ret['msg'] = 'Deposit Success'
    ret['data'] = {}

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

@permission_check_admin
def op_get_all_user():
    ret = {}
    data = []
    users = User.query.all()
    for user in users:
        d = {'id':user.id,'email':user.email,'usertype':user.usertype}
        data.append(d)
    ret['msg'] = 'Success'
    ret['users'] = data
    return ret

def op_admin_login(kwargs):
    ret = {}
    data = {}
    name = kwargs.args.get('name','')
    passwd = kwargs.args.get('passwd','')
    admin = User.query.filter(and_(AdminUser.name == name,AdminUser.passwd==passwd)).first()
    if not admin:
        ret['msg'] = 'Admin User Not Exist'
        ret['data'] = {}
    else:
        hash_md5 = hashlib.md5(name + str(time.time()))
        hash_md5 = hash_md5.hexdigest()
        admin.key = hash_md5
        db_session.commit()
        db_session.close()
        
        data['key'] = hash_md5
        ret['msg'] = 'Admin User Login'
        ret['data'] = data
    return ret