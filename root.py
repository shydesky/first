from flask import Flask
from flask.ext.jsontools import jsonapi
from controller import service,login,signup
import json
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/service", methods=['POST', 'GET'])
def service():
    userid = request.args.get('userid','')
    return json.dumps(service.get_user(userid))

@app.route("/login", methods=['POST', 'GET'])
@jsonapi
def login():
    userid = request.args.get('userid','')
    return json.dumps(service.get_user(userid))

@app.route("/signup", methods=['POST', 'GET'])
@jsonapi
def signup_r():
	phone = request.args.get('phone','')
	email = request.args.get('email','')
	passwd = request.args.get('passwd','')
    return signup(phone=phone,email=email,passwd=passwd)

if __name__ == "__main__":
    app.run(host='0.0.0.0')