from flask import make_response
from flask import send_file
def op_download_app():
    response = make_response(send_file("StormEye.exe"))
    response.headers["Content-Disposition"] = "attachment; filename=StormEye.exe;"
    return response