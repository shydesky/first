#-*- coding:utf-8 -*-
import requests;
import json;
def send_message_example(code,phone):
    print code,phone
    resp = requests.post(("http://api.weimi.cc/2/sms/send.html"),
    data={
        "uid": "RZPs22UzQTTU",
        "pas": "5fuuy4kd",
        "mob": phone,
        "con": code,
        "type": "json"
    },timeout=3 , verify=False);
    result =  json.loads( resp.content )
    print result