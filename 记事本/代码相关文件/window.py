import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import colorchooser
import setting
import time
class Window:
    def __init__(self):
        self.tk=tk.Tk()
        self.tk.title(setting.TITLE)
        self.width = 0
        self.height = 0
        self.file_path=None
        self.style=ttk.Style(self.tk)
        self.font_dict={"bold":False,"italic":False,"underline":False,"overstrike":False}
        self.font_list=setting.START_FONT
        self.menu()
        self.widget_show()

    def menu(self):
        self.menu_base=tk.Menu(self.tk)
        self.file_menu=tk.Menu(self.menu_base,tearoff=False)
        self.editor_menu=tk.Menu(self.menu_base,tearoff=False)
        self.menu_base.add_cascade(label="文件",menu=self.file_menu)
        self.file_menu.add_command(label="打开",command=lambda :self.file("打开"))
        self.file_menu.add_command(label="保存",command=lambda :self.file("保存"))
        self.file_menu.add_command(label="另存为",command=lambda :self.file("另存为"))
        self.menu_base.add_cascade(label="编辑",menu=self.editor_menu)
        self.editor_menu.add_command(label="日期/时间",command=lambda :self.editor("日期/时间"))
        self.editor_menu.add_command(label="字体",command=lambda :self.editor("字体"))
        self.menu_base.add_command(label="帮助",command=lambda :self.help_or_logging("help.txt","帮助"))
        self.menu_base.add_command(label="日志",command=lambda :self.help_or_logging("logging.txt","日志"))
        self.font_menu_base=tk.Menu(self.tk)
        self.font_menu_base.add_command(label="返回",command=self.font_return)
        self.tk.config(menu=self.menu_base)
    def file(self,mode:str):
        if mode=="打开":
            file_path=filedialog.askopenfilename(title="打开")
            if file_path:
                try:
                    f=open(file_path,mode="r+",encoding="UTF-8")
                    self.scr.delete("1.0","end")
                    self.scr.insert("1.0",f.read())
                    self.file_path=file_path
                except Exception:
                    messagebox.showerror(title="错误",message="打开文件失败!")
        else:
            if mode=="保存" and self.file_path:
                with open(self.file_path,mode="w+",encoding="UTF-8")as f:
                    f.write(self.scr.get("1.0","end"))
            else:
                file_path=filedialog.asksaveasfilename(title="另存为")
                if file_path:
                    with open(file_path,mode="w+",encoding="UTF-8")as f:
                        f.write(self.scr.get("1.0","end"))
                    self.file_path=file_path
    def editor(self,mode:str):
        if mode=="日期/时间":
            self.scr.insert("end",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        else:
            self.tk.config(menu=self.font_menu_base)
            self.scr.pack_forget()
            self.font_widget_show()
    def help_or_logging(self,filename:str,title:str):
        self.top=tk.Toplevel(self.tk)
        self.top.title(title)
        self.top_scr=scrolledtext.ScrolledText(self.top,width=100)
        self.top_scr.pack()
        with open(filename,mode="r+",encoding="UTF-8")as f:
            self.top_scr.insert("1.0",f.read())
    def widget_show(self):
        self.scr=scrolledtext.ScrolledText(self.tk,font=self.font_list)
        self.scr.pack()

    def font_widget_show(self):
        """
        显示字体编辑界面
        :return:
        """
        self.frame1=tk.Frame(self.tk)
        self.frame1_1=tk.Frame(self.frame1)
        self.label1_1_1=tk.Label(self.frame1_1,text="字体名:",font=setting.FONT_SET)
        self.label1_1_1.grid(row=0,column=0)
        self.style.configure("TMenubutton",font=setting.FONT_SET)
        self.font_var=tk.Variable(value=self.font_list[0])
        self.font_var.trace_add("write",lambda *args:self.font_replace())
        self.com_box1_1_1=ttk.Combobox(self.frame1_1,font=setting.FONT_SET,textvariable=self.font_var,
                                     values=(font.names()+font.families()),justify="right")
        self.com_box1_1_1.grid_configure(row=0,column=1)
        self.label1_1_2=tk.Label(self.frame1_1,text="字体大小:",font=setting.FONT_SET)
        self.label1_1_2.grid(row=1,column=0)
        self.size_var=tk.Variable(value=str(self.font_list[1]))
        self.size_var.trace_add("write",lambda *args:self.font_replace())
        self.com_box1_1_2=ttk.Combobox(self.frame1_1,font=setting.FONT_SET,textvariable=self.size_var,
                                       values=([str(i) for i in range(8,17)]+
                                            [str(i) for i in range(18,27,2)]),justify="right")
        self.com_box1_1_2.grid_configure(row=1,column=1)
        self.frame1_1.pack()
        self.frame1_2=tk.Frame(self.frame1)
        self.style.configure("TCheckbutton",font=setting.FONT_SET)
        self.bold_var=tk.Variable(value=self.font_dict.get("bold"))
        self.checkbutton1_2_1=ttk.Checkbutton(self.frame1_2,text="加粗",
                                              onvalue=True,offvalue=False,variable=self.bold_var,
                                              command=self.font_replace)
        self.checkbutton1_2_1.grid(row=0,column=0)
        self.italic_var=tk.Variable(value=self.font_dict.get("italic"))
        self.checkbutton1_2_1 = ttk.Checkbutton(self.frame1_2, text="斜体",
                                                onvalue=True,offvalue=False,variable=self.italic_var,
                                                command=self.font_replace)
        self.checkbutton1_2_1.grid(row=0, column=1)
        self.underline_var=tk.Variable(value=self.font_dict.get("underline"))
        self.checkbutton1_2_1 = ttk.Checkbutton(self.frame1_2, text="下划线",
                                                onvalue=True,offvalue=False,variable=self.underline_var,
                                                command=self.font_replace)
        self.checkbutton1_2_1.grid(row=1, column=0)
        self.overstrick_var=tk.Variable(value=self.font_dict.get("overstrike"))
        self.checkbutton1_2_1 = ttk.Checkbutton(self.frame1_2, text="删除线",
                                                onvalue=True,offvalue=False,variable=self.overstrick_var,
                                                command=self.font_replace)
        self.checkbutton1_2_1.grid(row=1, column=1)
        self.frame1_2.pack()
        self.label1_1=tk.Label(self.frame1,text="字体颜色",font=setting.FONT_SET,height=2)
        self.label1_1.pack()
        self.style.configure("button1_1.TButton",font=setting.FONT_SET)
        self.button1_1=ttk.Button(self.frame1,text="设置字体颜色",command=self.font_color_replace,
                                  style="button1_1.TButton")
        self.button1_1.pack()
        self.label1_2=tk.Label(self.frame1,text="这是一个示例文本",height=2,
                               font=self.font_list)
        self.label1_2.pack()
        self.frame1.pack()
    def font_replace(self,*args):
        self.font_list=[self.font_var.get(),int(self.size_var.get())]
        if self.bold_var.get():
            self.font_list.append("bold")
            self.font_dict["bold"]=True
        if self.italic_var.get():
            self.font_list.append("italic")
            self.font_dict["italic"] = True
        if self.underline_var.get():
            self.font_list.append("underline")
            self.font_dict["underline"] = True
        if self.overstrick_var.get():
            self.font_list.append("overstrike")
            self.font_dict["overstrike"] = True
        self.label1_2.config(font=self.font_list)
        self.scr.config(font=self.font_list)
    def font_color_replace(self):
        color_tuple=colorchooser.askcolor(title="字体颜色设置")
        if color_tuple[1]:
            temp=str(color_tuple[1])
            self.label1_2.config(fg=temp)
            self.scr.config(fg=temp)
    def font_return(self):
        self.frame1.destroy()
        self.tk.config(menu=self.menu_base)
        self.scr.pack()
    def get_root_size(self):
        """
        获取窗口大小并固定该窗口的大小
        :return:
        """
        self.width=self.tk.winfo_width()
        self.height=self.tk.winfo_height()
        self.tk.geometry(f"{self.width}x{self.height}")
    def show(self):
        self.tk.after(1000,self.get_root_size)  # 设置延迟获取组件显示后的窗口大小
        self.tk.mainloop()