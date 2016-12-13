from model import *
import hashlib
import datetime,time
from decorator import permission_check_admin
from constant import *

USER_FUNCTION = ['SIGNUP','SIGNIN','RESETPWD','GETCODE','GETUSERS']
ADMIN_FUNCTION = ['ADMINLOGIN','GETUSERS','CHANGEUSERTYPE']
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
    elif function == 'CHANGEUSERTYPE':
        ret = op_admin_change_user_type(kwargs)
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
    elif function == 'GETCODE':
        ret = op_send_verifycode(kwargs)

    return ret


def op_signup(kwargs):
    ret = {}
    data = {}
    email = kwargs.args.get('email','')
    phone = kwargs.args.get('phone','')
    passwd = kwargs.args.get('passwd','')
    name = kwargs.args.get('name','')
    usertype = kwargs.args.get('usertype','0')
    users = User.query.filter_by(email=email).all()

    if users:
        ret['msg'] = USER_EXIST
        ret['data'] = data
        ret['code'] = 0
        return ret

    user = User(name=name,email=email,phone=phone,passwd=passwd,clientKey='',usertype=usertype)
    db_session.add(user)
    db_session.commit()

    ret['msg'] = SIGNUP_SUCCESS
    ret['data'] = data
    ret['code'] = 1
    return ret

def op_signin(kwargs):
    ret = {}
    data = {}
    email = kwargs.args.get('email','')
    passwd = kwargs.args.get('passwd','')
    userip = kwargs.remote_addr
    user = User.query.filter(User.email==email).first()

    if not user:
        ret['msg'] = USER_NOT_EXIST
        ret['data'] = {}
        ret['code'] = 0
        return ret
    else:
        if user.passwd != passwd:
            ret['msg'] = USER_PASSWD_WRONG
            ret['data'] = {}
            ret['code'] = 0
            return ret
        hash_md5 = hashlib.md5(email + str(time.time()))
        hash_md5 = hash_md5.hexdigest()
        user.clientKey = hash_md5
        user.userip = userip
        db_session.commit()
        data['token'] = hash_md5
        data['email'] = user.email
        data['usertype'] = user.usertype

        ret['msg'] = SIGNIN_SUCCESS
        ret['data'] = data
        ret['code'] = 1
        return ret

def op_resetpwd(kwargs):
    ret = {}
    data = {}
    email = kwargs.args.get('email','')
    passwd = kwargs.args.get('passwd','')
    verifycode = kwargs.args.get('verifycode','')

    user = User.query.filter(User.email==email).first()
    if not user:
       ret['msg'] = USER_NOT_EXIST
       ret['code'] = 0
       return ret

    vcode = VerifyCode.query.filter(VerifyCode.userid==user.id).order_by(desc(VerifyCode.create_time)).first()
    if vcode and (vcode.code == verifycode) and ((datetime.datetime.now() - vcode.create_time).seconds < 600):
        user = User.query.filter(User.email==email).first()
        user.passwd = passwd
        db_session.commit()
        ret['msg'] = PASSWORD_RESET_SUCCESS
        ret['data'] = data
        ret['code'] = 1
    else:
        ret['msg'] = VERIFYCODE_IS_INVALID
        ret['data'] = data
        ret['code'] = 0
    return ret

def op_send_verifycode(kwargs):
    import random,string
    from tool.tool_sms import send_message_example
    ret={}
    email = kwargs.args.get('email','')
    code = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    user = User.query.filter(User.email==email).first()

    if not user:
       ret['msg'] = USER_NOT_EXIST
       ret['data'] = {}
       ret['code'] = 0
       return ret
    result = send_message_example(code, user.phone)
    if result.get('code') != 0:
        ret['msg'] = CODE_SERVICE_WRONG
        ret['data'] = {}
        ret['code'] = 0
        return ret
    code = '000000' #temp code
    ins = VerifyCode(userid=user.id, code=code, create_time=datetime.datetime.now())
    db_session.add(ins)
    db_session.commit()
    ret['msg'] = VERIFYCODE_IS_SEND
    ret['data'] = {}
    ret['code'] = 1
    return ret

