#!/usr/bin/python3
#-*-coding:utf-8-*-
from tkinter import *

root =Tk()
root.title("玉米街域名记事本")

def filecallback():
    print("文件被调用了")

def editcallback():
    print("编辑被调用了")

def searchcallback():
    print("查询被调用了")

def regexcallback():
    print("正则被调用了")

def aboutcallback():
    print("关于被调用了")

m=Menu(root)

# 定义文件菜单栏
fmenu =Menu(m,tearoff=False)
fmenu.add_command(label="新建",command=filecallback)
fmenu.add_command(label="打开",command=filecallback)
fmenu.add_separator()
fmenu.add_command(label="保存",command=filecallback)
fmenu.add_command(label="另存为",command=filecallback)
fmenu.add_separator()
fmenu.add_command(label="打开文件夹",command=filecallback)
fmenu.add_command(label="退出",command=root.quit)
m.add_cascade(label="文件",menu=fmenu)


# 定义编辑菜单栏
emenu =Menu(m,tearoff=False)
emenu.add_command(label="撤销",command=editcallback)
emenu.add_command(label="重做",command=editcallback)
emenu.add_separator()
emenu.add_command(label="剪切",command=editcallback)
emenu.add_command(label="复制",command=editcallback)
emenu.add_separator()
emenu.add_command(label="粘贴",command=editcallback)
emenu.add_command(label="删除",command=editcallback)
m.add_cascade(label="编辑",menu=emenu)

# 定义查询菜单栏
smenu =Menu(m,tearoff=False)
smenu.add_command(label="查找",command=searchcallback)
smenu.add_command(label="替代",command=searchcallback)
smenu.add_separator()
smenu.add_command(label="排序",command=searchcallback)
m.add_cascade(label="查询",menu=smenu)

# 定义正则菜单栏
rmenu =Menu(m,tearoff=False)
rmenu.add_command(label="四字母",command=regexcallback)
rmenu.add_command(label="四声母",command=regexcallback)
rmenu.add_separator()
rmenu.add_command(label="五数字",command=regexcallback)
rmenu.add_command(label="四数字",command=regexcallback)
rmenu.add_separator()
rmenu.add_command(label="双拼",command=regexcallback)
rmenu.add_command(label="三拼",command=regexcallback)
rmenu.add_separator()
rmenu.add_command(label="英文",command=regexcallback)
m.add_cascade(label="筛选",menu=rmenu)

# 定义帮助菜单栏
hmenu =Menu(m,tearoff=False)
hmenu.add_command(label="帮助",command=aboutcallback)
hmenu.add_command(label="联系我们",command=aboutcallback)
m.add_cascade(label="关于",menu=hmenu)

root.config(menu=m)
mainloop()