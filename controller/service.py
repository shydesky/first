from flask import Flask
from flask import request, make_response
from operation import op_service
from decorator import permission_check, permission_check_admin

def process():
    ret = {}
    service_name = request.args.get('service','')
    if not service_name:
        return ret
    elif service_name[0:4] == 'calc':
        ret = process_calc(service_name[4:])
    elif service_name == 'user':
        ret = process_user()
    elif service_name == 'admin':
        ret = process_admin()
    return ret

@permission_check
def process_calc(type):
    ret = op_service.process_calc(request,type)
    return ret

def process_user():
    ret = op_service.process_user(request)
    return ret


def process_admin():
    resp = make_response()
    ret = op_service.process_admin(request)
    resp.set_cookie('user', ret.get('data').get('key'))
    return resp