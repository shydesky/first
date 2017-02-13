#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import webbrowser
import requests
import wx
import hashlib
import json
import re
import datetime, time
from wx.lib.wordwrap import wordwrap
sys.path.append("libs")
URL_PREFIX = 'http://www.thestormeye.com:5000'
PWD_PREFIX = 'MDF'

def get_user_token():
    from bios_util import get_disk_info
    return get_disk_info()
TOKEN = get_user_token()

info_gywm_g = u'风暴眼外汇计算工具\n著作人:王岩，联合出品人:黄伟\n更多详细信息请登录www.thestormeye.com'
info_lxwm_g = 'email: hag_kane@sina.com'
last_getcode_time = None
def init_information():
    global info_gywm_g, info_lxwm_g
    url = URL_PREFIX + '/service?service=information'
    #print url
    response = requests.get(url).json()

    msg = response.get('msg')
    data = response.get('data')
    info_gywm_g = data.get('gywo')
    info_lxwm_g = data.get('lxwm')

account_g = ''

class MyApp(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.init_login_frame()
        self.login_frame.Centre()
        self.login_frame.Show()
        
    def OnQuit(self, event):
        self.login_frame.Destroy()
        self.app_frame.Destroy()

    def OnCharge(self, event):
        self.init_login_frame()
        self.login_frame.Centre()
        self.login_frame.Show()
        self.app_frame.Hide()
    def OnMenu(self, event):
        # import pdb;pdb.set_trace()
        print event.GetEventObject().GetId()

    def OnKJYC(self, event): # 空间预测
        self.kjyc_panel.SetBackgroundColour((211,244,254))
        self.kjyc_panel.SetSize(wx.Size(self.w,self.h))
        self.init_panel.Hide()
        self.kjyc_panel.Show()

    def OnCJRL(self, event): # 财经日历
        url = 'http://vip.stock.finance.sina.com.cn/forex/view/vDailyFX_More.php'
        webbrowser.open(url)

    def OnCJZZ(self, event): # 财经主站 
        if event.GetId() == wx.ID_CJZZ_ZGCJ:
            url = 'http://finance.fecn.net/'
        elif event.GetId() == wx.ID_CJZZ_DFCF:
            url = ' http://forex.eastmoney.com/'
        elif event.GetId() == wx.ID_CJZZ_XLCJ:
            url = 'http://finance.sina.com.cn/forex/'
        elif event.GetId() == wx.ID_CJZZ_SHCJ:
            url = 'http://money.sohu.com/waihui/'
        webbrowser.open(url)

    def OnGY(self, event):  # 关于
        dlg = wx.MessageDialog(parent=None, message=info_gywm_g, caption=u"关于我们", style=wx.OK)
        dlg.ShowModal()

    def OnLXWM(self, event): # 联系我们
        dlg = wx.MessageDialog(parent=None, message=info_lxwm_g, caption=u"联系我们", style=wx.OK)
        dlg.ShowModal()

    def OnZXGX(self, event): # 在线更新
        url = URL_PREFIX + '/download'
        webbrowser.open(url)

    def EvtCheckBox(self,event):
        self.showsrvfile()

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
        elif name == 'bSignin' or name == 'text': #用户登入panel
            if self.op_signin():
                self.init_app_frame()
                self.login_frame.Hide()
                self.app_frame.Show()

        elif name == 'bNewUser':
            self.panel_signin.Hide()
            self.panel_signup.Show()
            self.statusbar_login.SetStatusText('', 0)
        elif name == 'bBack':
            self.panel_signin.Show()
            self.panel_signup.Hide()
            self.statusbar_login.SetStatusText('', 0)
        elif name == 'bLogout':
            self.op_logout()
            self.panel_signin.Show()
            self.panel_left_2.Hide()
        elif name == 'bForgetPwd':
            self.panel_signin.Hide()
            self.panel_passwd.Show()
            self.statusbar_login.SetStatusText('', 0)
        elif name == 'bGetCode':
            self.op_get_code()
        elif name == 'bGetCode_signup':
            self.op_get_code_signup()
        elif name == 'bResetPwd':
            if self.op_reset_passwd():
                self.panel_signin.Show()
                self.panel_passwd.Hide()
                self.statusbar_login.SetStatusText('', 0)
        elif name == 'bBack_4':
            self.panel_signin.Show()
            self.panel_passwd.Hide()
            self.statusbar_login.SetStatusText('', 0)
        elif name == 'bBack_charge':
            self.panel_signin.Show()
            self.panel_charge.Hide()
            self.statusbar_login.SetStatusText('', 0)
        elif name == 'bUserCharge':
            self.panel_signin.Hide()
            self.panel_charge.Show()
            self.statusbar_login.SetStatusText('', 0)
        elif name == 'bCharge':
            self.op_charge()
        elif name == 'bBuyCard':
            self.op_buycard()
        elif name == 'bSrvfile':
            self.showsrvfile()

    def showsrvfile(self): # 服务协议
        url = URL_PREFIX + '/file/servicefile'
        webbrowser.open(url)

    def op_calc1(self):
        #import pdb;pdb.set_trace()
        url = URL_PREFIX + '/service?service=calc1&arg1=%s&arg2=%s&account=%s&key=%s'
        url = url % (self.param1.GetValue(),self.param2.GetValue(),account_g,TOKEN)
        #print url
        response = requests.get(url).json()
        #import pdb;pdb.set_trace()
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
        url = URL_PREFIX + '/service?service=calc2&arg1=%s&arg2=%s&account=%s&key=%s'
        url = url % (self.param3.GetValue(),self.param4.GetValue(),account_g,TOKEN)
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
        global account_g , TOKEN
        import re
        p2 = re.compile('^1[358]\d{9}$|^147\d{8}')
        phone = self.phone_signin.GetValue()
        if not p2.match(phone):
            msg = u'请输入有效的手机号!'
            self.statusbar_login.SetStatusText(msg, 0)
            return False
        passwd = hashlib.md5(PWD_PREFIX + self.passwd_signin.GetValue()).hexdigest()
        url = URL_PREFIX + '/service?service=user&function=signin&account=%s&passwd=%s&key=%s'
        url = url % (phone,passwd,TOKEN)
        response = requests.get(url).json()
        msg = response.get('msg')
        self.statusbar_login.SetStatusText(msg, 0)
        can_signin = int(response.get('data').get('can_signin'))

        if can_signin == 1:
            account_g = str(response.get('data').get('account'))
            validtime = str(response.get('data').get('validtime'))
            tryuse_time = str(response.get('data').get('tryuse_time'))
            usertype = int(response.get('data').get('usertype'))
            can_use = int(response.get('data').get('can_use'))

            if usertype == 0:
                if can_use:
                    message = u'亲爱的用户,感谢您使用风暴眼科技外汇计算工具进行体验。\n体验期为10天,有效期至'\
                    + tryuse_time + u',祝您使用愉快。'
                else:
                    message = u'亲爱的用户,感谢您使用风暴眼科技外汇计算工具进行体验。\n您的体验期已结束,为了不影响您的使用,请及时充值。'
            elif usertype == 1:
                if can_use:
                    message = u'尊敬的用户,感谢您使用风暴眼科技外汇计算器工具。\n您当前的使用有效期至'\
                    + validtime + u',如您想在服务到期之后继续使用,请及时充值。'
                else:
                    message = u'尊敬的用户,感谢您使用风暴眼科技外汇计算器工具。\n您当前的使用有效期至'\
                    + validtime + u',为了不影响您的使用,请及时充值。'
            
            dlg = wx.MessageDialog(parent=None, message=message, caption=u'温馨提示', style=wx.OK)
            dlg.ShowModal()
            self.statusbar_login.SetStatusText(msg, 0)
            return True
        elif can_signin == 0:
            self.statusbar_login.SetStatusText(msg, 0)
            return False

    #注册
    def op_signup(self):
        global TOKEN
        phone = self.phone_signup.GetValue()
        p_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        phonematch=p_re.match(phone)
        if not phonematch:
            self.statusbar_login.SetStatusText(u'手机号码无效！', 0)
            return

        email = self.email.GetValue()
        e_re = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")
        emailmatch=e_re.match(email)
        if not emailmatch:
            self.statusbar_login.SetStatusText(u'邮箱格式无效！', 0)
            return
        agree = self.checkSrvFile.GetValue()
        if not agree:
        	self.statusbar_login.SetStatusText(u'请阅读并同意服务协议！', 0)
        	return
        passwd = hashlib.md5(PWD_PREFIX + self.passwd.GetValue()).hexdigest()
        verifycode = self.signup_code.GetValue()

        url = URL_PREFIX + '/service?service=user&function=signup&email=%s&passwd=%s&phone=%s&key=%s&code=%s'
        url = url % (email, passwd, phone, TOKEN, verifycode)
        response = requests.get(url).json()
        
        msg = response.get('msg')
        code = response.get('code')
        if code:
            self.phone_signup.SetValue('')
            self.email.SetValue('')
            self.checkSrvFile.SetValue(0)
            self.signup_code.SetValue('')
            self.passwd.SetValue('')
        self.statusbar_login.SetStatusText(msg, 0)

    #退出
    def op_logout(self):
        global account_g , TOKEN
        account_g = ''
        TOKEN = ''
        self.passwd_signin.SetValue('') 
        self.statusbar.SetStatusText(u'您已成功退出', 0)

    def op_reset_passwd(self):
        url = URL_PREFIX + '/service?service=user&function=resetpwd&phone=%s&verifycode=%s&passwd=%s'
        phone = self.phone_resetpwd.GetValue()
        if not phone:
            self.statusbar_login.SetStatusText(u'邮箱不能为空！', 0)
            return False
        code = self.reset_code.GetValue()
        if not code:
            self.statusbar_login.SetStatusText(u'验证码不能为空！', 0)
            return False
        newpasswd = self.newpasswd.GetValue()
        if not newpasswd:
            self.statusbar_login.SetStatusText(u'请填写新密码！', 0)
            return False
        newpasswd = hashlib.md5(PWD_PREFIX + newpasswd).hexdigest()
        url = url % (phone, code, newpasswd)
        response = requests.get(url).json()

        msg = response.get('msg')
        flag = response.get('code')
        self.statusbar_login.SetStatusText(msg, 0)
        if flag:
            self.passwd_signin.SetValue('')
            return True
        else:
            return False

    def op_get_code(self):
        global last_getcode_time
        time_now = time.time()
        if last_getcode_time != None:
            if time_now - last_getcode_time < 70:
                self.statusbar_login.SetStatusText(u'验证码已发送,如未收到,请1分钟后再试', 0)
                return
        url = URL_PREFIX + '/service?service=user&function=getcode&phone=%s&type=1'
        phone = self.phone_resetpwd.GetValue()
        url = url % (phone)
        response = requests.get(url).json()
        msg = response.get('msg')
        last_getcode_time = time_now
        self.statusbar_login.SetStatusText(msg, 0)
    
    def op_get_code_signup(self):
        global last_getcode_time
        time_now = time.time()
        if last_getcode_time != None:
            if time_now - last_getcode_time < 70:
                self.statusbar_login.SetStatusText(u'验证码已发送,如未收到,请1分钟后再试', 0)
                return
        url = URL_PREFIX + '/service?service=user&function=getcode&phone=%s&type=2'
        phone = self.phone_signup.GetValue()
        p_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        phonematch=p_re.match(phone)
        if not phonematch:
            self.statusbar_login.SetStatusText(u'手机号码无效！', 0)
            return
        url = url % (phone)
        response = requests.get(url).json()
        msg = response.get('msg')
        last_getcode_time = time_now
        self.statusbar_login.SetStatusText(msg, 0)

    def op_charge(self):
        url = URL_PREFIX + '/service?service=user&function=usercharge&account=%s&cardnum=%s&cardpwd=%s'
        account = self.account.GetValue()
        cardnum =  self.cardnum.GetValue()
        cardpwd =  self.cardpwd.GetValue()
        url = url % (account, cardnum, cardpwd)
        response = requests.get(url).json()
        msg = response.get('msg')
        self.account.SetValue('')
        self.cardnum.SetValue('')
        self.cardpwd.SetValue('')
        self.statusbar_login.SetStatusText(msg, 0)

    def op_buycard(self):
        url = 'http://web10002066.sa.17uhui.com.cn/?page_id=2'
        webbrowser.open(url)

    def init_login_frame(self):
        
        self.login_frame = wx.Frame(None, wx.ID_ANY, title=u'风暴眼科技--用户登录', size=(350,200),
            style=wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CAPTION)
        self.statusbar_login = self.login_frame.CreateStatusBar()
        self.statusbar_login.SetFieldsCount(1)
        # panel_signup
        self.panel_signup = wx.Panel(self.login_frame, wx.ID_ANY, size=(350,200), pos=(0,0))

        wx.StaticText(self.panel_signup, -1, u'手机', pos=(15,10), size=wx.DefaultSize, style=0)
        self.phone_signup = wx.TextCtrl(self.panel_signup, -1, pos=(60,10), size=(100, 25), style=0, name="uout1")
        
        wx.StaticText(self.panel_signup, -1, u'邮箱', pos=(175,10), size=wx.DefaultSize, style=0)
        self.email = wx.TextCtrl(self.panel_signup, -1, pos=(225,10), size=(100, 25))

        wx.StaticText(self.panel_signup, -1, u'密码', pos=(15,40), size=wx.DefaultSize, style=0)
        self.passwd = wx.TextCtrl(self.panel_signup, -1, pos=(60,40), size=(100, 25), style=wx.TE_PASSWORD)

        wx.StaticText(self.panel_signup, -1, u"验证码", pos=(175,40), size=wx.DefaultSize, name='sendCode_signup')
        self.signup_code = wx.TextCtrl(self.panel_signup, -1, pos=(225,40), size=(100, 25), style=0)
        
        self.checkSrvFile = wx.CheckBox(self.panel_signup,-1, u'我同意服务协议', pos=(20,75), size=(140,20))
        #bSrvfile = wx.Button(self.panel_signup, -1, u"查看服务协议", pos=(225,75), size=(80,25), name='bSrvfile', style=1)
        #self.Bind(wx.EVT_BUTTON, self.OnButton, bSrvfile)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.checkSrvFile)

        bGetCode_signup = wx.Button(self.panel_signup, -1, u"获取验证码", pos=(20,105), size=(80,25), name='bGetCode_signup')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bGetCode_signup)

        bSignup = wx.Button(self.panel_signup, -1, u"提交注册", pos=(130,105), size=(80,25), name='bSignup')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bSignup)

        bBack = wx.Button(self.panel_signup, -1, u"返回登录", pos=(240,105), size=(80,25), name='bBack')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bBack)
        
        # self.panel_signin
        self.panel_signin = wx.Panel(self.login_frame, wx.ID_ANY, size=(350,200), pos=(0,0))
        wx.StaticText(self.panel_signin, -1, u'账号：', pos=(20,20), size=wx.DefaultSize, style=0)
        self.phone_signin = wx.TextCtrl(self.panel_signin, -1, u'手机号', pos=(85,20), size=wx.DefaultSize, style=0)
        self.phone_signin.Bind(wx.EVT_LEFT_DOWN, self.onSetFocus)
        self.phone_signin.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)

        wx.StaticText(self.panel_signin, -1, u'密码：', pos=(20,60), size=wx.DefaultSize, style=0)
        self.passwd_signin = wx.TextCtrl(self.panel_signin, -1, pos=(85,60), size=wx.DefaultSize, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)

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
        self.phone_resetpwd = wx.TextCtrl(self.panel_passwd, -1, pos=(85,20), size=wx.DefaultSize, style=0)

        wx.StaticText(self.panel_passwd, -1, u'新密码：', pos=(20,60), size=wx.DefaultSize, style=0)
        self.newpasswd = wx.TextCtrl(self.panel_passwd, -1, pos=(85,60), size=wx.DefaultSize, style=wx.TE_PASSWORD)

        wx.StaticText(self.panel_passwd, -1, u'验证码：', pos=(20,100), size=wx.DefaultSize, style=0)
        self.reset_code = wx.TextCtrl(self.panel_passwd, -1, pos=(85,100), size=wx.DefaultSize, style=0)

        bGetCode = wx.Button(self.panel_passwd, -1, u"获取验证码", pos=(220,100), size=(80,30), name='bGetCode')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bGetCode)

        bResetPwd = wx.Button(self.panel_passwd, -1, u"重置密码", pos=(220,20), size=(80,30), name='bResetPwd')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bResetPwd)

        bBack_4 = wx.Button(self.panel_passwd, -1, u"返回登录", pos=(220,60), size=(80,30), name='bBack_4')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bBack_4)
        
        # panel_charge
        self.panel_charge = wx.Panel(self.login_frame, wx.ID_ANY, size=(350,200), pos=(0,0))
        wx.StaticText(self.panel_charge, -1, u'账号:', pos=(20,20), size=wx.DefaultSize, style=0)
        self.account = wx.TextCtrl(self.panel_charge, -1, pos=(85,20), size=wx.DefaultSize, style=0)
        wx.StaticText(self.panel_charge, -1, u'充值卡号:', pos=(20,60), size=wx.DefaultSize, style=0)
        self.cardnum = wx.TextCtrl(self.panel_charge, -1, pos=(85,60), size=wx.DefaultSize, style=0)
        wx.StaticText(self.panel_charge, -1, u'充值密码:', pos=(20,100), size=wx.DefaultSize, style=0)
        self.cardpwd = wx.TextCtrl(self.panel_charge, -1, pos=(85,100), size=wx.DefaultSize, style=wx.TE_PASSWORD)
        bCharge = wx.Button(self.panel_charge, -1, u"充值", pos=(220,20), size=(80,30), name='bCharge')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bCharge)
       
        bBuyCard = wx.Button(self.panel_charge, -1, u"购买充值卡", pos=(220,60), size=(80,30), name='bBuyCard')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bBuyCard)

        bBack_charge = wx.Button(self.panel_charge, -1, u"返回登录", pos=(220,100), size=(80,30), name='bBack_charge')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bBack_charge)
        
        self.Bind(wx.EVT_TEXT_ENTER, self.OnButton)
        self.panel_signin.SetBackgroundColour((211,244,254))
        self.panel_passwd.SetBackgroundColour((211,244,254))
        self.panel_signup.SetBackgroundColour((211,244,254))
        self.panel_charge.SetBackgroundColour((211,244,254))
        self.panel_signin.Show()
        self.panel_passwd.Hide()
        self.panel_signup.Hide()
        self.panel_charge.Hide()

        def OnKeyEnterDown(self, event):
            wx.PostEvent(self,wx.CommandEvent(wx.EVT_BUTTON.typeId, bSignin.GetId()))

    def onKillFocus(self, event):
        event.Skip()

    def onSetFocus(self, event):
        if self.phone_signin.GetValue() == u'手机号':
            self.phone_signin.SetValue('')
        event.Skip()

    def init_app_frame(self):
        self.app_frame = wx.Frame(None, wx.ID_ANY, title=u'风暴眼v0.1', style=wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CAPTION|wx.RESIZE_BORDER)
        self.w = w = 1000
        self.h = h = 600
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
        information_second_menu = wx.Menu()
        wx.ID_CHARGE = 101
        wx.ID_KJYC = 201
        wx.ID_CJZZ = 301
        wx.ID_CJRL = 302
        wx.ID_GY = 401
        wx.ID_LXWM = 402
        wx.ID_ZXGX = 403
        # 三级菜单
        wx.ID_CJZZ_ZGCJ = 3011
        wx.ID_CJZZ_DFCF = 3012
        wx.ID_CJZZ_XLCJ = 3013
        wx.ID_CJZZ_SHCJ = 3014

        information_item_one = wx.MenuItem(information_second_menu, 3011, text=u'中国财经网',kind=wx.ITEM_NORMAL)
        information_item_two = wx.MenuItem(information_second_menu, 3012, text=u'东方财富网',kind=wx.ITEM_NORMAL)
        information_item_three = wx.MenuItem(information_second_menu, 3013, text=u'新浪财经',kind=wx.ITEM_NORMAL)
        information_item_four = wx.MenuItem(information_second_menu, 3014, text=u'搜狐财经',kind=wx.ITEM_NORMAL)

        information_second_menu.AppendItem(information_item_one)
        information_second_menu.AppendItem(information_item_two)
        information_second_menu.AppendItem(information_item_three)
        information_second_menu.AppendItem(information_item_four)    
        file.Append(wx.ID_CHARGE, u"&充值", u"充值")
        file.AppendSeparator()
        file.Append(wx.ID_EXIT, u"&退出", u"退出")
        file.AppendSeparator()
        function.Append(wx.ID_KJYC, u"&空间预测", u"空间预测")
        information.AppendMenu(wx.ID_CJZZ, u"&财经主站", information_second_menu)
        information.Append(wx.ID_CJRL, u"&财经日历", u"财经日历")
        help.Append(wx.ID_GY, u"&关于", u"关于")
        help.Append(wx.ID_LXWM, u"&联系我们", u"联系我们")
        help.Append(wx.ID_ZXGX, u"&在线更新", u"在线更新")

        menubar.Append( file, u'&系统' )
        menubar.Append( function, u'&功能' )
        menubar.Append( information, u'&资讯' )
        menubar.Append( help, u'&帮助' )

        self.app_frame.Bind(wx.EVT_MENU, self.OnCharge, id=wx.ID_CHARGE)
        self.app_frame.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
        self.app_frame.Bind(wx.EVT_MENU, self.OnKJYC, id=wx.ID_KJYC)
        self.app_frame.Bind(wx.EVT_MENU, self.OnCJZZ, id=wx.ID_CJZZ_ZGCJ)
        self.app_frame.Bind(wx.EVT_MENU, self.OnCJZZ, id=wx.ID_CJZZ_SHCJ)
        self.app_frame.Bind(wx.EVT_MENU, self.OnCJZZ, id=wx.ID_CJZZ_XLCJ)
        self.app_frame.Bind(wx.EVT_MENU, self.OnCJZZ, id=wx.ID_CJZZ_DFCF)
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
        right_base_x = 200
        tc_delta = 50
        t_out0 = wx.StaticText(self.kjyc_panel, -1, u'上涨计算', pos=(40,35), size=wx.DefaultSize, style=0)
        t_out0.SetFont(font)
        # first row
        FIRST_H = tc_delta + 20
        
        wx.StaticText(self.kjyc_panel, -1, u'L', pos=(40,FIRST_H), size=wx.DefaultSize, style=0)
        wx.StaticText(self.kjyc_panel, -1, u'H', pos=(100,FIRST_H), size=wx.DefaultSize, style=0)
        t_out1 = wx.StaticText(self.kjyc_panel, -1, u'结果1', pos=(right_base_x,FIRST_H), size=wx.DefaultSize, style=0)
        t_out2 = wx.StaticText(self.kjyc_panel, -1, u'结果2', pos=(right_base_x+175,FIRST_H), size=wx.DefaultSize, style=0)
        t_out3 = wx.StaticText(self.kjyc_panel, -1, u'结果3', pos=(right_base_x+350,FIRST_H), size=wx.DefaultSize, style=0)
        t_out4 = wx.StaticText(self.kjyc_panel, -1, u'结果4', pos=(right_base_x+525,FIRST_H), size=wx.DefaultSize, style=0)
        t_out1.SetFont(font)
        t_out2.SetFont(font)
        t_out3.SetFont(font)
        t_out4.SetFont(font)
        
        #second row
        SENCOND_H = tc_delta + 50

        self.param1 = wx.TextCtrl(self.kjyc_panel, -1, pos=(20,SENCOND_H), size=(50,20), style=0, name="param1")
        self.param2 = wx.TextCtrl(self.kjyc_panel, -1, pos=(80,SENCOND_H), size=(50,20), style=0, name="param2")
        
        self.uout1 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x,SENCOND_H), size=wx.DefaultSize, style=0, name="uout1")
        self.uout2 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+175,SENCOND_H), size=wx.DefaultSize, style=0, name="uout2")
        self.uout3 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+350,SENCOND_H), size=wx.DefaultSize, style=0, name="uout3")
        self.uout4 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+525,SENCOND_H), size=wx.DefaultSize, style=0, name="uout4")

        #third row
        THIRD_H = tc_delta + 90
        bCalc1 = wx.Button(self.kjyc_panel, -1, u"计算", pos=(35,THIRD_H), size=wx.DefaultSize, name='bCalc1')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bCalc1)
        t_out5 = wx.StaticText(self.kjyc_panel, -1, u'结果5', pos=(right_base_x,THIRD_H), size=wx.DefaultSize, style=0)
        t_out6 = wx.StaticText(self.kjyc_panel, -1, u'结果6', pos=(right_base_x+175,THIRD_H), size=wx.DefaultSize, style=0)
        t_out7 = wx.StaticText(self.kjyc_panel, -1, u'结果7', pos=(right_base_x+350,THIRD_H), size=wx.DefaultSize, style=0)
        t_out8 = wx.StaticText(self.kjyc_panel, -1, u'结果8', pos=(right_base_x+525,THIRD_H), size=wx.DefaultSize, style=0)
        t_out5.SetFont(font)
        t_out6.SetFont(font)
        t_out7.SetFont(font)
        t_out8.SetFont(font)
        
        #forth row
        FORTH_H = tc_delta + 130
        self.uout5 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x,FORTH_H), size=wx.DefaultSize, style=0, name="uout5")
        self.uout6 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+175,FORTH_H), size=wx.DefaultSize, style=0, name="uout6")
        self.uout7 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+350,FORTH_H), size=wx.DefaultSize, style=0, name="uout7")
        self.uout8 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+525,FORTH_H), size=wx.DefaultSize, style=0, name="uout8")
        

        
        wx.StaticLine(self.kjyc_panel, -1, (0, FORTH_H+60), (1000, 1))
        #fifth row
        d_out0 = wx.StaticText(self.kjyc_panel, -1, u'下跌计算', pos=(40,295), size=wx.DefaultSize, style=0)
        d_out0.SetFont(font)
        FIFTH_H = tc_delta + 280
        wx.StaticText(self.kjyc_panel, -1, u'L', pos=(40,FIFTH_H), size=(50,20), style=0)
        wx.StaticText(self.kjyc_panel, -1, u'H', pos=(100,FIFTH_H), size=(50,20), style=0)
        
        d_out1 = wx.StaticText(self.kjyc_panel, -1, u'结果1', pos=(right_base_x,FIFTH_H), size=wx.DefaultSize, style=0)
        d_out2 = wx.StaticText(self.kjyc_panel, -1, u'结果2', pos=(right_base_x+175,FIFTH_H), size=wx.DefaultSize, style=0)
        d_out3 = wx.StaticText(self.kjyc_panel, -1, u'结果3', pos=(right_base_x+350,FIFTH_H), size=wx.DefaultSize, style=0)
        d_out4 = wx.StaticText(self.kjyc_panel, -1, u'结果4', pos=(right_base_x+525,FIFTH_H), size=wx.DefaultSize, style=0)
        d_out1.SetFont(font)
        d_out2.SetFont(font)
        d_out3.SetFont(font)
        d_out4.SetFont(font)
        
    
        #sixth row
        SIXTH_H = tc_delta + 310
        self.param3 = wx.TextCtrl(self.kjyc_panel, -1, pos=(20,SIXTH_H), size=(50,20), style=0, name="param1")
        self.param4 = wx.TextCtrl(self.kjyc_panel, -1, pos=(80,SIXTH_H), size=(50,20), style=0, name="param2")
        
        self.dout1 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x,SIXTH_H), size=wx.DefaultSize, style=0, name="dout1")
        self.dout2 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+175,SIXTH_H), size=wx.DefaultSize, style=0, name="dout2")
        self.dout3 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+350,SIXTH_H), size=wx.DefaultSize, style=0, name="dout3")
        self.dout4 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+525,SIXTH_H), size=wx.DefaultSize, style=0, name="dout4")
        
        #seventh row
        SEVENTH_H = tc_delta + 350
        bCalc2 = wx.Button(self.kjyc_panel, -1, u"计算", pos=(35,SEVENTH_H), size=wx.DefaultSize, name='bCalc2')
        self.Bind(wx.EVT_BUTTON, self.OnButton, bCalc2)
        d_out5 = wx.StaticText(self.kjyc_panel, -1, u'结果5', pos=(right_base_x,SEVENTH_H), size=wx.DefaultSize, style=0)
        d_out6 = wx.StaticText(self.kjyc_panel, -1, u'结果6', pos=(right_base_x+175,SEVENTH_H), size=wx.DefaultSize, style=0)
        d_out7 = wx.StaticText(self.kjyc_panel, -1, u'结果7', pos=(right_base_x+350,SEVENTH_H), size=wx.DefaultSize, style=0)
        d_out8 = wx.StaticText(self.kjyc_panel, -1, u'结果8', pos=(right_base_x+525,SEVENTH_H), size=wx.DefaultSize, style=0)
        d_out5.SetFont(font)
        d_out6.SetFont(font)
        d_out7.SetFont(font)
        d_out8.SetFont(font)

        #eighth row
        EIGHTH_H = tc_delta + 380
        self.dout5 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x,EIGHTH_H), size=wx.DefaultSize, style=0, name="dout5")
        self.dout6 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+175,EIGHTH_H), size=wx.DefaultSize, style=0, name="dout6")
        self.dout7 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+350,EIGHTH_H), size=wx.DefaultSize, style=0, name="dout7")
        self.dout8 = wx.TextCtrl(self.kjyc_panel, -1, pos=(right_base_x+525,EIGHTH_H), size=wx.DefaultSize, style=0, name="dout8")
        
        self.kjyc_panel.SetBackgroundColour((211,244,254))
        self.kjyc_panel.Hide()

        self.app_frame.SetMenuBar( menubar )
        self.app_frame.SetSize( wx.Size(w, h))
        self.app_frame.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.init_panel = wx.Panel(self.app_frame, wx.ID_ANY, size=(w,h))

        to_bmp_image = wx.Image(resource_path('resource\\bg.jpg'), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.init_panel.bitmap = wx.StaticBitmap(self.init_panel, -1, to_bmp_image, (0, 0))

def resource_path(relative_path):
    import os
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()