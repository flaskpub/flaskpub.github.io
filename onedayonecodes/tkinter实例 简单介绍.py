#!/usr/bin/python3
#-*-coding:utf-8-*-
# http://blog.csdn.net/yao_yu_126/article/details/23422845
import tkinter  as tk  
from tkinter    import ttk  
  
def sample1_hello_title():  
    '''''1, 最简单'''  
    root = tk.Tk()  
    root.title('你好, 这是tkinter世界!')  
    root.mainloop()  
  
def sample2_hello_label():  
    '''''2, 添加一个标签'''  
    root = tk.Tk()  
    root.title('示例')  
    label = ttk.Label(root, text='你好,欢迎来到tkinter世界!')  
    label.pack()  
    root.mainloop()  
  
def sample3_hello2():  
    class Application(object):  
        def __init__(self, master=None):  
            self.master = master  
            frame = ttk.Frame(master)  
            frame.pack(expand="yes", fill="both")  
              
            #输入框  
            self.msgVar = tk.StringVar()  
            self.msgVar.set('欢迎来到tkinter的世界')  
            self.input = ttk.Entry(frame, textvariable=self.msgVar)  
            self.input.pack(fill='x', padx=10, pady=10)  
              
            #提示信息框  
            self.caption = ttk.Label(frame,text='')  
            self.caption.pack(expand='yes')  
              
            #命令面板  
            commandpane = ttk.Frame(frame)  
            commandpane.pack(pady=10)  
            self.btnHello = ttk.Button(commandpane, text='您好', command=self.say_hi)  
            self.btnHello.pack(side='left')  
            self.button = ttk.Button(commandpane, text='退出', command=frame.quit)  
            self.button.pack()  
              
        def say_hi(self):  
            self.caption['text']= '你好,%s!' % self.input.get()  
    app = Application(tk.Tk())  
    app.master.mainloop()  
  
if __name__ == '__main__':  
    #sample1_hello_title()  
    #sample2_hello_label()  
    sample3_hello2()  