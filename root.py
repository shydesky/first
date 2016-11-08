from flask import Flask
from flask import request
from flask_jsontools import jsonapi
from database import db_session
from controller import service
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/service", methods=['POST', 'GET'])
@jsonapi
def service_adapter():
    return service.process()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

