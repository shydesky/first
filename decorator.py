from model import *

from functools import wraps

def permission_check(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        ret = {}
        key = args.get('token','')
        email = args.get('email','')
        user = User.query.filter(and_(User.clientKey==key,User.email==email)).first()
        if user:
            return func(self, *args, **kwargs)
        else:
            ret['msg'] = 'Permission deny'
            ret['data'] = {}
            return ret
    return new_func