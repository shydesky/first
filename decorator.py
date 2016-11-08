from model import *
from flask import request
from functools import wraps

def permission_check(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        ret = {}
        #key = kwargs.get('token','')
        #email = kwargs.get('email','')
        key = request.args.get('token','')
        email = request.args.get('email','')
        user = User.query.filter(and_(User.clientKey==key,User.email==email)).first()
        if user:
            return func(*args, **kwargs)
        else:
            ret['msg'] = 'Permission deny'
            ret['data'] = {}
            return ret
    return new_func