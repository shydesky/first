#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from flask import Flask, flash
from flask import request, make_response, url_for, redirect
from operation import op_service, op_download
from decorator import permission_check, permission_check_admin
import datetime
def process():
    ret = {}
    service_name = request.args.get('service', '')
    if not service_name:
        return ret
    elif service_name[0:4] == 'calc':
        ret = process_calc(service_name[4:])
    elif service_name == 'user':
        ret = process_user()
    return ret

def process_user_list():
    ret = op_service.op_get_all_user()
    return ret

@permission_check
def process_calc(type):
    ret = op_service.process_calc(request,type)
    return ret

def process_user():
    ret = op_service.process_user(request)
    return ret

def process_admin():
    resp = make_response('<a href="%s">用户管理</a> <br> <a href="%s">卡密管理</a>' % (url_for('admin'),url_for('card')))
    username = request.form['username']
    password = request.form['password']
    ret = op_service.op_admin_login(username, password)
    if ret.get('data').get('key',None):
        outdate = datetime.datetime.today() + datetime.timedelta(days=(1.0/48))
        resp.set_cookie('user', ret.get('data').get('key'), expires=outdate)
    return resp

def process_download():
    u"""软件下载."""
    return op_download.op_download_app()

def process_information():
    u"""信息初始化."""
    return op_service.op_get_information()

def process_card():
    u"""录入卡密."""
    card = request.form['card']
    card_list = card.split(',')
    cardtype = request.form['cardtype']
    res = op_service.op_set_card(card_list, cardtype)
    if res.get('data').get('data', None):
        ss = res.get('data').get('data')
        flash(u'成功添加了%s个卡密' % (len(ss)))
    else:
        flash(u'添加卡密失败!')
    return redirect(url_for('card'))

def user_get_charge():
    userid = int(request.form['userid'])
    res = op_service.user_get_charge(userid)
    return res