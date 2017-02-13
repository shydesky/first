#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
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
        user = User.query.filter(User.phone == phone).first()

        if user.clientKey != key:
            ret['msg'] = u'您的账号已绑定其他机器,无法使用空间预测服务!'
            ret['data'] = {}
            return ret
        # valid_time 不用区分usertype 因为试用账户已经自动将validtime设置为createtime+10天之后的时间
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
            return redirect(url_for('admin_login'))
    return new_func