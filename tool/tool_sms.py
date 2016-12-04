#-*- coding:utf-8 -*-
import requests;
import json;
def send_messag_example(code):
    resp = requests.post(("http://api.weimi.cc/2/sms/send.html"),
    data={
        "uid": "AvwM2OSpi1VD",
        "pas": "u3zhavh4",
        "mob": "15901009909",
        "con": code,
        "type": "json"
    },timeout=3 , verify=False);
    result =  json.loads( resp.content )
    print result