def op_deposit(kwargs):
    ret={}
    email = kwargs.args.get('email','')
    deposit_type = kwargs.args.get('deposit_type','')
    user = User.query.filter(User.email==email).first()
    if not user:
       ret['msg'] = USER_NOT_EXIST
       return ret

    ins = Deposit(userid=user.id, type=deposit_type)
    db_session.add(ins)
    db_session.commit()

    ret['msg'] = DEPOSIT_SUCCESS
    ret['data'] = {}

    return ret

def process_calc(kwargs, index):
    arg1 = kwargs.args.get('arg1',0)
    arg2 = kwargs.args.get('arg2',0)
    return op_calc(float(arg1), float(arg2), index)

    

def op_calc(arg1, arg2, index):
    ret = {}
    data = {}
    if index == '1':
        data['X1'] = "%.5f" % round((arg2/arg1*2.0-1)*arg1, 5)
        data['X2'] = "%.5f" % round((arg2/arg1*3.0-2)*arg1, 5)
        data['X3'] = "%.5f" % round((arg2/arg1*4.0-3)*arg1, 5)
        data['X4'] = "%.5f" % round((arg2/arg1*5.0-4)*arg1, 5)
        data['X5'] = "%.5f" % round((arg2/arg1*6.0-5)*arg1, 5)
        data['X6'] = "%.5f" % round((arg2/arg1*7.0-6)*arg1, 5)
        data['X7'] = "%.5f" % round((arg2/arg1*8.0-7)*arg1, 5)
        data['X8'] = "%.5f" % round((arg2/arg1*9.0-8)*arg1, 5)
    elif index == '2':
        data['Y1'] = "%.5f" % round(arg2/(arg2/arg1*2.0-1), 5)
        data['Y2'] = "%.5f" % round(arg2/(arg2/arg1*3.0-2), 5)
        data['Y3'] = "%.5f" % round(arg2/(arg2/arg1*4.0-3), 5)
        data['Y4'] = "%.5f" % round(arg2/(arg2/arg1*5.0-4), 5)
        data['Y5'] = "%.5f" % round(arg2/(arg2/arg1*6.0-5), 5)
        data['Y6'] = "%.5f" % round(arg2/(arg2/arg1*7.0-6), 5)
        data['Y7'] = "%.5f" % round(arg2/(arg2/arg1*8.0-7), 5)
        data['Y8'] = "%.5f" % round(arg2/(arg2/arg1*9.0-8), 5)

    ret['data'] = data
    ret['msg'] = CALC_SUCCESS
    return ret

@permission_check_admin
def op_get_all_user():
    ret = {}
    data = []
    users = User.query.all()
    for user in users:
        d = {'id':user.id,'email':user.email,'usertype':user.usertype}
        data.append(d)
    ret['msg'] = SUCCESS
    ret['users'] = data
    return ret

def op_admin_login(kwargs):
    ret = {}
    data = {}
    name = kwargs.args.get('name','')
    passwd = kwargs.args.get('passwd','')
    admin = User.query.filter(and_(AdminUser.name == name,AdminUser.passwd==passwd)).first()
    if not admin:
        ret['msg'] = ADMIN_USER_NOT_EXIST
        ret['data'] = {}
    else:
        hash_md5 = hashlib.md5(name + str(time.time()))
        hash_md5 = hash_md5.hexdigest()
        admin.key = hash_md5
        db_session.commit()
        db_session.close()

        data['key'] = hash_md5
        ret['msg'] = ADMIN_USER_LOGIN
        ret['data'] = data
    return ret

def op_admin_change_user_type(kwargs):
    ret = {}
    data = {}
    email = kwargs.args.get('email','')
    usertype = kwargs.args.get('usertype','')
    user = User.query.filter(User.email == email).first()
    if not user:
        ret['msg'] = USER_NOT_EXIST
        ret['data'] = {}
    else:
        user.usertype = usertype
        db_session.commit()
        db_session.close()
        ret['msg'] = SUCCESS
        ret['data'] = data
    return ret