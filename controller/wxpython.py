#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import requests
import wx
import hashlib
import json
import re
from wx.lib.wordwrap import wordwrap
URL_PREFIX = 'http://101.200.151.176:5000'
PWD_PREFIX = 'MDF'
TOKEN = ''
email_g = ''
class MyApp(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, wx.ID_ANY, title=u'外汇计算器', style=wx.DEFAULT_FRAME_STYLE)
        w, h = wx.DisplaySize()
        line_px = w/10
        line_py = 0
        line_sx = 5
        line_sy = h
        self.panel = wx.Panel(self.frame, wx.ID_ANY, size=(w-line_px,h), pos=(line_px,0))
        self.panel_left_1 = wx.Panel(self.frame, wx.ID_ANY, size=(line_px-line_sx,h), pos=(0,0))
        self.panel_left_2 = wx.Panel(self.frame, wx.ID_ANY, size=(line_px-line_sx,h), pos=(0,0))
        self.panel_left_3 = wx.Panel(self.frame, wx.ID_ANY, size=(line_px-line_sx,h), pos=(0,0))
        self.panel_left_4 = wx.Panel(self.frame, wx.ID_ANY, size=(line_px-line_sx,h), pos=(0,0))
       
        # copy the code for the AboutBox
 
        # change the button's parent to refer to my panel
        
        # menu
        menubar = wx.MenuBar()
        file = wx.Menu()
        help = wx.Menu()
        file.Append(wx.ID_ABOUT, "&About"," Information about this program")
        file.AppendSeparator()
        file.Append(wx.ID_EXIT,"&Exit"," Terminate the program")
        file.AppendSeparator()
        menubar.Append( file, '&File' )
        menubar.Append( help, '&Help' )

       # panel_left_1
        wx.StaticText(self.panel_left_1, -1, u'邮箱：', pos=(20,20), size=wx.DefaultSize, style=0)
        self.email = wx.TextCtrl(self.panel_left_1, -1, pos=(65,20), size=wx.DefaultSize, style=0, name="uout1")
       
        wx.StaticText(self.panel_left_1, -1, u'手机：', pos=(20,50), size=wx.DefaultSize, style=0)
        self.phone = wx.TextCtrl(self.panel_left_1, -1, pos=(65,50), size=wx.DefaultSize, style=0, name="uout1")
       
        wx.StaticText(self.panel_left_1, -1, u'密码：', pos=(20,80), size=wx.DefaultSize, style=0)
        self.passwd = wx.TextCtrl(self.panel_left_1, -1, pos=(65,80), size=wx.DefaultSize, style=wx.TE_PASSWORD)
       
        wx.StaticText(self.panel_left_1, -1, u'密码：', pos=(20,110), size=wx.DefaultSize, style=0)
        self.passwd_confirm = wx.TextCtrl(self.panel_left_1, -1, pos=(65,110), size=wx.DefaultSize, style=wx.TE_PASSWORD)

        bSignup = wx.Button(self.panel_left_1, -1, u"提交", pos=(50,150), size=wx.DefaultSize, name='bSignup')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bSignup)
       
        bBack = wx.Button(self.panel_left_1, -1, u"返回登录", pos=(50,180), size=wx.DefaultSize, name='bBack')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bBack)

        self.line = wx.StaticLine(self.panel_left_1, -1, pos=(line_px, line_py), size=(line_sx,line_sy))
        self.line.SetBackgroundColour(wx.Colour(255, 0, 0))
        # panel_left_2
        wx.StaticText(self.panel_left_2, -1, u'账号：', pos=(20,50), size=wx.DefaultSize, style=0)
        self.account = wx.StaticText(self.panel_left_2, -1, pos=(65,50), size=wx.DefaultSize, style=0)
       
        wx.StaticText(self.panel_left_2, -1, u'类型：', pos=(20,80), size=wx.DefaultSize, style=0)
        self.usertype = wx.StaticText(self.panel_left_2, -1, u'试用', pos=(65,80), size=wx.DefaultSize, style=0)
       
        bLogout = wx.Button(self.panel_left_2, -1, u"退出登录", pos=(50,110), size=wx.DefaultSize, name='bLogout')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bLogout)
        # panel_left_3
        wx.StaticText(self.panel_left_3, -1, u'账号：', pos=(20,50), size=wx.DefaultSize, style=0)
        self.email_signin = wx.TextCtrl(self.panel_left_3, -1, pos=(65,50), size=wx.DefaultSize, style=0)
       
        wx.StaticText(self.panel_left_3, -1, u'密码：', pos=(20,80), size=wx.DefaultSize, style=0)
        self.passwd_signin = wx.TextCtrl(self.panel_left_3, -1, pos=(65,80), size=wx.DefaultSize, style=wx.TE_PASSWORD)
       
        bSignin = wx.Button(self.panel_left_3, -1, u"新用户？", pos=(50,170), size=wx.DefaultSize, name='bNewUser')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bSignin)

        bSignin = wx.Button(self.panel_left_3, -1, u"登录", pos=(50,120), size=wx.DefaultSize, name='bSignin')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bSignin)

        bForgetPwd = wx.Button(self.panel_left_3, -1, u"忘记密码", pos=(50,220), size=wx.DefaultSize, name='bForgetPwd')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bForgetPwd)
        # panel_left_4
        wx.StaticText(self.panel_left_4, -1, u'账号：', pos=(20,50), size=wx.DefaultSize, style=0)
        self.email_resetpwd = wx.TextCtrl(self.panel_left_4, -1, pos=(65,50), size=wx.DefaultSize, style=0)
        
        wx.StaticText(self.panel_left_4, -1, u'新密码：', pos=(20,100), size=wx.DefaultSize, style=0)
        self.newpasswd = wx.TextCtrl(self.panel_left_4, -1, pos=(65,100), size=wx.DefaultSize, style=0)

        wx.StaticText(self.panel_left_4, -1, u'验证码：', pos=(20,150), size=wx.DefaultSize, style=0)
        self.reset_code = wx.TextCtrl(self.panel_left_4, -1, pos=(65,150), size=wx.DefaultSize, style=0)
        
        bGetCode = wx.Button(self.panel_left_4, -1, u"获取验证码", pos=(50,200), size=wx.DefaultSize, name='bGetCode')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bGetCode)
        
        bResetPwd = wx.Button(self.panel_left_4, -1, u"重置密码", pos=(50,250), size=wx.DefaultSize, name='bResetPwd')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bResetPwd)

        bBack = wx.Button(self.panel_left_1, -1, u"返回登录", pos=(50,300), size=wx.DefaultSize, name='bBack')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bBack)
        #right panel
        #first row
        FIRST_H = 20
        wx.StaticText(self.panel, -1, u'参数1', pos=(20,FIRST_H), size=wx.DefaultSize, style=0)
        wx.StaticText(self.panel, -1, u'参数2', pos=(270,FIRST_H), size=wx.DefaultSize, style=0)
        self.param1 = wx.TextCtrl(self.panel, -1, pos=(120,FIRST_H), size=wx.DefaultSize, style=0, name="param1")
        self.param2 = wx.TextCtrl(self.panel, -1, pos=(320,FIRST_H), size=wx.DefaultSize, style=0, name="param2")
        bCalc = wx.Button(self.panel, -1, u"计算", pos=(570,FIRST_H), size=wx.DefaultSize, name='bCalc')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bCalc)
        #second row
        SENCOND_H = 80
        right_base_x = 35
        tc_delta = 50
        wx.StaticText(self.panel, -1, u'结果1', pos=(right_base_x,SENCOND_H), size=wx.DefaultSize, style=0)
        self.uout1 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta,SENCOND_H), size=wx.DefaultSize, style=0, name="uout1")
       
        wx.StaticText(self.panel, -1, u'结果2', pos=(right_base_x+175,SENCOND_H), size=wx.DefaultSize, style=0)
        self.uout2 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+175,SENCOND_H), size=wx.DefaultSize, style=0, name="uout2")
       
        wx.StaticText(self.panel, -1, u'结果3', pos=(right_base_x+350,SENCOND_H), size=wx.DefaultSize, style=0)
        self.uout3 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+350,SENCOND_H), size=wx.DefaultSize, style=0, name="uout3")
       
        wx.StaticText(self.panel, -1, u'结果4', pos=(right_base_x+525,SENCOND_H), size=wx.DefaultSize, style=0)
        self.uout4 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+525,SENCOND_H), size=wx.DefaultSize, style=0, name="uout4")
       
        #third row
        THIRD_H = 120
        wx.StaticText(self.panel, -1, u'结果5', pos=(right_base_x,THIRD_H), size=wx.DefaultSize, style=0)
        self.uout5 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta,THIRD_H), size=wx.DefaultSize, style=0, name="uout5")
       
        wx.StaticText(self.panel, -1, u'结果6', pos=(right_base_x+175,THIRD_H), size=wx.DefaultSize, style=0)
        self.uout6 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+175,THIRD_H), size=wx.DefaultSize, style=0, name="uout6")
       
        wx.StaticText(self.panel, -1, u'结果7', pos=(right_base_x+350,THIRD_H), size=wx.DefaultSize, style=0)
        self.uout7 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+350,THIRD_H), size=wx.DefaultSize, style=0, name="uout7")
       
        wx.StaticText(self.panel, -1, u'结果8', pos=(right_base_x+525,THIRD_H), size=wx.DefaultSize, style=0)
        self.uout8 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+525,THIRD_H), size=wx.DefaultSize, style=0, name="uout8")
       
        #forth row
        FORTH_H = 180
        wx.StaticText(self.panel, -1, u'结果1', pos=(right_base_x,FORTH_H), size=wx.DefaultSize, style=0)
        self.dout1 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta,FORTH_H), size=wx.DefaultSize, style=0, name="dout1")
       
        wx.StaticText(self.panel, -1, u'结果2', pos=(right_base_x+175,FORTH_H), size=wx.DefaultSize, style=0)
        self.dout2 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+175,FORTH_H), size=wx.DefaultSize, style=0, name="dout2")
       
        wx.StaticText(self.panel, -1, u'结果3', pos=(right_base_x+350,FORTH_H), size=wx.DefaultSize, style=0)
        self.dout3 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+350,FORTH_H), size=wx.DefaultSize, style=0, name="dout3")
       
        wx.StaticText(self.panel, -1, u'结果4', pos=(right_base_x+525,FORTH_H), size=wx.DefaultSize, style=0)
        self.dout4 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+525,FORTH_H), size=wx.DefaultSize, style=0, name="dout4")
       
        #fifth row
        FIFTH_H = 220
        wx.StaticText(self.panel, -1, u'结果5', pos=(right_base_x,FIFTH_H), size=wx.DefaultSize, style=0)
        self.dout5 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta,FIFTH_H), size=wx.DefaultSize, style=0, name="dout5")
       
        wx.StaticText(self.panel, -1, u'结果6', pos=(right_base_x+175,FIFTH_H), size=wx.DefaultSize, style=0)
        self.dout6 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+175,FIFTH_H), size=wx.DefaultSize, style=0, name="dout6")
      
        wx.StaticText(self.panel, -1, u'结果7', pos=(right_base_x+350,FIFTH_H), size=wx.DefaultSize, style=0)
        self.dout7 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+350,FIFTH_H), size=wx.DefaultSize, style=0, name="dout7")
       
        wx.StaticText(self.panel, -1, u'结果8', pos=(right_base_x+525,FIFTH_H), size=wx.DefaultSize, style=0)
        self.dout8 = wx.TextCtrl(self.panel, -1, pos=(right_base_x+tc_delta+525,FIFTH_H), size=wx.DefaultSize, style=0, name="dout8")
       
        self.frame.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        # StatusBar
        self.statusbar = self.frame.CreateStatusBar()
        self.statusbar.SetFieldsCount(1)

        #self.panel.Bind(wx.EVT_MOTION, self.OnPaintMotion)
        self.panel.SetBackgroundColour((211,244,254))
        #self.panel.Hide()
        self.panel_left_1.SetBackgroundColour((211,244,254))
        self.panel_left_2.SetBackgroundColour((211,244,254))
        self.panel_left_3.SetBackgroundColour((211,244,254))
        self.panel_left_4.SetBackgroundColour((211,244,254))
        self.panel_left_1.Hide()
        self.panel_left_2.Hide()
        self.panel_left_4.Hide()
        #self.panel_left.Hide()
        self.frame.SetMenuBar( menubar )
        self.frame.SetSize( wx.Size( w/2,h/2 ))
        self.frame.SetMaxSize(wx.Size( w/2,h/2 ))
        self.frame.SetMinSize(wx.Size( w/2,h/2 ))
        self.frame.Centre()
        self.frame.Show()
    
    def OnPaintMotion(self, event):
        #设置状态栏1内容
        self.statusbar.SetStatusText(u"鼠标位置：" + str(event.GetPositionTuple()), 0)             
        event.Skip()

    def OnButton(self, evt):
        #Button的响应事件
        name = evt.GetEventObject().GetName()
        if name == 'bCalc':
            self.op_calc()
        elif name == 'bSignup': #用户注册panel
            self.op_signup()
        elif name == 'bSignin': #用户登入panel
            if self.op_signin():
                self.panel_left_2.Show()
                self.panel_left_3.Hide()
        elif name == 'bNewUser':
            self.panel_left_3.Hide()
            self.panel_left_1.Show()
        elif name == 'bBack':
            self.panel_left_3.Show()
            self.panel_left_1.Hide()
        elif name == 'bLogout':
            self.op_logout()
            self.panel_left_3.Show()
            self.panel_left_2.Hide()
        elif name == 'bForgetPwd':
            self.panel_left_3.Hide()
            self.panel_left_4.Show()
        elif name == 'bGetCode':
            self.op_get_code()
        elif name == 'bResetPwd':
            if self.op_reset_passwd():
                self.panel_left_3.Show()
                self.panel_left_4.Hide()

    def op_calc(self):
        #import pdb;pdb.set_trace()
        url = URL_PREFIX + '/service?service=calc&arg1=%s&arg2=%s&email=%s&token=%s'
        url = url % (self.param1.GetValue(),self.param2.GetValue(),email_g,TOKEN)
        print url
        response = requests.get(url).json()
        #import pdb;pdb.set_trace()
        #print self.param1.GetValue() + self.param2.GetValue()
        msg = response.get('msg')
        data = response.get('data')
        self.uout1.SetValue(str(data.get('X1')))
        self.uout2.SetValue(str(data.get('X2')))
        self.uout3.SetValue(str(data.get('X3')))
        self.uout4.SetValue(str(data.get('X4')))
        self.uout5.SetValue(str(data.get('X5')))
        self.uout6.SetValue(str(data.get('X6')))
        self.uout7.SetValue(str(data.get('X7')))
        self.uout8.SetValue(str(data.get('X8')))

        self.dout1.SetValue(str(data.get('Y1')))
        self.dout2.SetValue(str(data.get('Y2')))
        self.dout3.SetValue(str(data.get('Y3')))
        self.dout4.SetValue(str(data.get('Y4')))
        self.dout5.SetValue(str(data.get('Y5')))
        self.dout6.SetValue(str(data.get('Y6')))
        self.dout7.SetValue(str(data.get('Y7')))
        self.dout8.SetValue(str(data.get('Y8')))
        self.statusbar.SetStatusText(msg, 0)

    #登录
    def op_signin(self):
        global email_g , TOKEN
        email = self.email_signin.GetValue()
        passwd = hashlib.md5(PWD_PREFIX + self.passwd_signin.GetValue()).hexdigest()
        url = URL_PREFIX + '/service?service=user&function=signin&email=%s&passwd=%s'
        url = url % (email,passwd)
       
        response = requests.get(url).json()
        msg = response.get('msg')
        flag = response.get('code')
        self.statusbar.SetStatusText(msg, 0)
        print response
        if flag:
            email_g = str(response.get('data').get('email'))
            TOKEN = str(response.get('data').get('token'))
            self.account.SetLabel(email_g)
            self.usertype.SetLabel(str(response.get('data').get('usertype')))
            return True
        else:
            return False

    #注册
    def op_signup(self):
        phone = self.phone.GetValue()
        p_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        phonematch=p_re.match(phone)
        if not phonematch:
            self.statusbar.SetStatusText(u'手机号码无效！', 0)
            return
       
        email = self.email.GetValue()
        e_re = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")
        emailmatch=e_re.match(email)
        if not emailmatch:
            self.statusbar.SetStatusText(u'邮箱格式无效！', 0)
            return

        passwd = hashlib.md5(PWD_PREFIX + self.passwd.GetValue()).hexdigest()
        passwd_confirm = hashlib.md5(PWD_PREFIX + self.passwd_confirm.GetValue()).hexdigest()
        if passwd != passwd_confirm:
            self.statusbar.SetStatusText(u'密码输入不一致！', 0)
            return
        url = URL_PREFIX + '/service?service=user&function=signup&email=%s&passwd=%s&phone=%s'
        url = url % (email, passwd, phone)
        response = requests.get(url).json()

        msg = response.get('msg')
        self.statusbar.SetStatusText(msg, 0)

    #退出
    def op_logout(self):
        global email_g , TOKEN
        email_g = ''
        TOKEN = ''
        self.passwd_signin.SetValue('') 
        self.statusbar.SetStatusText(u'您已成功退出', 0)

    def op_reset_passwd(self):
        url = URL_PREFIX + '/service?service=user&function=resetpwd&email=%s&verifycode=%s&passwd=%s'
        email = self.email_resetpwd.GetValue()
        code = self.reset_code.GetValue()
        newpasswd = hashlib.md5(PWD_PREFIX + self.newpasswd.GetValue()).hexdigest()
        url = url % (email, code, newpasswd)
        response = requests.get(url).json()
        
        msg = response.get('msg')
        flag = response.get('code')
        self.statusbar.SetStatusText(msg, 0)
        if flag:
            return True
        else:
            return False

    def op_get_code(self):
        url = URL_PREFIX + '/service?service=user&function=getcode&email=%s'
        email = self.email_resetpwd.GetValue()
        url = url % (email)
        response = requests.get(url).json()
        msg = response.get('msg')
        self.statusbar.SetStatusText(msg, 0)

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()