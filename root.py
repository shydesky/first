from flask import Flask, render_template
from flask import request
from flask_jsontools import jsonapi
from database import db_session
from controller import service
app = Flask(__name__, static_url_path='')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/service", methods=['POST', 'GET'])
@jsonapi
def service_adapter():
    return service.process()

@app.route("/admin1")
def admin():
    return render_template('ss.html')

@app.route("/admin/users", methods=['GET','POST'])
def admin():
    return service.process_user_list()

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
    app.run(host='0.0.0.0')
if __name__ == "__main__":
    app.run(host='0.0.0.0')

