from model import *

def op_get_user(id):
	ret = User.query.filter_by(id=id).one()
	return {'id':ret.id}