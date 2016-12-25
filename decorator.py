from model import *
from flask import request
from functools import wraps

def permission_check(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        ret = {}
        key = request.args.get('token','')
        email = request.args.get('email','')
        user = User.query.filter(and_(User.clientKey==key,User.email==email)).filter(User.usertype!=0).first()
        if user:
            return func(*args, **kwargs)
        else:
            ret['msg'] = 'Permission deny'
            ret['data'] = {}
            return ret
    return new_func


def permission_check_admin(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        ret = {}
        #key = request.cookies.get('user','')
        key = 'mdf1234'
        admin = AdminUser.query.filter(AdminUser.key==key).first()
        if admin:
            return func(*args, **kwargs)
        else:
            ret['msg'] = 'Permission deny'
            ret['data'] = {}
            return ret
    return new_func