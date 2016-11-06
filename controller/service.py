from flask import Flask
from operation.op_service import op_get_user

def get_user(user_id):
    return op_get_user(user_id)