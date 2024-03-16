import tkinter as tk
from tkinter import scrolledtext
import setting
import board
class Window:
    def __init__(self):
        self.tk=tk.Tk()
        self.tk.title(setting.TITLE)
        self.menu()
        self.board=board.Board(self.tk)
        self.board.show_start_window()
    def menu(self):
        self.menu_base=tk.Menu(self.tk)
        self.menu_base.add_command(label="设置",command=self.set)
        self.menu_base.add_command(label="帮助",command=lambda :self.help_or_logging("help.txt","帮助"))
        self.menu_base.add_command(label="日志",command=lambda :self.help_or_logging("logging.txt","日志"))
        self.set_menu_base=tk.Menu(self.tk)
        self.tk.config(menu=self.menu_base)
    def set(self):
        self.board.board_set()
    def help_or_logging(self,filename:str,title:str):
        self.top=tk.Toplevel(self.tk)
        self.top.title(title)
        self.top_scr=scrolledtext.ScrolledText(self.top,font=setting.SCR_FONT)
        self.top_scr.pack()
        with open(filename,mode="r+",encoding="UTF-8")as f:
            self.top_scr.insert("1.0",f.read())
    def show(self):
        self.tk.mainloop()