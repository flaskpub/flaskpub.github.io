#!/usr/bin/python3
#-*-coding:utf-8-*-
# 多线程聊天软件程序
# http://www.cnblogs.com/Arago/p/5162618.html
import socket
import pickle
import threading
import tkinter
import os
import datetime
import time
try:
    import pymysql
except:
    print("can't find pymysql")


tcplocalport=8101 #TCP监听端口
tcpconnectport=8101 #TCP连接端口
udplocalport=8201 #广播监听端口
udpconnectport=8201 #广播连接端口
filelocalport=8301 #文件监听接口
fileconnectport=8301 #文件连接端口
localIP=socket.gethostbyname(socket.gethostname()) #本机IP
print("localip:",localIP)
print('localtcpport:',tcplocalport)

#sockdict字典用于存放本机作为客户端的连接对象
sockdict={}

#filedict字典用于存放文件传输的信息
#filedict['IP']=['filename',filesize,fpobj,restsize]
filedict={}
sendfileflag={}

#用于调用软件的图形界面
showdict={}

#转换用表
#a为address,i为listbox的index值，n为name
a2i={}
a2n={}
i2a={}

myname='a'

sqlflag=0 #MYSQL启用标志，若启用MYSQL，则为1


#用于通讯的类,type为通讯指令的类型，name为发送端的名称
#data为正文，target为目标对象，time为发送时的时间
class talkdata:
    def __init__(self,ttype,tname,tdata,ttarget=""):
        self.dtype=ttype
        self.dname=tname
        self.ddata=tdata
        self.dtarget=ttarget
        self.dtime=gettime()

#获取时间的函数
def gettime():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


#解析接收到的数据
def solvedata(data_str,address,protocols):
    global sockdict
    global filedict
    global a2n
    global sendfileflag
    data_obj=pickle.loads(data_str)
    if data_obj.dtype=="searchse" and (address[0]!=localIP or data_obj.dname!=myname): #搜索发起类型
        reply=talkdata("searchre",myname,"")
        if sockdict.get(address[0])==None:
            socketconnect(address[0],tcpconnectport)
        send(sockdict[address[0]],reply)
    if data_obj.dtype=="searchre" and (address[0]!=localIP or data_obj.dname!=myname): #搜索回复类型
        a2n[address[0]]=data_obj.dname
    """if data_obj.dtype=="tcpcon":
        if showdict.get(address[0])==None:
            socketconnect(address[0],tcpconnectport)
            threading.Thread(target=
                         createfgui_guif,arg=
                         (sockdict[address[0]],(address[0],tcpconnectport))).start()            
    """
    if data_obj.dtype=="str": #聊天内容类型
        adata=data_obj.dtime+"\n"+data_obj.dname+':'+data_obj.ddata
        if showdict.get(address[0])==None:
            a2n[address[0]]=data_obj.dname
            socketconnect(address[0],tcpconnectport)
            threading.Thread(target=
                createfgui_guif,args=
                (sockdict[address[0]],(address[0],tcpconnectport))).start()
            time.sleep(0.5)
        showdict[address[0]].insert('end',adata)
        print(data_obj.ddata)
    if data_obj.dtype=="filehead": #发送文件头类型
        filename=data_obj.ddata[0]
        filesize=data_obj.ddata[1]
        restsize=filesize
        print("filename:",filename)
        print("filesize:",filesize)

        filetk=tkinter.Tk()
        filetk.withdraw()
        fd=tkinter.filedialog.FileDialog(filetk)
        filesavename=fd.go()
        filetk.destroy()
        if filesavename==None:
            filef=talkdata('fileflag',myname,"refuse")
        else:
            #fp=open(filename,'wb')
            #fp=open(input("filename:"),'wb')
            fp=open(filesavename,'wb')
            filedict[address[0]]=[filename,filesize,fp,restsize]
            if sockdict.get(address[0])==None:
                socketconnect(address[0],tcpconnectport)
            filef=talkdata('fileflag',myname,"accept")
        send(sockdict[address[0]],filef)
    if data_obj.dtype=="fileflag": #文件允许接收类型
        if data_obj.ddata=="accept":
            sendfileflag[address[0]]=1
            print("start send file")
        if data_obj.ddata=="refuse":
            sendfileflag[address[0]]=2
    if data_obj.dtype=="udpstr" and (address[0]!=localIP or data_obj.dname!=myname): #广播聊天内容类型
        adata=data_obj.dtime+"\n"+data_obj.dname+':'+data_obj.ddata
        showdict[data_obj.dtarget].insert('end',adata)
    if sqlflag==1 and protocols=='tcp':
        sqlsavedata(data_obj,address[0])

