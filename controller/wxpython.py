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
        
        # # panel_left_2
        # wx.StaticText(self.panel_left_2, -1, u'账号：', pos=(20,50), size=wx.DefaultSize, style=0)
        # self.account = wx.StaticText(self.panel_left_2, -1, pos=(65,50), size=wx.DefaultSize, style=0)

        # wx.StaticText(self.panel_left_2, -1, u'类型：', pos=(20,80), size=wx.DefaultSize, style=0)
        # self.usertype = wx.StaticText(self.panel_left_2, -1, u'试用', pos=(65,80), size=wx.DefaultSize, style=0)

        # bLogout = wx.Button(self.panel_left_2, -1, u"退出登录", pos=(50,110), size=wx.DefaultSize, name='bLogout')
        # self.Bind(wx.EVT_BUTTON, self.OnButton, bLogout)
        
       
        #right panel



        #self.frame.SetMaxSize(wx.Size( w/2,h/2 ))
        #self.frame.SetMinSize(wx.Size( w/2,h/2 ))
        self.init_login_frame()
        self.login_frame.Centre()
        self.login_frame.Show()
        
    def OnQuit(self, event):
        self.frame.Close()

    def OnMenu(self, event):
        print 1
        # import pdb;pdb.set_trace()
        print event.GetEventObject().GetId()
    def OnKJYC(self, event): # 空间预测
        self.kjyc_panel.SetBackgroundColour((211,244,254))
        self.kjyc_panel.SetSize(wx.Size(self.w,self.h))
        self.kjyc_panel.Show()
    def OnCJRL(self, event): # 财经日历
        pass
    def OnCJZZ(self, event): # 财经主站
        pass 
    def OnGY(self, event):  # 关于
        dlg = wx.MessageDialog(parent=None, message=u"我们是风暴眼", caption=u"关于我们", style=wx.YES_NO)
        dlg.ShowModal()
    def OnLXWM(self, event): # 联系我们
        pass 
    def OnZXGX(self, event): # 在线更新
        pass   
    def OnAbout(self, event):
        pass

    def OnButton(self, evt):
        #Button的响应事件
        #import pdb;pdb.set_trace()
        name = evt.GetEventObject().GetName()
        if name == 'bCalc1':
            self.op_calc1()
        elif name == 'bCalc2':
            self.op_calc2()
        elif name == 'bSignup': #用户注册panel
            self.op_signup()
        elif name == 'bSignin': #用户登入panel
            if self.op_signin():
                self.init_app_frame()
                self.login_frame.Hide()
                self.app_frame.Show()
                # self.self.panel_signin.Hide()
        elif name == 'bNewUser':
            self.panel_signin.Hide()
            self.panel_signup.Show()
        elif name == 'bBack':
            self.panel_signin.Show()
            self.panel_signup.Hide()
        elif name == 'bLogout':
            self.op_logout()
            self.panel_signin.Show()
            self.panel_left_2.Hide()
        elif name == 'bForgetPwd':
            self.panel_signin.Hide()

            self.panel_passwd.Show()
        elif name == 'bGetCode':
            self.op_get_code()
        elif name == 'bResetPwd':
            if self.op_reset_passwd():
                self.panel_signin.Show()
                self.panel_passwd.Hide()
        elif name == 'bBack_4':
            self.panel_signin.Show()
            self.panel_passwd.Hide()

    def op_calc1(self):
        #import pdb;pdb.set_trace()
        url = URL_PREFIX + '/service?service=calc1&arg1=%s&arg2=%s&email=%s&token=%s'
        url = url % (self.param1.GetValue(),self.param2.GetValue(),email_g,TOKEN)
        #print url
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
        self.statusbar.SetStatusText(msg, 0)

    def op_calc2(self):
        url = URL_PREFIX + '/service?service=calc2&arg1=%s&arg2=%s&email=%s&token=%s'
        url = url % (self.param3.GetValue(),self.param4.GetValue(),email_g,TOKEN)
        #print url
        response = requests.get(url).json()
        #import pdb;pdb.set_trace()
        #print self.param1.GetValue() + self.param2.GetValue()
        msg = response.get('msg')
        data = response.get('data')

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
        #self.statusbar.SetStatusText(msg, 0)
        #print response
        if flag:
            email_g = str(response.get('data').get('email'))
            TOKEN = str(response.get('data').get('token'))
            return True
        else:
            return False

    #注册
    def op_signup(self):
    	import pdb;pdb.set_trace()
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
        if not email:
            self.statusbar.SetStatusText(u'邮箱不能为空！', 0)
            return False
        code = self.reset_code.GetValue()
        if not code:
            self.statusbar.SetStatusText(u'验证码不能为空！', 0)
            return False
        newpasswd = self.newpasswd.GetValue()
        if not newpasswd:
            self.statusbar.SetStatusText(u'请填写新密码！', 0)
            return False
        newpasswd = hashlib.md5(PWD_PREFIX + newpasswd).hexdigest()
        url = url % (email, code, newpasswd)
        response = requests.get(url).json()

        msg = response.get('msg')
        flag = response.get('code')
        self.statusbar.SetStatusText(msg, 0)
        if flag:
            self.passwd_signin.SetValue('')
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

    def init_login_frame(self):
        
        self.login_frame = wx.Frame(None, wx.ID_ANY, title=u'用户登录', size=(350,200),
            style=wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CAPTION)
        
        # panel_signup
        self.panel_signup = wx.Panel(self.login_frame, wx.ID_ANY, size=(350,200), pos=(0,0))

        wx.StaticText(self.panel_signup, -1, u'手机号', pos=(20,20), size=wx.DefaultSize, style=0)
        self.phone = wx.TextCtrl(self.panel_signup, -1, pos=(85,20), size=wx.DefaultSize, style=0, name="uout1")
        
        wx.StaticText(self.panel_signup, -1, u'邮箱', pos=(20,60), size=wx.DefaultSize, style=0)
        self.email = wx.TextCtrl(self.panel_signup, -1, pos=(85,60), size=wx.DefaultSize)

        wx.StaticText(self.panel_signup, -1, u'密码：', pos=(20,100), size=wx.DefaultSize, style=0)
        self.passwd = wx.TextCtrl(self.panel_signup, -1, pos=(85,100), size=wx.DefaultSize, style=wx.TE_PASSWORD)

        bSignup = wx.Button(self.panel_signup, -1, u"提交注册", pos=(220,20), size=(80,30), name='bSignup')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bSignup)

        bBack = wx.Button(self.panel_signup, -1, u"返回登录", pos=(220,60), size=(80,30), name='bBack')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bBack)
        
        # self.panel_signin
        self.panel_signin = wx.Panel(self.login_frame, wx.ID_ANY, size=(350,200), pos=(0,0))
        wx.StaticText(self.panel_signin, -1, u'账号：', pos=(20,20), size=wx.DefaultSize, style=0)
        self.email_signin = wx.TextCtrl(self.panel_signin, -1, pos=(85,20), size=wx.DefaultSize, style=0)

        wx.StaticText(self.panel_signin, -1, u'密码：', pos=(20,60), size=wx.DefaultSize, style=0)
        self.passwd_signin = wx.TextCtrl(self.panel_signin, -1, pos=(85,60), size=wx.DefaultSize, style=wx.TE_PASSWORD)

        bNewUser = wx.Button(self.panel_signin, -1, u"用户注册", pos=(220,20), size=(80,30), name='bNewUser')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bNewUser)

        bUserCharge = wx.Button(self.panel_signin, -1, u"用户充值", pos=(220,60), size=(80,30), name='bUserCharge')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bUserCharge)

        bForgetPwd = wx.Button(self.panel_signin, -1, u"忘记密码", pos=(220,100), size=(80,30), name='bForgetPwd')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bForgetPwd)
        
        bSignin = wx.Button(self.panel_signin, -1, u"登录", pos=(50,100), size=wx.DefaultSize, name='bSignin')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bSignin)
        
        # panel_passwd
        self.panel_passwd = wx.Panel(self.login_frame, wx.ID_ANY, size=(350,200), pos=(0,0))
        wx.StaticText(self.panel_passwd, -1, u'账号：', pos=(20,20), size=wx.DefaultSize, style=0)
        self.email_resetpwd = wx.TextCtrl(self.panel_passwd, -1, pos=(85,20), size=wx.DefaultSize, style=0)

        wx.StaticText(self.panel_passwd, -1, u'新密码：', pos=(20,60), size=wx.DefaultSize, style=0)
        self.newpasswd = wx.TextCtrl(self.panel_passwd, -1, pos=(85,60), size=wx.DefaultSize, style=0)

        wx.StaticText(self.panel_passwd, -1, u'验证码：', pos=(20,100), size=wx.DefaultSize, style=0)
        self.reset_code = wx.TextCtrl(self.panel_passwd, -1, pos=(85,100), size=wx.DefaultSize, style=0)

        bGetCode = wx.Button(self.panel_passwd, -1, u"获取验证码", pos=(220,100), size=(80,30), name='bGetCode')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bGetCode)

        bResetPwd = wx.Button(self.panel_passwd, -1, u"重置密码", pos=(220,20), size=(80,30), name='bResetPwd')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bResetPwd)

        bBack_4 = wx.Button(self.panel_passwd, -1, u"返回登录", pos=(220,60), size=(80,30), name='bBack_4')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bBack_4)
        
        self.panel_signin.SetBackgroundColour((211,244,254))
        self.panel_passwd.SetBackgroundColour((211,244,254))
        self.panel_signup.SetBackgroundColour((211,244,254))
        self.panel_signin.Show()
        self.panel_passwd.Hide()
        self.panel_signup.Hide()
    
    def init_app_frame(self):
    	self.app_frame = wx.Frame(None, wx.ID_ANY, title=u'风暴眼v0.1', style=wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CAPTION|wx.RESIZE_BORDER)
        w, h = wx.DisplaySize()
        self.w = w = 1500
        self.h = h = 900
        line_px = 0
        line_py = 0
        line_sx = 1
        line_sy = h

        # menu
        # 一级菜单
        menubar = wx.MenuBar()
        file = wx.Menu()
        function = wx.Menu()
        information = wx.Menu()
        help = wx.Menu()

        # 二级菜单
        wx.ID_KJYC = 201
        wx.ID_CJZZ = 301
        wx.ID_CJRL = 302
        wx.ID_GY = 401
        wx.ID_LXWM = 402
        wx.ID_ZXGX = 403

        file.Append(wx.ID_ABOUT, u"&登录", u"登录")
        file.AppendSeparator()
        file.Append(wx.ID_EXIT, u"&退出", u"退出")
        file.AppendSeparator()
        function.Append(wx.ID_KJYC, u"&空间预测", u"空间预测")
        information.Append(wx.ID_CJZZ, u"&财经主站", u"财经主站")
        information.Append(wx.ID_CJRL, u"&财经日历", u"财经日历")
        help.Append(wx.ID_GY, u"&关于", u"关于")
        help.Append(wx.ID_LXWM, u"&联系我们", u"联系我们")
        help.Append(wx.ID_ZXGX, u"&在线更新", u"在线更新")

        menubar.Append( file, u'&系统' )
        menubar.Append( function, u'&功能' )
        menubar.Append( information, u'&资讯' )
        menubar.Append( help, u'&帮助' )

        self.app_frame.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        self.app_frame.Bind(wx.EVT_MENU, self.OnKJYC, id=wx.ID_KJYC)
        self.app_frame.Bind(wx.EVT_MENU, self.OnCJZZ, id=wx.ID_CJZZ)
        self.app_frame.Bind(wx.EVT_MENU, self.OnCJRL, id=wx.ID_CJRL)
        self.app_frame.Bind(wx.EVT_MENU, self.OnGY, id=wx.ID_GY)
        self.app_frame.Bind(wx.EVT_MENU, self.OnLXWM, id=wx.ID_LXWM)
        self.app_frame.Bind(wx.EVT_MENU, self.OnZXGX, id=wx.ID_ZXGX)

        self.app_frame.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        # StatusBar
        self.statusbar = self.app_frame.CreateStatusBar()
        self.statusbar.SetFieldsCount(1)
        
        self.kjyc_panel = wx.Panel(self.app_frame, wx.ID_ANY, size=(w,h))

        font = wx.Font(10, wx.DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        right_base_x = 160
        tc_delta = 50

        # first row
        FIRST_H = 20
        wx.StaticText(self.kjyc_panel, -1, u'参数1', pos=(right_base_x+20,FIRST_H), size=wx.DefaultSize, style=0)
        wx.StaticText(self.kjyc_panel, -1, u'参数2', pos=(right_base_x+270,FIRST_H), size=wx.DefaultSize, style=0)
        self.param1 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+120,FIRST_H), size=wx.DefaultSize, style=0, name="param1")
        self.param2 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+320,FIRST_H), size=wx.DefaultSize, style=0, name="param2")
        bCalc1 = wx.Button(self.kjyc_panel, -1, u"计算", pos=(right_base_x+570,FIRST_H), size=wx.DefaultSize, name='bCalc1')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bCalc1)

        #second row
        SENCOND_H = 80
        t_out1 = wx.StaticText(self.kjyc_panel, -1, u'结果1', pos=(right_base_x,SENCOND_H), size=wx.DefaultSize, style=0)
        self.uout1 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta,SENCOND_H), size=wx.DefaultSize, style=0, name="uout1")
        t_out1.SetFont(font)

        t_out2 = wx.StaticText(self.kjyc_panel, -1, u'结果2', pos=(right_base_x+175,SENCOND_H), size=wx.DefaultSize, style=0)
        self.uout2 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+175,SENCOND_H), size=wx.DefaultSize, style=0, name="uout2")
        t_out2.SetFont(font)
        
        t_out3 = wx.StaticText(self.kjyc_panel, -1, u'结果3', pos=(right_base_x+350,SENCOND_H), size=wx.DefaultSize, style=0)
        self.uout3 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+350,SENCOND_H), size=wx.DefaultSize, style=0, name="uout3")
        t_out3.SetFont(font)

        t_out4 = wx.StaticText(self.kjyc_panel, -1, u'结果4', pos=(right_base_x+525,SENCOND_H), size=wx.DefaultSize, style=0)
        self.uout4 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+525,SENCOND_H), size=wx.DefaultSize, style=0, name="uout4")
        t_out4.SetFont(font)

        #third row
        THIRD_H = 120
        t_out5 = wx.StaticText(self.kjyc_panel, -1, u'结果5', pos=(right_base_x,THIRD_H), size=wx.DefaultSize, style=0)
        self.uout5 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta,THIRD_H), size=wx.DefaultSize, style=0, name="uout5")
        t_out5.SetFont(font)
        
        t_out6 = wx.StaticText(self.kjyc_panel, -1, u'结果6', pos=(right_base_x+175,THIRD_H), size=wx.DefaultSize, style=0)
        self.uout6 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+175,THIRD_H), size=wx.DefaultSize, style=0, name="uout6")
        t_out6.SetFont(font)
        
        t_out7 = wx.StaticText(self.kjyc_panel, -1, u'结果7', pos=(right_base_x+350,THIRD_H), size=wx.DefaultSize, style=0)
        self.uout7 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+350,THIRD_H), size=wx.DefaultSize, style=0, name="uout7")
        t_out7.SetFont(font)

        t_out8 = wx.StaticText(self.kjyc_panel, -1, u'结果8', pos=(right_base_x+525,THIRD_H), size=wx.DefaultSize, style=0)
        self.uout8 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+525,THIRD_H), size=wx.DefaultSize, style=0, name="uout8")
        t_out8.SetFont(font)

        #forth row
        FORTH_H = 180
        wx.StaticText(self.kjyc_panel, -1, u'参数3', pos=(right_base_x+20,FORTH_H), size=wx.DefaultSize, style=0)
        wx.StaticText(self.kjyc_panel, -1, u'参数4', pos=(right_base_x+270,FORTH_H), size=wx.DefaultSize, style=0)
        self.param3 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+120,FORTH_H), size=wx.DefaultSize, style=0, name="param1")
        self.param4 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+320,FORTH_H), size=wx.DefaultSize, style=0, name="param2")
        
        bCalc2 = wx.Button(self.kjyc_panel, -1, u"计算", pos=(right_base_x+570,FORTH_H), size=wx.DefaultSize, name='bCalc2')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bCalc2)

        #fifth row
        FIFTH_H =240
        d_out1 = wx.StaticText(self.kjyc_panel, -1, u'结果1', pos=(right_base_x,FIFTH_H), size=wx.DefaultSize, style=0)
        self.dout1 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta,FIFTH_H), size=wx.DefaultSize, style=0, name="dout1")
        d_out1.SetFont(font)

        d_out2 = wx.StaticText(self.kjyc_panel, -1, u'结果2', pos=(right_base_x+175,FIFTH_H), size=wx.DefaultSize, style=0)
        self.dout2 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+175,FIFTH_H), size=wx.DefaultSize, style=0, name="dout2")
        d_out2.SetFont(font)

        d_out3 = wx.StaticText(self.kjyc_panel, -1, u'结果3', pos=(right_base_x+350,FIFTH_H), size=wx.DefaultSize, style=0)
        self.dout3 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+350,FIFTH_H), size=wx.DefaultSize, style=0, name="dout3")
        d_out3.SetFont(font)

        d_out4 = wx.StaticText(self.kjyc_panel, -1, u'结果4', pos=(right_base_x+525,FIFTH_H), size=wx.DefaultSize, style=0)
        self.dout4 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+525,FIFTH_H), size=wx.DefaultSize, style=0, name="dout4")
        d_out4.SetFont(font)

        #sixth row
        SIXTH_H = 280
        d_out5 = wx.StaticText(self.kjyc_panel, -1, u'结果5', pos=(right_base_x,SIXTH_H), size=wx.DefaultSize, style=0)
        self.dout5 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta,SIXTH_H), size=wx.DefaultSize, style=0, name="dout5")
        d_out5.SetFont(font)

        d_out6 = wx.StaticText(self.kjyc_panel, -1, u'结果6', pos=(right_base_x+175,SIXTH_H), size=wx.DefaultSize, style=0)
        self.dout6 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+175,SIXTH_H), size=wx.DefaultSize, style=0, name="dout6")
        d_out6.SetFont(font)

        d_out7 = wx.StaticText(self.kjyc_panel, -1, u'结果7', pos=(right_base_x+350,SIXTH_H), size=wx.DefaultSize, style=0)
        self.dout7 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+350,SIXTH_H), size=wx.DefaultSize, style=0, name="dout7")
        d_out7.SetFont(font)

        d_out8 = wx.StaticText(self.kjyc_panel, -1, u'结果8', pos=(right_base_x+525,SIXTH_H), size=wx.DefaultSize, style=0)
        self.dout8 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+tc_delta+525,SIXTH_H), size=wx.DefaultSize, style=0, name="dout8")
        d_out8.SetFont(font)

        self.kjyc_panel.SetBackgroundColour((211,244,254))
        self.kjyc_panel.Hide()

        self.app_frame.SetMenuBar( menubar )
        self.app_frame.SetSize( wx.Size( w/1.5,h/1.5 ))

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()