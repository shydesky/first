#-*- coding:utf-8 -*-
import requests;
import json;
def send_messag_example():
    resp = requests.post(("http://api.weimi.cc/2/sms/send.html"),
    data={
        "uid": "AvwM2OSpi1VD",
        "pas": "u3zhavh4",
        "mob": "15901009909",
        "con": "【微米】您的验证码是：610912，3分钟内有效。如非您本人操作，可忽略本消息。",
        "type": "json"
    },timeout=3 , verify=False);
    result =  json.loads( resp.content )
    print result