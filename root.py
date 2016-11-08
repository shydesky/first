from flask import Flask
from flask import request
from flask_jsontools import jsonapi
from database import db_session
from controller import service,login,signup
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# @app.route("/service", methods=['POST', 'GET'])
# @jsonapi
# def service():
#     userid = request.args.get('userid','')
#     return service.get_user(userid)

@app.route("/service", methods=['POST', 'GET'])
@jsonapi
def service():
    return service.process()

@app.route("/login", methods=['POST', 'GET'])
@jsonapi
def login():
    userid = request.args.get('userid','')
    return service.login(userid)

@app.route("/signup", methods=['POST', 'GET'])
@jsonapi
def signup_r():
    phone = request.args.get('phone','')
    email = request.args.get('email','')
    passwd = request.args.get('passwd','')
    name = request.args.get('name','')
    return signup.signup(name=name,phone=phone,email=email,passwd=passwd)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