#连接MYSQL
def sqlinit():
    global sqlcon,sqlcur,sqlflag
    sqlcon=pymysql.connect(host='localhost',user='root',passwd='',port=3306)
    sqlcur=sqlcon.cursor()
    try :
        sqlcon.select_db('talk')
    except :        
        sqlcur.execute('create database if not exists talk')
        sqlcon.select_db('talk')    
    sqlcon.commit()
    sqlflag=1
    print('connect sql')

#创建表    
def sqlcreattable(ip):
    global sqlcon,sqlcur
    daip=''
    for i in ip:
        if i=='.':
            i='_'
        daip=daip+i
    sqlcur.execute("""create table if not exists %s
    (type varchar(20),
    name varchar(20),
    data varchar(500),
    time datetime)""" % daip)
    sqlcon.commit()

#将数据加入数据库
def sqlsavedata(data_obj,ip):
    global sqlcon,sqlcur
    daip=''
    for i in ip:
        if i=='.':
            i='_'
        daip=daip+i
    value="insert into %s values('%s','%s','%s','%s')" % (daip,data_obj.dtype,data_obj.dname,data_obj.ddata,data_obj.dtime)
    #print(value)
    sqlcur.execute(value)
    sqlcon.commit()

#读取数据库中的数据
def sqlloaddata(ip):
    global sqlcon,sqlcur
    daip=''
    for i in ip:
        if i=='.':
            i='_'
        daip=daip+i
    sqlcur.execute('select * from %s' % daip)
    a=sqlcur.fetchall() 
    sqlcon.commit()
    return a


#发送聊天
def send(socketobj,data_obj):
    data_pickle=pickle.dumps(data_obj)
    try :
        socketobj.send(data_pickle)
    except ConnectionResetError :
        address=socketobj.getpeername()
        socketconnect(address[0],address[1])
        sockdict[address[0]].send(data_pickle)

#广播聊天对象
def sendudp(data_obj):
    data_str=pickle.dumps(data_obj)
    addr=('<broadcast>',udpconnectport)
    udps=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udps.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    udps.sendto(data_str,addr)

#发送文件
def sendfile(socketobj,filename):
    fp=open(filename,'rb')
    filesize=os.stat(filename).st_size
    fhead=talkdata("filehead",myname,(filename,filesize))
    address=socketobj.getpeername()
    send(socketobj,fhead)
    sendfileflag[address[0]]=0
    while sendfileflag[address[0]]==0:
        pass
    if sendfileflag[address[0]]==2:
        return 0
    socketfile=socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
    socketfile.connect((address[0],fileconnectport))
    
    while 1:
        filedata=fp.read(1024)
        if not filedata:
            break
        socketfile.send(filedata)
    print("send over")

#接收TCP信息
def rec(connect,address):
    while 1:
        #try:
            data_str=connect.recv(1024)
            if not data_str:
                print("leave")
                break
            print('Receive TCP data from',address)            
            solvedata(data_str,address,'tcp')
        #except:
         #   print('Receive TCP data error\n')
          #  break

#接收文件
def recfile(connect,address):
    while 1:
        #try:
            filedata=connect.recv(1024)
            if not filedata:
                print("leave")
                break                        
            restsize=filedict[address[0]][3]
            print("Receive file data from",address,"\nRestsize:",restsize)
            fp=filedict[address[0]][2]
            fp.write(filedata)
            restsize=restsize-len(filedata)
            filedict[address[0]][3]=restsize
            if restsize<=0:
                fp.close()
                print("Receive file successful")
        #except:
         #   print('Receive file data error\n')
          #  break    

#接收广播信息
def socketudplisten(sockobj):
    while 1:
        data_str,address=sockobj.recvfrom(1024)
        if not data_str:
            pring("no udpdata")
        if sqlflag==1 :
            sqlcreattable(address[0])
        solvedata(data_str,address,'udp')

#文件接收端口监听    
def filelisten(sockobj):
    threfdict={}
    while 1:
        connect,address=sockobj.accept()
        print("File accept ",address)
        threfdict[address[0]]=threading.Thread(target=recfile,args=(connect,address))
        threfdict[address[0]].start()   

#TCP端口监听
def socketlisten(sockobj):
    global sqlflag
    thredict={}
    while 1:
        connect,address=sockobj.accept()
        print("Accept ",address)
        if sqlflag==1 :
            sqlcreattable(address[0])
        thredict[address[0]]=threading.Thread(target=rec,args=(connect,address))
        thredict[address[0]].start()

