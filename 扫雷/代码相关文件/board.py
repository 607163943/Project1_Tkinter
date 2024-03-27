import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from os import path
import random
import setting
import csv
class Board:   # 扫雷组件相关类
    def __init__(self,root:tk.Tk):
        self.tk=root  # 放置主窗口类的对象
        self.image_dict={"face":[],"mine":[],"safe":[]}   # 存放不同类型的图片
        self.board_dict={"row":9,"col":9,"boom":10,"flag":10,"time":0}  # 存放扫雷棋盘的数据
        self.using="简单"  # 当前的扫雷难度
        self.board1=[]  # 存放棋盘中雷的位置
        self.board2=[]  # 存放棋盘中每个位置的周围雷的个数
        self.board3=[]  # 存放棋盘中各位置的排查情况
        self.time=0   # 扫雷耗时
        self.flag=self.board_dict.get("flag")  # 红旗数
        self.button_list=[]   # 存放棋盘中各位置的按钮
        self.time_continue=True  # 判断是否继续计时
        self.flag_list=[]   # 判断棋盘中插旗位置
        self.is_menu_set_window_show=True   # 是否从开始界面跳转过来
        self.score_dict={'easy':0,'normal':0,'trouble':0}  # 存放各难度的最高分数记录
        self.is_once_again=False  # 是否重新开始过
        self.file_start()   # 初始化加载数据文件
        self.load_image()  # 初始化加载图片文件
    def __del__(self):
        self.file.seek(0)  # 将数据文件指针移到文件开头
        self.csv_file.writerow(self.score_dict.values())  # 将最新的各难度最高记录同步到数据文件中
        self.file.close()  # 关闭文件
    def load_image(self):  # 加载图片文件函数
        dir_image_base=""
        dir_image=path.join(dir_image_base,"image")  # 生成图片总文件夹路径
        self.image_dict["flag"]=tk.PhotoImage(file=path.join(dir_image,"flag1.png"),format="png")
        self.image_dict["normal"]=tk.PhotoImage(file=path.join(dir_image,"normal.png"),format="png")
        dir_image_face=path.join(dir_image,"face")
        for i in range(1,4):
            self.image_dict["face"].append(tk.PhotoImage(file=path.join(dir_image_face,f"face{i}.png"),format="png"))
        dir_image_mine=path.join(dir_image,"mine")
        for i in range(1,3):
            self.image_dict["mine"].append(tk.PhotoImage(file=path.join(dir_image_mine,f"mine{i}.png"),format="png"))
        dir_image_safe=path.join(dir_image,"safe")
        for i in range(9):
            self.image_dict["safe"].append(tk.PhotoImage(file=path.join(dir_image_safe,f"safe{i}.png"),format="png"))
    def file_start(self):  # 加载数据文件函数
        dir_path_base=""
        dir_data_path=path.join(dir_path_base,"data")  # 生成数据文件总文件夹路径
        csv_file=open(path.join(dir_data_path,"score.csv"),mode="r+",encoding="UTF-8",newline="")  # 打开数据文件
        self.file=csv_file
        for i in self.file:  # 获取数据文件中各难度的最高纪录
            temp_list=i.split(',')
            self.score_dict["easy"]=int(temp_list[0])
            self.score_dict["normal"]=int(temp_list[1])
            self.score_dict["trouble"]=int(temp_list[2])
            break
        self.csv_file=csv.writer(csv_file)
    def show_start_window(self):  # 扫雷的开始界面
        self.frame1=tk.Frame(self.tk)
        self.label1_1=tk.Label(self.frame1,text="扫雷",font=setting.START_WINDOW_TITLE_FONT,width=20)
        self.label1_1.pack(pady=10)
        self.label1_2=tk.Label(self.frame1,text="最快通关记录",font=setting.START_WINDOW_OTHER_FONT)
        self.label1_2.pack(pady=10)
        self.label1_3=tk.Label(self.frame1,text=f"简单:{self.score_dict.get('easy')}",font=setting.START_WINDOW_OTHER_FONT)
        self.label1_3.pack(pady=10)
        self.label1_4=tk.Label(self.frame1,text=f"普通:{self.score_dict.get('normal')}",font=setting.START_WINDOW_OTHER_FONT)
        self.label1_4.pack(pady=10)
        self.label1_5=tk.Label(self.frame1,text=f"困难:{self.score_dict.get('trouble')}",font=setting.START_WINDOW_OTHER_FONT)
        self.label1_5.pack(pady=10)
        self.button1_1=tk.Button(self.frame1,text="开始游戏",font=setting.BOARD_FONT,command=self.start)
        self.button1_1.pack(pady=10)
        self.frame1.pack()
    def start(self):  # 扫雷开始游戏后的初始化函数
        if self.is_menu_set_window_show:  # 从开始界面进入游戏将销毁开始界面组件
            self.frame1.destroy()
            self.is_menu_set_window_show=False
        # 初始化棋盘位置数据
        self.board1=[[0 for j in range(self.board_dict.get("col")+2)] for i in range(self.board_dict.get("row")+2)]
        self.board2=[[0 for j in range(self.board_dict.get("col")+2)] for i in range(self.board_dict.get("row")+2)]
        self.board3=[["*" for j in range(self.board_dict.get("col")+2)] for i in range(self.board_dict.get("row")+2)]
        temp=self.board_dict.get("boom")
        # 放置棋盘的雷
        while temp>0:
            x,y=random.randint(0,self.board_dict.get("row")-1),random.randint(0,self.board_dict.get("col")-1)
            if self.board1[x+1][y+1]==0:
                self.board1[x+1][y+1]=1
                temp-=1
        for i in range(1,self.board_dict.get("row")+1):
            for j in range(1,self.board_dict.get("col")+1):
                self.board2[i][j]=(self.board1[i+1][j]+self.board1[i][j+1]+self.board1[i+1][j+1]+
                                   self.board1[i-1][j]+self.board1[i][j-1]+self.board1[i-1][j-1]+
                                   self.board1[i-1][j+1]+self.board1[i+1][j-1])
        # 初始化棋盘其他数据
        self.time = 0
        self.flag = self.board_dict.get("flag")
        self.button_list = []
        self.time_continue = True
        self.flag_list = []
        self.widget_show()  # 展示扫雷棋盘组件

    def widget_show(self):  # 展示扫雷棋盘各组件
        self.frame2=tk.Frame(self.tk)
        self.frame2_1=tk.Frame(self.frame2)
        self.label2_1_1=tk.Label(self.frame2_1, text=f"红旗数:{self.flag}", font=setting.BOARD_FONT, width=10)
        self.label2_1_1.grid(row=0, column=0)
        self.button2_1_1=tk.Button(self.frame2_1, image=self.image_dict.get("face")[0], command=self.once_again)
        self.button2_1_1.grid(row=0, column=1)
        self.label2_1_2=tk.Label(self.frame2_1, text=f"用时:{self.time}", font=setting.BOARD_FONT, width=10)
        self.label2_1_2.grid(row=0, column=2)
        self.frame2_1.pack()
        self.frame2_2=tk.Frame(self.frame2)
        # 展示扫雷棋盘
        for i in range(self.board_dict.get("row")):
            temp_list=[]
            for j in range(self.board_dict.get("col")):
                temp=tk.Button(self.frame2_2, image=self.image_dict["normal"], command=lambda x=i, y=j :self.button_show(x, y))
                temp.grid(row=i,column=j)
                temp.bind("<Button-3>",lambda event,x=i,y=j:self.flag_show_or_cancel(x,y))  # 绑定鼠标右键事件到插旗函数上
                temp_list.append(temp)
            self.button_list.append(temp_list)  # 将棋盘组件放到按钮列表中
        self.frame2_2.pack()
        self.frame2.pack()
        self.tk.after(1000,self.time_counter)  # 开始计时
    def once_again(self):  # 重新开始扫雷的函数
        self.frame2.destroy()  # 销毁扫雷棋盘的组件
        if self.time_continue:  # 判断当前重新开始时,计时器是否正常计时
            self.is_once_again=True  # 设置成刚重新开始过的状态
        self.start()  # 进入初始化函数
    def time_counter(self):  # 计时函数
        if self.time_continue:   # 判断是否继续即使
            if not self.is_once_again:  # 判断是否在上一次计时未结束时重新开始
                self.time+=1
                self.label2_1_2.config(text=f"用时:{self.time}")  # 将当前用时显示在扫雷棋盘上
                self.tk.after(1000,self.time_counter)   # 重新开始下一次计时
            else:
                self.is_once_again=False
    def button_show(self,x,y):  # 展示棋盘排查结果
        if self.board1[x+1][y+1]==1:  # 判断是否触雷
            self.game_over(x,y)  # 执行游戏结束函数
        else:
            self.blank_show(x, y)  # 将安全位置的周围雷数显示
            if self.is_win():  # 判断是否排查完扫雷棋盘
                self.game_win()  # 执行游戏胜利函数
    def flag_show_or_cancel(self,x,y):  # 红旗放置和撤销函数
        if (x,y) not in self.flag_list:  # 判断该位置是否有红旗
            if self.flag>0:  # 判断是否还有可使用的棋子
                self.flag-=1
                self.flag_list.append((x,y))  # 将该红旗位置记录到数据列表中
                self.button_list[x][y].config(image=self.image_dict["flag"])  # 替换该位置的按钮图片
        else:  # 撤销红旗操作
            self.flag+=1
            self.flag_list.pop(self.flag_list.index((x,y)))  # 将数据列表中该红旗的位置信息移除
            self.button_list[x][y].config(image=self.image_dict["normal"])  # 替换该位置的按钮图片
        self.label2_1_1.config(text=f"红旗数:{self.flag}")  # 更新红旗数据到扫雷棋盘的组件中
    def game_over(self,x,y):  # 游戏结束执行函数
        self.time_continue=False  # 停止计时
        for i in range(self.board_dict.get("row")):
            for j in range(self.board_dict.get("col")):
                self.button_list[i][j].config(command=lambda :None)  # 将棋盘的所有按钮执行函数撤销
                self.button_list[i][j].unbind("<Button-3>")  # 解除所有按钮的绑定鼠标右键的事件
                if self.board1[i+1][j+1]==1:
                    self.button_list[i][j].config(image=self.image_dict.get("mine")[0])  # 将棋盘中有雷的位置的按钮图标换成雷图标
        self.button2_1_1.config(image=self.image_dict.get("face")[1])  # 替换重新开始的按钮图像
        self.button_list[x][y].config(image=self.image_dict.get("mine")[1])  # 展示触雷位置的特殊雷图标
    def is_win(self):  # 判断是否胜利的执行函数
        for i in range(self.board_dict.get("row")):
            for j in range(self.board_dict.get("col")):
                if self.board1[i+1][j+1]==0 and self.board3[i+1][j+1]=="*":  # 判断是否有非雷位置没排查
                    return False
        return True
    def game_win(self):  # 游戏胜利的执行函数
        self.time_continue=False  # 停止计时
        for i in range(self.board_dict.get("row")):
            for j in range(self.board_dict.get("col")):
                self.button_list[i][j].config(command=lambda :None)  # 将棋盘的所有按钮执行函数撤销
                self.button_list[i][j].unbind("<Button-3>")  # 解除所有按钮的绑定鼠标右键的事件
                if self.board1[i+1][j+1]==1:
                    self.button_list[i][j].config(image=self.image_dict.get("mine")[0])  # 将棋盘中有雷的位置的按钮图标换成雷图标
        self.button2_1_1.config(image=self.image_dict.get("face")[2])  # 替换重新开始的按钮图像
        if self.using=="简单":  # 判断是否刷新当前难度的纪录
            if self.score_dict["easy"]==0:  # 判断该难度是否有通关记录
                self.score_dict["easy"]=self.time
            else:
                if self.time<self.score_dict.get("easy"):  # 判断是否刷新记录
                    self.score_dict["easy"]=self.time
        elif self.using=="普通":
            if self.score_dict["normal"]==0:  # 判断该难度是否有通关记录
                self.score_dict["normal"]=self.time
            else:
                if self.time < self.score_dict.get("normal"):  # 判断是否刷新记录
                    self.score_dict["normal"]=self.time
        elif self.using=="困难":
            if self.score_dict["trouble"]==0:  # 判断该难度是否有通关记录
                self.score_dict["trouble"]=self.time
            else:
                if self.time < self.score_dict.get("trouble"):  # 判断是否刷新记录
                    self.score_dict["trouble"]=self.time


    def blank_show(self, x, y):  # 显示安全区域的周围雷数的执行函数
        # 判断是否越界(递归空白展开时会用到)
        if x<0 or y<0:
            return None
        elif x>=self.board_dict.get("row") or y>=self.board_dict.get("col"):  # 判断是否越界(递归空白展开时会用到)
            return None
        elif self.board3[x+1][y+1]==' ':  # 判断是否已排查
            return None
        else:  # 显示棋盘安全区域
            if self.board1[x+1][y+1]==0:  # 只对非雷区域处理(递归空白展开时会有扫描到雷区的情况)
                self.board3[x+1][y+1]=' '  # 排查当前区域
                self.button_list[x][y].grid_forget()   # 取下该位置的按钮
                temp=tk.Label(self.frame2_2, image=self.image_dict.get("safe")[self.board2[x + 1][y + 1]])
                temp.grid(row=x,column=y)  # 放置记录周围雷数的标签
                if (x, y) in self.flag_list:  # 判断排查的区域上是否有红旗
                    self.flag += 1  # 回收红旗
                    self.flag_list.pop(self.flag_list.index((x, y)))  # 将该红旗位置从数据列表中删除
                    self.label2_1_1.config(text=f"红旗数:{self.flag}")  # 将可用红旗数据同步到扫雷棋盘中
                if self.board2[x+1][y+1]==0:  # 判断排查的区域周围是否无雷
                    # 如果无雷则将周围自动排查一遍(遇到空白则将该空白周围也自动排查一遍)[递归]
                    self.blank_show(x + 1, y)
                    self.blank_show(x, y + 1)
                    self.blank_show(x + 1, y + 1)
                    self.blank_show(x - 1, y)
                    self.blank_show(x, y - 1)
                    self.blank_show(x - 1, y - 1)
                    self.blank_show(x + 1, y - 1)
                    self.blank_show(x - 1, y + 1)
    def board_set(self):  # 显示扫雷设置界面
        self.time_continue=False  # 停止计时
        if not self.is_menu_set_window_show:  # 判断是否从扫雷游戏期间进入设置界面
            self.frame2.destroy()  # 销毁扫雷棋盘
        else:  # 从扫雷游戏开始界面进入设置界面
            self.frame1.destroy()  # 销毁扫雷开始界面组件
        self.style = ttk.Style(self.tk)  # 设置ttk组件的工具对象
        self.frame3=tk.Frame(self.tk)
        self.frame3_1=tk.Frame(self.frame3)
        self.label3_1_1=tk.Label(self.frame3_1, text="难度", font=setting.BOARD_FONT)
        self.label3_1_1.grid(row=0, column=0)
        self.board_var=tk.Variable(value=self.using)
        self.label3_1_2=tk.Label(self.frame3_1, width=10)
        self.label3_1_2.grid(row=0, column=1)
        self.style.configure("TMenubutton",font=setting.BOARD_FONT)  # 设置该类和子类组件的字体
        self.opt_menu3_1_1=ttk.OptionMenu(self.frame3_1, self.board_var,
                                          self.using, *["简单","普通","困难","自定义"], command=self.board_replace)
        self.opt_menu3_1_1.grid(row=0, column=2)
        self.frame3_1.pack()
        self.label3_1=tk.Label(self.frame3, text="行数:", font=setting.BOARD_FONT, anchor="w", width=20)
        self.label3_1.pack()
        self.entry3_1=ttk.Entry(self.frame3, justify="right", font=setting.BOARD_FONT)
        self.entry3_1.pack()
        self.label3_2 = tk.Label(self.frame3, text="列数:", font=setting.BOARD_FONT, anchor="w", width=20)
        self.label3_2.pack()
        self.entry3_2 = ttk.Entry(self.frame3, justify="right", font=setting.BOARD_FONT)
        self.entry3_2.pack()
        self.label3_3 = tk.Label(self.frame3, text="雷数:", font=setting.BOARD_FONT, anchor="w", width=20)
        self.label3_3.pack()
        self.entry3_3 = ttk.Entry(self.frame3, justify="right", font=setting.BOARD_FONT)
        self.entry3_3.pack()
        self.frame3_2=tk.Frame(self.frame3)
        self.style.configure("TButton",font=setting.BOARD_FONT)  # 设置该类和子类组件的字体
        self.button3_2_1=ttk.Button(self.frame3_2, text="完成", command=self.set_true)
        self.button3_2_1.grid(row=0, column=0)
        self.label3_2_1=tk.Label(self.frame3_2, width=10)
        self.label3_2_1.grid(row=0, column=1)
        self.button3_2_2=ttk.Button(self.frame3_2, text="取消", command=self.set_return)
        self.button3_2_2.grid(row=0, column=2)
        self.frame3_2.pack()
        self.frame3.pack()
        # 插入当前使用棋盘的数据
        self.entry3_1.insert("end", str(self.board_dict.get("row")))
        self.entry3_2.insert("end", str(self.board_dict.get("col")))
        self.entry3_3.insert("end", str(self.board_dict.get("boom")))
        if self.using!="自定义":  # 判断当前是否是自定义模式
            # 非自定义模式下棋盘数据由各难度模式决定,因此禁用棋盘数据修改框
            self.entry3_1.configure(state="disable")
            self.entry3_2.configure(state="disable")
            self.entry3_3.configure(state="disable")
    def board_replace(self,x):  # 修改棋盘数据框的执行函数
        # 解除文本输入框的禁用状态
        self.entry3_1.configure(state="normal")
        self.entry3_2.configure(state="normal")
        self.entry3_3.configure(state="normal")
        # 删除文本输入框的旧数据
        self.entry3_1.delete(0, "end")
        self.entry3_2.delete(0, "end")
        self.entry3_3.delete(0, "end")
        # 根据选择的不同模式插入对应数据
        if x=="简单":
            self.entry3_1.insert("end", "9")
            self.entry3_2.insert("end", "9")
            self.entry3_3.insert("end", "10")
        elif x=="普通":
            self.entry3_1.insert("end", "16")
            self.entry3_2.insert("end", "16")
            self.entry3_3.insert("end", "40")
        elif x=="困难":
            self.entry3_1.insert("end", "16")
            self.entry3_2.insert("end", "30")
            self.entry3_3.insert("end", "99")
        if x!="自定义":
            # 自定义模式的数据有玩家决定,此时玩家可修改文本输入框,其余模式在自动修改数据后均再次禁用次文本输入框防止玩家修改
            self.entry3_1.configure(state="disable")
            self.entry3_2.configure(state="disable")
            self.entry3_3.configure(state="disable")
    def set_true(self):  # 确定修改棋盘数据的执行函数
        try:
            # 判断数据是否合法(玩家的输入可能非法)
            row = int(self.entry3_1.get())
            col = int(self.entry3_2.get())
            booms = int(self.entry3_3.get())
            flags = int(self.entry3_3.get())
        except Exception:
            # 非法弹出警告消息框提醒玩家数据不合法
            messagebox.showerror(title="错误",message="请输入合法的自定义数据!")
        else:
            # 合法则更新到棋盘数据存放位置中
            self.using = self.board_var.get()
            self.board_dict["row"]=row
            self.board_dict["col"]=col
            self.board_dict["boom"]=booms
            self.board_dict["flag"]=flags
            self.frame3.destroy()
            if self.is_menu_set_window_show:  # 判断是否从游戏开始界面进入设置界面
                self.show_start_window()  # 进入游戏开始界面
            else:  # 不是则从游戏期间进入的设置界面
                self.start()  # 进入初始化函数(重新开始游戏)
    def set_return(self):  # 不修改数据直接返回的执行函数
        self.frame3.destroy()
        if self.is_menu_set_window_show:  # 判断是否从游戏开始界面进入设置界面
            self.show_start_window()  # 进入游戏开始界面
        else:  # 不是则从游戏期间进入的设置界面
            self.start()  # 进入初始化函数(重新开始游戏)