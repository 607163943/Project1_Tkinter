import tkinter as tk
import setting
from tkinter import scrolledtext
import sum_widget
class Window:
    def __init__(self):
        self.tk=tk.Tk()
        self.using_sum=None
        self.using_sum_name=None
        self.menu()
    def menu(self):
        self.menu_base=tk.Menu(self.tk)
        self.sum_menu_base=tk.Menu(self.tk,tearoff=False)
        self.sum_var=tk.Variable(value="计算器")
        self.menu_base.add_cascade(label="计算器",menu=self.sum_menu_base)
        temp_tuple=("计算器","科学计算器")
        for i in temp_tuple:
            self.sum_menu_base.add_radiobutton(label=i,variable=self.sum_var,command=self.select_sum)
        self.menu_base.add_command(label="帮助",command=lambda :self.help_or_logging('help.txt','帮助'))
        self.menu_base.add_command(label="日志",command=lambda :self.help_or_logging('logging.txt','日志'))
        self.tk.config(menu=self.menu_base)
        self.select_sum()
    def select_sum(self):
        if self.using_sum_name!=self.sum_var.get():
            if self.using_sum:
                self.using_sum.widget_replace()
                del self.using_sum
                self.using_sum=None
            match self.sum_var.get():
                case "计算器":
                    self.using_sum=sum_widget.Sum_Widget1(self.tk)
                case "科学计算器":
                    self.using_sum=sum_widget.Sum_Widget2(self.tk)
            self.using_sum_name=self.sum_var.get()

    def help_or_logging(self,filename:str,title:str):
        self.top=tk.Toplevel(self.tk)
        self.top.title(title)
        self.top_scr=scrolledtext.ScrolledText(self.top,width=100)
        self.top_scr.pack()
        with open(filename,mode="r+",encoding="UTF-8")as f:
            self.top_scr.insert("1.0",f.read())
    def show(self):
        self.tk.mainloop()