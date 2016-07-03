# -*- coding: utf-8 -*-
from tkinter import *

root = Tk()
# 80x80代表了初始化时主窗口的大小，0，0代表了初始化时窗口所在的位置
root.geometry('80x80+10+10')

# 填充方向
'''
Label(root, text = 'l1', bg = 'red').pack(fill = Y)
Label(root, text = 'l2', bg = 'green').pack(fill = BOTH)
Label(root, text = 'l3', bg = 'blue').pack(fill = X)


# 左右布局
Label(root, text = 'l1', bg = 'red').pack(fill = Y, side = LEFT)
Label(root, text = 'l2', bg = 'green').pack(fill = BOTH, side = RIGHT)
Label(root, text = 'l3', bg = 'blue').pack(fill = X, side = LEFT)

# 绝对布局
l4 = Label(root, text = 'l4')
l4.place(x = 3, y = 3, anchor = NW)
'''

# Grid 网格布局
l1 = Label(root, text = 'l1', bg = 'red')
l2 = Label(root, text = 'l2', bg = 'blue')
l3 = Label(root, text = 'l3', bg = 'green')
l4 = Label(root, text = 'l4', bg = 'yellow')
l5 = Label(root, text = 'l5', bg = 'purple')

l1.grid(row = 0, column = 0)
l2.grid(row = 1, column = 0)
l3.grid(row = 1, column = 1)
l4.grid(row = 2 )
l5.grid(row = 0, column = 3)

root.mainloop()