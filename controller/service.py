from flask import Flask
from flask import request
from operation import op_service
from decorator import permission_check

def get_user(user_id):
    return op_service.op_get_user(user_id)

def process():
    ret = {}
    service_name = request.args.get('service','')
    if not service_name:
        return ret
    elif service_name == 'calc':
        ret = process_calc(request.args)
    elif service_name == 'user':
        ret = op_service.process_user(request.args)
    return ret

@permission_check
def process_calc(**kwargs):
	ret = op_service.process_calc(request.args)
	return ret