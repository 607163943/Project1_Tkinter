import tkinter as tk
from tkinter import scrolledtext
import setting
import board
class Window:  # 窗口类
    def __init__(self):
        self.tk=tk.Tk()
        self.tk.title(setting.TITLE)  # 设置窗口标题
        self.menu()  # 设置窗口菜单
        self.board=board.Board(self.tk)    # 生成扫雷组件类对象
        self.board.show_start_window()   # 展示扫雷开始界面
    def menu(self):   # 设置窗口菜单函数
        self.menu_base=tk.Menu(self.tk)  # 设置主窗口菜单栏
        self.menu_base.add_command(label="设置",command=self.set)
        self.menu_base.add_command(label="帮助",command=lambda :self.help_or_logging("help.txt","帮助"))
        self.menu_base.add_command(label="日志",command=lambda :self.help_or_logging("logging.txt","日志"))
        self.set_menu_base=tk.Menu(self.tk)    # 设置设置界面窗口菜单栏
        self.tk.config(menu=self.menu_base)   # 放置主窗口菜单栏
    def set(self):  # 进入窗口设置界面
        self.board.board_set()
    def help_or_logging(self,filename:str,title:str):   # 帮助和日志菜单项执行函数
        self.top=tk.Toplevel(self.tk)  # 生成子窗口
        self.top.title(title)   # 设置子窗口标题
        self.top_scr=scrolledtext.ScrolledText(self.top,font=setting.SCR_FONT)   # 生成滚滚动式多文本输入框
        self.top_scr.pack()   # 放置滚动式文本输入框
        with open(filename,mode="r+",encoding="UTF-8")as f:
            self.top_scr.insert("1.0",f.read())  # 插入在文本框首行首列插入读取的文件内容
    def show(self):   # 展示主窗口界面
        self.tk.mainloop()