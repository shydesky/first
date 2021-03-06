from flask import Flask, render_template
from flask import request
from flask_jsontools import jsonapi
from database import db_session
from controller import service
from decorator import permission_check_admin
app = Flask(__name__, static_url_path='')
app.secret_key = 'some_secret'
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/file/servicefile")
def servicefile():
    return render_template('servicefile.html')

@app.route("/index")
def index():
    return "Hello World!"

@app.route("/service", methods=['POST', 'GET'])
@jsonapi
def service_adapter():
    return service.process()

@app.route("/admin1")
@permission_check_admin
def admin():
    return render_template('ss.html')

@app.route("/admin/card", methods=['POST', 'GET'])
@permission_check_admin
def card():
    if request.method == 'GET':
        return render_template('card.html')
    elif request.method == 'POST':
        return service.process_card()

@app.route("/admin/users", methods=['GET','POST'])
@jsonapi
def admin_user():
    return service.process_user_list()

@app.route("/user/<int:userid>", methods=['GET','POST'])
def user(userid):
    if request.method == 'GET':
        return render_template('userchargedetail.html')

@app.route("/user/getcharge", methods=['GET','POST'])
@jsonapi
def user_get_charge():
    if request.method == 'POST':
        return service.user_get_charge()

@app.route("/admin/login", methods=['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin_login.html')
    elif request.method == 'POST':
        return service.process_admin()

@app.route("/download", methods=['POST', 'GET'])
def download():
    return service.process_download()

@app.route("/information", methods=['POST', 'GET'])
def information():
    return service.process_information()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def application():
    app.run(host='0.0.0.0', port=80)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
