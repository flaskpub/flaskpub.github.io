# -*- coding: utf-8 -*-

from Tkinter import *
import random 
from tkMessageBox import askquestion

#尚需改进，有待提高

#各种方块的表示，与参考方块的相对位置
shapedic={1:((0,0),(1,0),(0,-1),(1,-1)),#正方形
          2:((0,0),(0,-1),(0,-2),(0,1)),#长条
          3:((0,0),(0,-1),(1,0),(1,1)),#之字型
          4:((0,0),(0,-1),(-1,0),(-1,1)),#反之字型
          5:((0,0),(1,0),(-1,0),(-1,-1)),#L型
          6:((0,0),(1,0),(-1,0),(1,-1)),#反L型
          7:((0,0),(1,0),(-1,0),(0,-1))#T型
          }

#旋转函数，顺时针旋转90度，相对于参考方块
change_dic={(0,0):(0,0),(0,1):(-1,0),(-1,0):(0,-1),(0,-1):(1,0),(1,0):(0,1),
           (1,-1):(1,1),(1,1):(-1,1),(-1,1):(-1,-1),(-1,-1):(1,-1),
            (2,0):(0,2),(0,2):(-2,0),(-2,0):(0,-2),(0,-2):(2,0)}
            
#随机颜色
colorDict = {
        0 :'#CCC0B4', 
        1 :'#EEE4DA', 
        2 : '#EDE0C8', 
        3 : '#F2B179',
        4 : '#EC8D54', 
        5 : '#F67C5F',  
        6 : '#EA5937', 
        7 : '#804000',  
        8 : '#F1D04B', 
        9 : '#E4C02A', 
        10 : '#EE7600', 
        11 : '#D5A500', 
        12 : '#E4C02A', 
        13 : '#804000', 
        14 : '#EA5937', 
        15 : '#EE7600',
        16 : '#776E65',
        17 : '#776E65',
        18 : '#FFFFFF',
        19 : 'yellow',
        20 : 'blue',
        21 : 'lightblue',
        22 : 'red'
        }

#俄罗斯方块
class Game_Russia:
    
    def __init__(self):
        
        #每个方块的大小
        self.width=20
        
        #方块数目，长和宽
        self.row=28
        self.column=19
        
        
