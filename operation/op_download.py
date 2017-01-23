from flask import make_response
def op_download_app():
    response = make_response(send_file("fengbaoyan.exe"))
    response.headers["Content-Disposition"] = "attachment; filename=fengbaoyan.exe;"
    return response