#连接TCP
def socketconnect(connectIP,connectport):
    global sockdict
    try:
        sockse=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sockse.connect((connectIP,connectport))
        print("connect")
        sockdict[connectIP]=sockse
        if sqlflag==1 :
            sqlcreattable(connectIP)
    except:
        print("tcp connect error")

#登录按钮执行的功能
def login_guif():
    global myname
    if entryname.get()!='':
        myname=entryname.get()
    listgui.title(myname)
    listgui.deiconify()
    logingui.withdraw()

#ip连接对话框的连接按钮执行的功能
def getip_guif():
    global i2a,a2i,a2n
    #连接对话框
    tcpcongui=tkinter.Toplevel()
    framefip=tkinter.Frame(tcpcongui)
    framefip.pack()
    labelip=tkinter.Label(tcpcongui,text='IP地址')
    labelip.pack()
    entryip=tkinter.Entry(tcpcongui)
    entryip.pack()
    tkinter.Button(tcpcongui,text="连接",command=lambda :inputip_guif(tcpcongui,entryip)).pack()
    
    select=lbfriends.curselection()
    a=()
    if select==a:
        connectip=""
    else:
        connectip=i2a[select[0]]
    entryip.insert(0,connectip)

#发送文件按钮执行的功能
def sendfile_guif(socketobj,tkobj):
    fd=tkinter.filedialog.FileDialog(tkobj)
    filename=fd.go()
    threading.Thread(target=sendfile,args=(socketobj,filename)).start()

#创建私聊聊天窗口
def createfgui_guif(socketobj,address):
    global showdict
    global a2n
    if a2n.get(address[0])==None:
        name=address[0]
    else:
        name=a2n[address[0]]
    tl=tkinter.Tk()
    tl.title(name)
    framereceive=tkinter.Frame(tl)
    framereceive.pack()
    scrollbarreceive=tkinter.Scrollbar(framereceive)
    scrollbarreceive.pack(fill='y',side='right')
    showtext=tkinter.Text(framereceive,height=20,
                      width=60,yscrollcommand=scrollbarreceive.set)
    showtext.pack(side='left')
    
    framesend=tkinter.Frame(tl)
    framesend.pack()
    scrollbarsend=tkinter.Scrollbar(framesend)
    scrollbarsend.pack(fill='y',side='right')
    sendtext=tkinter.Text(framesend,height=4,
                      width=60,yscrollcommand=scrollbarsend.set)
    sendtext.pack(side='left')
    
    framebutton=tkinter.Frame(tl)
    framebutton.pack()
    tkinter.Button(framebutton,text='发送信息',command=lambda:send_guif(socketobj,showtext,sendtext)).pack(side='right')
    tkinter.Button(framebutton,text='发送文件',command=lambda:sendfile_guif(socketobj,tl)).pack(side='left')
    tkinter.Button(framebutton,text='聊天记录',command=lambda:loaddata_guif(address[0])).pack(side='left')

    showdict[address[0]]=showtext
    tl.mainloop()

#创建广播聊天窗口
def createggui_guif(target):
    global showdict
    tl=tkinter.Tk()
    tl.title(target)
    framereceive=tkinter.Frame(tl)
    framereceive.pack()
    scrollbarreceive=tkinter.Scrollbar(framereceive)
    scrollbarreceive.pack(fill='y',side='right')
    showtext=tkinter.Text(framereceive,height=20,
                      width=60,yscrollcommand=scrollbarreceive.set)
    showtext.pack(side='left')
    
    framesend=tkinter.Frame(tl)
    framesend.pack()
    scrollbarsend=tkinter.Scrollbar(framesend)
    scrollbarsend.pack(fill='y',side='right')
    sendtext=tkinter.Text(framesend,height=4,
                      width=60,yscrollcommand=scrollbarsend.set)
    sendtext.pack(side='left')
    
    framebutton=tkinter.Frame(tl)
    framebutton.pack()
    tkinter.Button(framebutton,text='发送信息',command=lambda:sendudp_guif(target,showtext,sendtext)).pack(side='right')

    showdict[target]=showtext
    tl.mainloop()

#聊天记录按钮执行的功能
def loaddata_guif(ip):
    sqldata=sqlloaddata(ip)
    datagui=tkinter.Tk()
    scrollbarreceive=tkinter.Scrollbar(datagui)
    scrollbarreceive.pack(fill='y',side='right')
    showtext=tkinter.Text(datagui,height=20,
                      width=60,yscrollcommand=scrollbarreceive.set)
    showtext.pack(side='left')
    for tadata in sqldata:
        adata="%s %s \n%s:%s" % (tadata[3],tadata[0],tadata[1],tadata[2])
        showtext.insert('end',adata)

