from model import User

def login(email, key):
	user = User.query.filter_by(email=email).one()
	if user:
		currentkey = user.clientKey
		db_session.commit()
		return True
	else:
		pass
