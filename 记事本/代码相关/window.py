# python内置模块
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import colorchooser
from os import path
import tkinter as tk
import time
import json
# 编写的python模块
import setting

class Window:
    # 初始化窗口对象数据
    def __init__(self):
        self.tk=tk.Tk()
        # 设置窗口标题
        self.tk.title(setting.TITLE)
        # 设置窗口大小
        self.tk.geometry(setting.WIDTH_AND_HEIGHT)
        # 记录窗口大小数据
        self.width = setting.WIDTH
        self.height = setting.HEIGHT
        self.file_path=None  # 当前保存的文件路径(None就是没有打开文件)
        self.style=ttk.Style(self.tk)  # 设置ttk组件通用样式的工具对象
        # 存放记事本使用的字体类型
        self.font_dict={}
        # 存放记事本使用的字体数据
        self.font_list=[]
        # 存放字体颜色
        self.font_color=""
        # 加载部分json数据
        self.load_json_data()
        self.menu()
        self.widget_show()
        # 记录记事本字体名,大小数据
        self.font_var = tk.Variable(value=self.font_list[0])
        self.size_var = tk.Variable(value=str(self.font_list[1]))
        # 设置字体名,大小变量的触发函数(触发条件:变量值改变)
        self.font_var.trace_add("write",lambda *args: self.font_replace())
        self.size_var.trace_add("write", lambda *args: self.font_replace())
        # 记录记事本字体类型数据
        self.bold_var = tk.Variable(value=self.font_dict.get("bold"))
        self.italic_var = tk.Variable(value=self.font_dict.get("italic"))
        self.underline_var = tk.Variable(value=self.font_dict.get("underline"))
        self.overstrick_var = tk.Variable(value=self.font_dict.get("overstrike"))
        # 将加载的初始字体类型渲染到记事本组件的字体中
        self.font_replace(True)
        self.tk.bind("<Configure>",self.replace_root_and_book)
    # 加载json数据
    def load_json_data(self):
        dir_data_base=""
        dir_data_path=path.join(dir_data_base,"data")
        with open(path.join(dir_data_path,"font.json"),mode="r+",encoding="UTF-8")as f:
            # 将json文件中的全部数据取出
            font_dict=json.load(f)
            # 依据json数据设置初始记事本使用字体的数据
            self.font_list = [font_dict.get("name"),font_dict.get("size")]
            # 依据json数据设置初始字体的类型
            self.font_dict=font_dict.get("font_style")
            self.font_color=font_dict.get("font_color")

    # 设置窗口菜单
    def menu(self):
        self.menu_base=tk.Menu(self.tk)  # 生成记事本界面根菜单栏
        self.file_menu=tk.Menu(self.menu_base,tearoff=False)  # 生成字体子菜单栏
        self.editor_menu=tk.Menu(self.menu_base,tearoff=False)  # 生成编辑子菜单栏
        self.menu_base.add_cascade(label="文件",menu=self.file_menu)   # 生成文件菜单下拉项
        self.file_menu.add_command(label="打开",command=lambda :self.file("打开"))
        self.file_menu.add_command(label="保存",command=lambda :self.file("保存"))
        self.file_menu.add_command(label="另存为",command=lambda :self.file("另存为"))
        self.menu_base.add_cascade(label="编辑",menu=self.editor_menu)  # 生成编辑菜单下拉项
        self.editor_menu.add_command(label="日期/时间",command=lambda :self.editor("日期/时间"))
        self.editor_menu.add_command(label="字体",command=lambda :self.editor("字体"))
        self.menu_base.add_command(label="帮助",command=lambda :self.help_or_logging("help.txt","帮助"))
        self.menu_base.add_command(label="日志",command=lambda :self.help_or_logging("logging.txt","日志"))
        self.font_menu_base=tk.Menu(self.tk)  # 生成字体编辑界面的根菜单栏
        self.font_menu_base.add_command(label="返回",command=self.font_return)
        self.tk.config(menu=self.menu_base)  # 显示记事本界面根菜单栏

    # 文件菜单项执行函数
    def file(self,mode:str):
        if mode=="打开":
            file_path=filedialog.askopenfilename(title="打开")  # 弹出文件对话框指定一个文件返回对应路径
            if file_path:
                try:
                    f=open(file_path,mode="r+",encoding="UTF-8")
                    self.scr.delete("1.0","end")
                    self.scr.insert("1.0",f.read())
                    self.file_path=file_path  # 记录打开的文件路径
                except Exception as e:
                    print(e)
                    messagebox.showerror(title="错误",message="打开文件失败!")  # 弹出错误消息框
        else:
            if mode=="保存" and self.file_path:
                with open(self.file_path,mode="w+",encoding="UTF-8")as f:
                    f.write(self.scr.get("1.0","end"))
            else:
                file_path=filedialog.asksaveasfilename(title="另存为")  # 弹出文件对话框指定一个文件保存路径
                if file_path:
                    with open(file_path,mode="w+",encoding="UTF-8")as f:
                        f.write(self.scr.get("1.0","end"))
                    self.file_path=file_path  # 记录打开的文件路径

    # 编辑菜单项执行函数
    def editor(self,mode:str):
        if mode=="日期/时间":
            self.scr.insert("end",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))  # 在记事本编辑界面
                                                                                                    # 末尾插入当前时间
        else:  # 进入字体编辑界面
            self.tk.config(menu=self.font_menu_base)
            self.scr.pack_forget()   # 取下记事本相关组件(没有销毁，写道文字还在，还可以放上去)
            self.font_widget_show()  # 展示字体编辑界面的组件

    # 帮助和日志菜单项执行函数
    def help_or_logging(self,filename:str,title:str):
        self.top=tk.Toplevel(self.tk)  # 生成一个子窗口
        self.top.title(title)  # 设置子窗口标题
        self.top_scr=scrolledtext.ScrolledText(self.top,font=setting.TOP_SCR_FONT)  # 生成滚动式多行文本输入框
        self.top_scr.pack()
        with open(filename,mode="r+",encoding="UTF-8")as f:
            self.top_scr.insert("1.0",f.read())

    # 展示记事本界面组件
    def widget_show(self):
        self.scr=scrolledtext.ScrolledText(self.tk,font=self.font_list,fg=self.font_color,
                                           width=setting.SCR_WIDTH,height=setting.SCR_HEIGHT)
        self.scr.pack()

    # 展示字体编辑界面

    def font_widget_show(self):
        self.frame1=tk.Frame(self.tk)
        self.frame1_1=tk.Frame(self.frame1)
        self.label1_1_1=tk.Label(self.frame1_1,text="字体名:",font=setting.FONT_SET)
        self.label1_1_1.grid(row=0,column=0)
        self.com_box1_1_1=ttk.Combobox(self.frame1_1,font=setting.FONT_SET,textvariable=self.font_var,
                                     values=(font.names()+font.families()),justify="right")  # 设置下拉菜单式文本输入框
        self.com_box1_1_1.grid_configure(row=0,column=1)
        self.label1_1_2=tk.Label(self.frame1_1,text="字体大小:",font=setting.FONT_SET)
        self.label1_1_2.grid(row=1,column=0)
        self.com_box1_1_2=ttk.Combobox(self.frame1_1,font=setting.FONT_SET,textvariable=self.size_var,
                                       values=([str(i) for i in range(8,17)]+
                                            [str(i) for i in range(18,27,2)]),justify="right")  # 设置下拉菜单式文本输入框
        self.com_box1_1_2.grid_configure(row=1,column=1)
        self.frame1_1.pack()
        self.frame1_2=tk.Frame(self.frame1)
        self.style.configure("TCheckbutton",font=setting.FONT_SET)  # 设置ttk复选框的通用字体样式
        self.checkbutton1_2_1=ttk.Checkbutton(self.frame1_2,text="加粗",
                                              onvalue=True,offvalue=False,variable=self.bold_var,
                                              command=self.font_replace)
        self.checkbutton1_2_1.grid(row=0,column=0)
        self.checkbutton1_2_1 = ttk.Checkbutton(self.frame1_2, text="斜体",
                                                onvalue=True,offvalue=False,variable=self.italic_var,
                                                command=self.font_replace)
        self.checkbutton1_2_1.grid(row=0, column=1)
        self.checkbutton1_2_1 = ttk.Checkbutton(self.frame1_2, text="下划线",
                                                onvalue=True,offvalue=False,variable=self.underline_var,
                                                command=self.font_replace)
        self.checkbutton1_2_1.grid(row=1, column=0)
        self.checkbutton1_2_1 = ttk.Checkbutton(self.frame1_2, text="删除线",
                                                onvalue=True,offvalue=False,variable=self.overstrick_var,
                                                command=self.font_replace)
        self.checkbutton1_2_1.grid(row=1, column=1)
        self.frame1_2.pack()
        self.label1_1=tk.Label(self.frame1,text="字体颜色",font=setting.FONT_SET,height=2)
        self.label1_1.pack()
        self.style.configure("button1_1.TButton",font=setting.FONT_SET)  # 设置ttk按钮通用字体
        self.button1_1=ttk.Button(self.frame1,text="设置字体颜色",command=self.font_color_replace,
                                  style="button1_1.TButton")
        self.button1_1.pack()
        self.label1_2=tk.Label(self.frame1,text="这是一个示例文本",height=2,
                               font=self.font_list)
        self.label1_2.pack()
        self.frame1.pack()

    # 字体样式设置函数
    def font_replace(self,is_start=False):
        self.font_list=[self.font_var.get(),int(self.size_var.get())]  # 获取当前字体的样式
        if self.bold_var.get():
            self.font_list.append("bold")
            self.font_dict["bold"]=True
        else:
            self.font_dict["bold"] = False
        if self.italic_var.get():
            self.font_list.append("italic")
            self.font_dict["italic"] = True
        else:
            self.font_dict["italic"] = False
        if self.underline_var.get():
            self.font_list.append("underline")
            self.font_dict["underline"] = True
        else:
            self.font_dict["underline"] = False
        if self.overstrick_var.get():
            self.font_list.append("overstrike")
            self.font_dict["overstrike"] = True
        else:
            self.font_dict["overstrike"] = False
        if not is_start:
            self.label1_2.config(font=self.font_list)
        self.scr.config(font=self.font_list)  # 将新的字体样式同步到记事本界面的字体中

    # 字体颜色设置函数
    def font_color_replace(self):
        color_tuple=colorchooser.askcolor(title="字体颜色设置")   # 指定一个字体颜色
        if color_tuple[1]:  # 判断是否指定字体颜色(取消为None)
            self.font_color=str(color_tuple[1])
            self.label1_2.config(fg=self.font_color)
            self.scr.config(fg=self.font_color)

    # 字体界面返回到记事本编辑界面
    def font_return(self):
        # 销毁字体编辑界面组件
        self.frame1.destroy()
        # 换回记事本界面的根菜单栏
        self.tk.config(menu=self.menu_base)
        # 重新放置记事本组件
        self.scr.pack()
        # 将设置好的字体数据更新到json数据文件中
        self.update_json_data()

    # 将新设置好的字体数据更新到json文件中
    def update_json_data(self):
        dir_data_base = ""
        dir_data_path = path.join(dir_data_base, "data")
        font_dict = {"name": self.font_list[0], "size": self.font_list[1],
                     "font_style":self.font_dict,"font_color":self.font_color}
        with open(path.join(dir_data_path, "font.json"), mode="w+", encoding="UTF-8") as f:
            json.dump(font_dict, f)
    # 设置窗口和记事本组件同步窗口大小的变化
    def replace_root_and_book(self,event=None):
        # 获取改变后的窗口大小
        width,height=self.get_root_size()
        # 将新窗口大小数据同步到记事本组件上
        self.set_book_size(width,height)

    # 获取当前窗口大小的函数
    def get_root_size(self) ->list[int]:
        return [self.tk.winfo_width(),self.tk.winfo_height()]

    # 设置记事本组件的大小
    def set_book_size(self,width,height):
        self.scr.configure(width=width,height=height)

    # 显示窗口
    def show(self):
        self.tk.mainloop()