import tkinter as tk
from tkinter import scrolledtext
import setting
import game
from tkinter import ttk
class Window:  # 游戏窗口类
    def __init__(self):
        self.tk=tk.Tk()
        self.tk.title(setting.TITLE)  # 设置主窗口标题
        self.menu()   # 设置主窗口菜单
        self.game=game.Game(self.tk)   # 实例化游戏组件类对象
        self.game.show_start_game()  # 显示游戏类的开始界面
        self.style=ttk.Style(self.tk)   # 设置ttk模块组件的工具类
    def menu(self):  # 设置窗口菜单
        self.menu_base=tk.Menu(self.tk)  # 生成主窗口根菜单栏
        self.set_menu_base=tk.Menu(self.tk)  # 生成设置根菜单栏
        self.menu_base.add_command(label="设置", command=self.set_start)
        self.menu_base.add_command(label="帮助",command=lambda :self.help_or_logging("help.txt","帮助"))
        self.menu_base.add_command(label="日志",command=lambda :self.help_or_logging("logging.txt","日志"))
        self.tk.config(menu=self.menu_base)  # 放置主窗口根菜单栏
    def set_start(self):  # 销毁进入设置界面时所在的当前界面
        if self.game.root_status=="start":
            self.game.frame1.destroy()
        elif self.game.root_status=="game":
            self.game.frame2.destroy()
            self.game.player.move_unset()
            self.game.time_is_continue = False
        else:
            self.game.frame3.destroy()
        self.tk.config(menu=self.set_menu_base)  # 放置设置界面的根菜单栏
        self.set()  # 显示设置界面
    def set(self):  # 显示设置界面函数
        self.frame1=tk.Frame(self.tk)
        self.style.configure("TMenubutton", font=setting.GAME_FONT)
        self.frame1_1=tk.Frame(self.frame1)
        self.label1_1_1=tk.Label(self.frame1_1,text="难度设置:",font=setting.GAME_FONT)
        self.label1_1_1.grid(row=0,column=0)
        self.mode_var=tk.Variable(value=self.game.mode_var_name)
        self.opt_menu1_1_1=ttk.OptionMenu(self.frame1_1,self.mode_var,self.mode_var.get(),*("简单","普通","困难"))
        self.opt_menu1_1_1.grid(row=0,column=1)
        self.frame1_1.pack(pady=20)
        self.style.configure("TButton",font=setting.GAME_FONT)  # 设置TButton类及其子类的font属性
        self.frame1_2=tk.Frame(self.frame1)
        self.button1_2_1=ttk.Button(self.frame1_2,text="确定",width=8,command=self.set_true)
        self.button1_2_1.grid(row=0,column=0)
        self.label1_2_1=tk.Label(self.frame1_2,width=5)
        self.label1_2_1.grid(row=0,column=1)
        self.button1_2_2=ttk.Button(self.frame1_2,text="取消",width=8,command=self.set_return)
        self.button1_2_2.grid(row=0,column=2)
        self.frame1_2.pack(pady=20)
        self.frame1.pack()
    def set_true(self):   # 确定修改地图难度的执行函数
        temp=self.mode_var.get()
        if temp=="简单":
            self.game.using="easy"
        elif temp=="普通":
            self.game.using="normal"
        else:
            self.game.using="trouble"
        self.game.mode_var_name=temp  # 更新选择的难度
        self.frame1.destroy()
        self.tk.config(menu=self.menu_base)  # 放置主窗口根菜单栏
        self.game.show_start_game()  # 进入游戏的开始界面
    def set_return(self):  # 不修改地图难度直接返回的执行函数
        self.frame1.destroy()
        self.tk.config(menu=self.menu_base)  # 放置主窗口根菜单栏
        self.game.show_start_game()  # 进入游戏的开始界面
    def help_or_logging(self,filename:str,title:str):  # 帮助和日志菜单项执行函数
        self.top=tk.Toplevel(self.tk)  # 生成子窗口
        self.top.title(title)  # 设置子窗口标题
        self.top_scr=scrolledtext.ScrolledText(self.top,width=100)  # 生成滚动式多行文本输入框组件
        self.top_scr.pack()
        with open(filename,mode="r+",encoding="UTF-8")as f:
            self.top_scr.insert("1.0",f.read())  # 在文本框的首行首列插入文件的文本
    def show(self):  # 主窗口显示函数
        self.tk.mainloop()  # 显示主窗口