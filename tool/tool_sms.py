#-*- coding:utf-8 -*-
import requests;
import json;
def send_message_example(code,phone):
    print code, phone
    resp = requests.post(("http://api.weimi.cc/2/sms/send.html"),
    data={
        "uid": "f2Ns6qnlML1c",
        "pas": "nf4wxhx9",
        "mob": phone,
        "cid": "inLaXL7UPnaJ",
        "p1": code,
        "con": '【微米】您的验证码是：%s，10分钟内有效。如非您本人操作，可忽略本消息。' % code,
        "type": "json"
    },timeout=3, verify=False);
    result = json.loads(resp.content)
    print result
    return result