#        #初始化
#        self.scores=0
#        self.all_square={}#坐标系网格中个位置方块的存在性
#        self.head_square=[]#参考方块绝对位置
#        self.new_square=[]#移动方块相对位置
#        self.direction=-1#方块初始方向
#        #规定界限
#        #i表示第i列，0在左边
#        #j表示第j行，零在上面
#        for j in range(-4,self.row):
#            for i in range(self.column):
#                self.all_square[i,j]=0
#        #划界，开口向上
#        for j in range(self.row+1):
#            self.all_square[19,j]=1
#            self.all_square[-1,j]=1
#        for i in range(-1,self.column+1):
#            self.all_square[i,28]=1
         
        """ 
        用来debug
        for j in range(self.row+1):
            for i in range(-1,self.column+1):
                print self.all_square[i,j],
            print
        """

        self.window = Tk()
        self.window.geometry()
        self.window.maxsize(400,610)
        self.window.minsize(400,610)
        self.window.title(u"俄罗斯方块")
        
        self.frame1=Frame(self.window,bg="white",relief=GROOVE,borderwidth=5)
        self.frame2=Frame(self.window,bg="white",relief=RAISED,borderwidth=2,height=40,
                          width=570)
        self.canvas=Canvas(self.frame1,bg='purple',width=400,height=570)
        self.score_label=Label(self.frame2,text="Score: 0")
        
        self.frame1.pack()
        self.frame2.pack(fill=BOTH)
        self.score_label.pack(side=LEFT)
        self.canvas.pack(fill=BOTH)
        
        self.draw_wall()
        
        self.initial()
        
        self.get_new_square()
        
        self.draw_new_square()
        
        self.play()
        
        self.window.mainloop()
        
        
        
    "=== View Part ==="
    #边界
    def draw_wall(self):
        self.canvas.create_line(5,5,385,5,fill='blue',width=1)
        self.canvas.create_line(385,5,385,565,fill='blue',width=1)
        self.canvas.create_line(5,5,5,565,fill='blue',width=1)
        self.canvas.create_line(5,565,385,565,fill='blue',width=1)
    
    #得分
    def draw_score(self):
        self.get_score()
        self.score_label.config(self.score_label,text="Score: "+str(self.scores))

    #画下面所有不动的方块
    def draw_square(self):
        color=colorDict[random.randint(0,len(colorDict)-1)]
        for j in range(self.row):
            self.canvas.delete("line"+str(j))
            for i in range(self.column):
                if self.all_square[i,j]:
                    self.canvas.create_rectangle(5+i*self.width,
                    5+j*self.width,5+(i+1)*self.width,
                    5+(j+1)*self.width,fill=color,tags="line"+str(j))
    #画移动的方块
    def draw_new_square(self):
        self.canvas.delete("new")
        self.head_square[1]+=1
        color=colorDict[random.randint(0,len(colorDict)-1)]
        for i in range(4):
            self.canvas.create_rectangle(5+(self.head_square[0]+self.new_square[i][0])*self.width,
                5+(self.head_square[1]+self.new_square[i][1])*self.width,
                5+(self.head_square[0]+self.new_square[i][0]+1)*self.width,
                5+(self.head_square[1]+1+self.new_square[i][1])*self.width,fill=color,tags="new")

    
    "=== Model Part ==="
    def initial(self):
        #初始化
        self.scores=0
        self.all_square={}#坐标系网格中个位置方块的存在性
        self.head_square=[]#参考方块绝对位置
        self.new_square=[]#移动方块相对位置
        self.direction=-1#方块初始方向
        #规定界限
        #i表示第i列，0在左边
        #j表示第j行，零在上面
        for j in range(-4,self.row):
            for i in range(self.column):
                self.all_square[i,j]=0
        #划界，开口向上
        for j in range(self.row+1):
            self.all_square[19,j]=1
            self.all_square[-1,j]=1
        for i in range(-1,self.column+1):
            self.all_square[i,28]=1
        
    def is_dead(self):
        #判断死亡与否，最上方中间四个方块
        for i in {8,9,10,11}:
            if self.all_square[i,0]:
                return True
        else:
            return False
            
    
    def get_new_square(self):
        #获得新的方块，初始位置均为（9,-2）
        self.new=random.randrange(1,8)#随机方块
        #主方块（参考方块）的位置
        self.direction=random.randrange(4)
        self.head_square=[9,-2]
        self.new_square=list(shapedic[self.new])
        for i in range(self.direction):
            self.change()
        
        
    def delete_one_line(self,j):
        #得分后删除整行
        for t in range(j,2,-1):
            for i in range(self.column):
                self.all_square[i,t]=self.all_square[i,t-1]
        for i in range(self.column):
            self.all_square[i,0]=0
        
    
    def get_score(self):
        for j in range(self.row):
            for i in range(self.column):
                #判断某行是否全满
                if not self.all_square[i,j]:
                    break
            else:
                self.scores+=10
                self.delete_one_line(j)
                
    #移动方块停止
    def get_seated(self):
        self.all_square[tuple(self.head_square)]=1
        for i in range(4):
            self.all_square[self.head_square[0]+self.new_square[i][0],
            self.head_square[1]+self.new_square[i][1]]=1
            
    #方块是否到了最底端    
    def is_seated(self):
        for i in range(4):
            if self.all_square[self.head_square[0]+self.new_square[i][0],
                               self.head_square[1]+self.new_square[i][1]+1]:
                return True
        return False
            
     
        
    "=== Control Part ===" 
    #改变方块朝向
    #通过旋转改变，主方块不动
    def change(self):
        if self.new>1:
            for i in range(4):
                if self.all_square[self.head_square[0]+change_dic[self.new_square[i]][0],self.head_square[1]+change_dic[self.new_square[i]][1]]:
                    return 
            else:
                for i in range(4):
                    self.new_square[i]=change_dic[self.new_square[i]]
        else:
            return
    #右移
    def right_move(self):
        #先判断是否可以移动
        for i in range(4):
            if self.all_square[self.head_square[0]+self.new_square[i][0]-1,
                self.head_square[1]+self.new_square[i][1]]:
                return True
        self.head_square[0]-=1
    
    #左移
    def left_move(self):
        for i in range(4):
            if self.all_square[self.head_square[0]+self.new_square[i][0]+1,
                self.head_square[1]+self.new_square[i][1]]:
                return True
        self.head_square[0]+=1
    
    #向下加速
    def down_quicker(self):
        while (not self.is_seated()):
            self.draw_new_square()
            
            self.canvas.after(50)
            self.canvas.update()
            
    #方向键控制
    def move(self,event):
        if event.keycode == 39:
            self.left_move()   
        elif event.keycode == 38:
            self.change()
        elif event.keycode == 37:
            self.right_move()
        elif event.keycode == 40:
            self.down_quicker()
        else:
            pass
    #开始游戏
    def play(self):
        self.canvas.bind('<Key>',self.move)
        self.canvas.focus_set()
        
        while True:
            if self.is_dead():
                self.gameover()
                break
            
            if self.is_seated():
                
                self.get_seated()
                self.get_new_square()
                
                self.draw_score()
                self.draw_square()
                self.draw_new_square()
                
                
            else:
                self.draw_new_square()
                
                self.canvas.after(500)
                self.canvas.update()
            

    #游戏结束
    def gameover(self):
        if askquestion("LOSE",u"你输了!\n重新开始吗？") == 'yes':
            return self.restart()
        else:
            return self.window.destroy()
    
    #重新开始    
    def restart(self):
        self.initial()
        
        self.draw_square()
        
        self.get_new_square()
        
        self.draw_new_square()
        
        self.play()
     
#主程序
if __name__ == "__main__":
    Game_Russia() 
