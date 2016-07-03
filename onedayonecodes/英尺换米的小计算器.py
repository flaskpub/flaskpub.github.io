from tkinter import *
from tkinter import ttk
# http://blog.csdn.net/maillibin/article/details/46954223
#计算程序
def calculate(* args):
    value=float(feet_entry.get())
    meters=(0.3048*value*10000.0+0.5)/10000.0
    ttk.Label(mainframe,text=meters).grid(column=2,row=2,sticky=W)
    print(meters)

#界面设计
root=Tk()
root.title("英尺转换为米")
    
mainframe=ttk.Frame(root,padding="150 30 10 30")
mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

feet_entry=ttk.Entry(mainframe,width=5)
feet_entry.grid(column=2,row=1,sticky=(W,E))

ttk.Label(mainframe,text="英尺").grid(column=3,row=1,sticky=W)
ttk.Label(mainframe,text="等于").grid(column=1,row=2,sticky=E)
ttk.Label(mainframe,text="米").grid(column=3,row=2,sticky=W)

ttk.Button(mainframe,text="计算",command=calculate).grid(column=3,row=3,sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=3,pady=7)
    
feet_entry.focus()

#绑定事件
root.bind("<Return>",calculate)

root.mainloop()