from model import *
from flask import request, url_for, redirect
from werkzeug.routing import RequestRedirect
from functools import wraps
from constant import *
import datetime
import hashlib
def permission_check(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        ret = {}
        key = request.args.get('key', '')
        phone = request.args.get('account', '')
        key = hashlib.md5(phone + key).hexdigest()
        user = User.query.filter(and_(User.clientKey == key, User.phone == phone)).first()
        if not user:
            ret['msg'] = 'Permission deny'
            ret['data'] = {}
            return ret
        if user.valid_time > datetime.datetime.now():
            return func(*args, **kwargs)
        else:
            ret['msg'] = BALANCE_NOT_ENOUGH
            ret['data'] = {}
            return ret
    return new_func


def permission_check_admin(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        ret = {}
        key = request.cookies.get('user','')
        admin = AdminUser.query.filter(AdminUser.key==key).first()
        if admin:
            return func(*args, **kwargs)
        else:
            raise RequestRedirect(url_for('admin_login'))
    return new_func