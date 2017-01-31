from flask import Flask
from flask import request, make_response, url_for
from operation import op_service, op_download
from decorator import permission_check, permission_check_admin
import datetime
def process():
    ret = {}
    service_name = request.args.get('service', '')
    if not service_name:
        return ret
    elif service_name[0:4] == 'calc':
        ret = process_calc(service_name[4:])
    elif service_name == 'user':
        ret = process_user()
    elif service_name == 'admin':
        ret = process_admin()
    return ret

def process_user_list():
    ret = op_service.op_get_all_user()
    return ret

@permission_check
def process_calc(type):
    ret = op_service.process_calc(request,type)
    return ret

def process_user():
    ret = op_service.process_user(request)
    return ret

def process_admin():
    resp = make_response('<a href="%s">index</a>' % url_for('admin'))
    username = request.form['username']
    password = request.form['password']
    ret = op_service.op_admin_login(username, password)
    if ret.get('data').get('key',None):
        outdate = datetime.datetime.today() + datetime.timedelta(days=(1.0/48))
        resp.set_cookie('user', ret.get('data').get('key'), expires=outdate)
    return resp

def process_download():
    return op_download.op_download_app()

def process_information():
    return op_service.op_get_information()