#!/usr/bin/python3
#-*-coding:utf-8-*-
# http://www.cnblogs.com/lao-wan/p/5111808.html

import tkinter
import smtplib
from email.mime.text import MIMEText
from configparser import ConfigParser
import os
import tkinter.filedialog
import re

class Window:
    def __init__(self, root):
        #Label标签
        Host = tkinter.Label(root, text = '服务器')
        Port = tkinter.Label(root, text = '端口')
        User = tkinter.Label(root, text = '用户名')
        Passwd = tkinter.Label(root, text = '密码')
        Subject = tkinter.Label(root, text = '主题')
        To = tkinter.Label(root, text = '收件人')
        MailFile = tkinter.Button(root, text = '浏览', command = self.MailFile)#调用MailFile函数(得到收件人群组)
        #定义Label的位置
        Host.place(x = 5, y = 5)
        Port.place(x = 200, y = 5)
        User.place(x = 5, y = 30)
        Passwd.place(x = 200, y = 30)
        Subject.place(x = 5, y = 55)
        To.place(x = 5, y = 83)
        #定义浏览按钮的位置
        MailFile.place(x = 345, y = 80)
    
        #Entry文本框
        self.entryHost = tkinter.Entry(root)
        self.entryPort = tkinter.Entry(root)
        self.entryUser = tkinter.Entry(root)
        self.entryPasswd = tkinter.Entry(root, show = '*')
        self.entryTo = tkinter.Entry(root, width = 40)
        self.entrySub = tkinter.Entry(root, width = 40)
        #读取配置文件
        config = ConfigParser()
        config.read('smtp.conf')
        Host = config.get('setting','Host')
        Port = config.get('setting','Port')
        User = config.get('setting','User')
        Passwd = config.get('setting','Passwd')
        #将配置文件里的值放入文本框
        self.entryHost.insert(tkinter.END,Host)
        self.entryPort.insert(tkinter.END,Port)
        self.entryUser.insert(tkinter.END,User)
        self.entryPasswd.insert(tkinter.END,Passwd)
        #文本框的位置
        self.entryHost.place(x = 50, y = 5)
        self.entryPort.place(x = 235, y = 5)
        self.entryUser.place(x = 50, y = 30)
        self.entryPasswd.place(x = 235, y = 30)
        self.entryTo.place(x = 50, y = 83)
        self.entrySub.place(x = 50, y = 55)
    
        #发送按钮，调用MailSend函数
        self.mailsend = tkinter.Button(root,text='开始发送',command=self.MailSend)
        #调用SaveConfig函数保存配置
        self.save = tkinter.Button(root,text='保存配置',command=self.SaveConfig)
        #调用Help函数打开帮助
        self.help = tkinter.Button(root,text='使用帮助',command=self.Help)
        #三个按钮的位置
        self.mailsend.place(x=430,y=20)
        self.save.place(x=430,y=60)
        self.help.place(x=520,y=60)

        #多行文本框，用来输入邮件内容
        self.text = tkinter.Text(root)
        self.text.place(y=120)

    def MailFile(self):
        #该函数用来读取放有邮件地址的文本文件
        r = tkinter.filedialog.askopenfilename(title='打开文件',filetypes=[('txt','*.txt')])
        if r :
            self.entryTo.delete(0,tkinter.END)
            self.entryTo.insert(tkinter.END,r)
    def MailSend(self):
        #使用get()获取各文本框中的内容
        host = self.entryHost.get()
        port = self.entryPort.get()
        user = self.entryUser.get()
        pw = self.entryPasswd.get()
        fromaddr = user
        subject = self.entrySub.get()
        text = self.text.get(1.0,tkinter.END)
        #读取文件
        mailfile = open(self.entryTo.get(),'r')
        mailaddr = mailfile.read()
        #使用正则表达式分割字符串，这里用逗号分割
        mail = re.split(',',mailaddr)
        #设置邮件内容为utf-8编码
        msg = MIMEText(text,_charset='utf-8')
        msg['From'] = fromaddr
        msg['Subject'] = subject
        smtp = smtplib.SMTP()
        smtp.connect(host,port)
        smtp.login(user,pw)
        #使用循环读取分割出来的邮件地址，同时实现邮件群发
        for toaddr in mail:
            msg['To'] = toaddr
            smtp.sendmail(fromaddr,toaddr,msg.as_string())
            smtp.close()
    #保存设置
    def SaveConfig(self):
        #获取文本框内容
        Host = self.entryHost.get()
        Port = self.entryPort.get()
        User = self.entryUser.get()
        Passwd = self.entryPasswd.get()
        #对需要保存的配置写入文件stmp.conf进行保存
        config = ConfigParser()
        config.add_section('setting')
        config.set('setting','Host',Host)
        config.set('setting','Port',Port)
        config.set('setting','User',User)
        config.set('setting','Passwd',Passwd)
        config.write(open('smtp.conf','w'))
    #使用帮助
    def Help(self):
        help_str = """
        1.服务器是SMTP服务器，QQ邮箱为smtp.qq.com, 126邮箱为smtp.126.com
        2.用户名必须带后缀，例如：12345@qq.com,   12345@126.com
        3.收件人使用txt文件，邮件地址有“,”分隔开
        """
        self.text.insert(tkinter.END,help_str)


#检查配置文件是否存在，不存在则创建
if(not os.path.isfile('smtp.conf')):
    config = ConfigParser()
    config.add_section('setting')
    config.set('setting','Host','smtp.qq.com')
    config.set('setting','Port','25')
    config.set('setting','User','user')
    config.set('setting','Passwd','passwd')
    config.write(open('smtp.conf','w'))

root = tkinter.Tk()
root.title("GUI_MAIL") #APP标题
root.geometry("650x500")
window = Window(root)
root.mainloop()