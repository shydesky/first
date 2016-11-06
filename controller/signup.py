from flask import Flask
from operation.op_service import op_signup


def signup(**kwargs):
    return op_signup(**kwargs)