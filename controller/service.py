from flask import Flask
from flask import request
from operation import op_service

def get_user(user_id):
    return op_service.op_get_user(user_id)

def process():
	ret = {}
	service_name = request.args.get('service','')
	if not service_name:
		return ret
	elif service_name == 'calc':
        ret = op_service.process_calc(request.args)
    elif service_name = 'user':
    	ret = op_service.process_user(request.args)
    return ret