#私聊窗口中发送信息按钮执行的功能
def send_guif(socketobj,showtext,sendtext):
    data=sendtext.get('0.0','end')
    adata=gettime()+'\n'+myname+':'+data
    sendtext.delete('0.0','end')
    showtext.insert('end',adata)
    data_obj=talkdata("str",myname,data)
    if sqlflag==1:
        address=socketobj.getpeername()
        sqlsavedata(data_obj,address[0])
    send(socketobj,data_obj)

#群聊窗口中发送信息按钮执行的功能    
def sendudp_guif(target,showtext,sendtext):
    data=sendtext.get('0.0','end')
    adata=gettime()+'\n'+myname+':'+data
    sendtext.delete('0.0','end')
    showtext.insert('end',adata)
    data_obj=talkdata("udpstr",myname,data,target)
    sendudp(data_obj)

#IP对话框中连接按钮执行的功能            
def inputip_guif(gui,entryip):
    global sockdict
    gui.withdraw()
    connectip=entryip.get()
    if connectip=="":
        connectip="127.0.0.1"
    socketconnect(connectip,tcpconnectport)
    threading.Thread(target=
                     createfgui_guif,args=
                     (sockdict[connectip],(connectip,tcpconnectport))).start()

#我的群组中连接按钮执行的功能，暂未加入
def getgroup_guif():
    target=lbgroups.selection_get()
    threading.Thread(target=
                     createggui_guif,args=(target,)).start()
    
#我的好友中刷新按钮执行的功能
def refreshf_guif():
    global a2n
    global a2i
    global i2a
    a2n.clear()
    a2i.clear()
    i2a.clear()
    lbfriends.delete(0,'end')    
    data=talkdata("searchse",myname,(localIP,tcplocalport))
    sendudp(data)
    time.sleep(1)
    i=0
    for key in a2n:
        lbfriends.insert(i,a2n[key])
        a2i[key]=i
        i2a[i]=key
        i=i+1
    
#我的群组中刷新按钮执行的功能
def refreshg_guif():
    pass

    
            
#登录界面
logingui=tkinter.Tk()
logingui.title('登录')

framelogin=tkinter.Frame(logingui)
framelogin.pack()
labelname=tkinter.Label(framelogin,text='名称')
labelname.pack(side='left')
entryname=tkinter.Entry(framelogin)
entryname.pack(side='right')

frameloginbutton=tkinter.Frame(logingui)
frameloginbutton.pack()
tkinter.Button(frameloginbutton,text="  登录  ",command=login_guif).pack(side='right')
tkinter.Button(frameloginbutton,text="MYSQL",command=sqlinit).pack(side='left')


#列表界面
#listgui=tkinter.Toplevel()
listgui=tkinter.Tk()
listgui.withdraw()

framelistfriends=tkinter.Frame(listgui)
framelistfriends.pack(side='left')
lablefriends=tkinter.Label(framelistfriends,text='我的好友')
lablefriends.pack(side='top')
lbfriends=tkinter.Listbox(framelistfriends)
lbfriends.pack(side='top')
framlistfbutton=tkinter.Frame(framelistfriends)
framlistfbutton.pack()
tkinter.Button(framlistfbutton,text="刷新",command=refreshf_guif).pack(side='left')
tkinter.Button(framlistfbutton,text="连接",command=getip_guif).pack(side='right')

framelistgroups=tkinter.Frame(listgui)
framelistgroups.pack(side='right')
lablegroups=tkinter.Label(framelistgroups,text='我的群组')
lablegroups.pack(side='top')
lbgroups=tkinter.Listbox(framelistgroups)
lbgroups.pack(side='top')
lbgroups.insert(0,"广播")
framlistgbutton=tkinter.Frame(framelistgroups)
framlistgbutton.pack()
tkinter.Button(framlistgbutton,text="刷新",command=refreshg_guif).pack(side='left')
tkinter.Button(framlistgbutton,text="连接",command=getgroup_guif).pack(side='right')

#TCP套接字初始化
sockre=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sockre.bind(('',tcplocalport))
sockre.listen(30)
print('TCP listen')

#接收文件初始化
sockref=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sockref.bind(('',filelocalport))
sockref.listen(30)

#UDP套接字初始化
sockreudp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sockreudp.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sockreudp.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
sockreudp.bind(('',udplocalport))

#创建线程监听端口
thredlisten=threading.Thread(target=socketlisten,args=(sockre,))
thredlisten.start()

threfilelisten=threading.Thread(target=filelisten,args=(sockref,))
threfilelisten.start()

threudplisten=threading.Thread(target=socketudplisten,args=(sockreudp,))
threudplisten.start()