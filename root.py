from flask import Flask
from controller import service
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/service", methods=['POST', 'GET'])
def service():
	userid = request.form['userid']
    service.get_user(userid)

if __name__ == "__main__":
    app.run(host='0.0.0.0')