# _*_ coding: utf-8 _*_
from tkinter import *
root = Tk()
root.title('极简记事本0.01')
mi=StringVar()
Label(text='请在下面编辑您的文档').pack()

te = Text(height = 30,width =100)
te.pack()

Label(text='File name').pack(side = LEFT)
Entry(textvariable = mi).pack(side = LEFT)
mi.set('*.txt')
def save():
  t = te.get('0.0','10.0')
  f = open(mi.get(),'w')
  f.write(t)
Button(text = 'Save' , command = save).pack(side = RIGHT)
Button(text = 'Exit' , command = root.quit).pack(side = RIGHT)

mainloop()
