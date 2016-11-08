from flask import Flask
from flask import request
from operation import op_service
from decorator import permission_check

def process():
    ret = {}
    service_name = request.args.get('service','')
    if not service_name:
        return ret
    elif service_name == 'calc':
        ret = process_calc()
    elif service_name == 'user':
        ret = process_user()
    return ret

@permission_check
def process_calc():
    ret = op_service.process_calc(request)
    return ret

def process_user():
    ret = op_service.process_user(request)
    return ret