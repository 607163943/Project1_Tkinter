# python内置模块
from tkinter import ttk
import tkinter as tk
import math
import re
# 编写的模块
import setting
class Sum_Widhet_Base:
    def __init__(self,root:tk.Tk):
        # tk主窗口(tcl解释器对象)
        self.tk=root
        self.tk.title(setting.TITLE1)
        # ttk的工具对象
        self.style=ttk.Style(self.tk)
    # 显示计算器组件
    def widget_show(self):
        pass
    # 清空表达式
    def entry_clear(self):
        pass
    # 删除表达式尾项
    def entry_pop(self):
        pass
    # 插入指定字符
    def entry_add(self,x:str):
        pass
    # 计算表达式
    def entry_sum(self,row):
        pass
    # 销毁计算器组件
    def widget_replace(self):
        pass
# 普通计算器类
class Sum_Widget1(Sum_Widhet_Base):
    # 初始化计算器对象
    def __init__(self,root:tk.Tk):
        super().__init__(root)
        self.tk.geometry("450x350")
        self.widget_show()

    # 显示计算器组件
    def widget_show(self):
        # 放置计算器输入框
        self.entry1=tk.Entry(self.tk,font=setting.SUM_WIDGET1_ENTRY_FONT,justify="right",relief=tk.FLAT)
        self.entry1.place_configure(x=60,y=18)
        self.entry2 = tk.Entry(self.tk, font=setting.SUM_WIDGET1_ENTRY_FONT,
                               justify="right",relief=tk.FLAT,insertbackground="#0033cc")
        self.entry2.place_configure(x=60, y=50)
        # 在2号输入框设置初始焦点
        self.entry2.focus_set()
        # 放置计算器计算按钮组件
        self.frame1=tk.Frame(self.tk)
        self.style.configure("clear_pop.TButton",font=setting.SUM_WIDGET1_BUTTON_FONT)
        temp=ttk.Button(self.frame1,text="清空",command=self.entry_clear,style="clear_pop.TButton",padding=[0,7])
        temp.grid_configure(row=0, column=0, columnspan=2, sticky="ew")
        temp = ttk.Button(self.frame1, text="删除", command=self.entry_pop,style="clear_pop.TButton",padding=[0,7])
        temp.grid_configure(row=0, column=2, columnspan=2, sticky="ew")
        self.style.configure("sum.TButton",font=setting.SUM_WIDGET1_BUTTON_FONT)
        for i in range(len(setting.SUM_WIDGET1)):
            for j in range(len(setting.SUM_WIDGET1[0])):
                temp = ttk.Button(self.frame1, text=setting.SUM_WIDGET1[i][j],width=8,style="sum.TButton",
                                  padding=[0,7],
                                  command=lambda x=setting.SUM_WIDGET1[i][j]: self.entry_add(x))
                temp.grid_configure(row=i + 1, column=j)
                if setting.SUM_WIDGET1[i][j]=="=":
                    temp.config(command=lambda :self.entry_sum(2))
        self.frame1.place_configure(x=10,y=100)
    # 清空表达式
    def entry_clear(self):
        self.entry1.delete(0,"end")
        self.entry2.delete(0,"end")
        self.entry2.focus_set()

    # 删除表达式尾项
    def entry_pop(self):
        text=self.entry2.get()
        if text=="表达式错误!":
            self.entry2.delete(0,"end")
        else:
            temp_len=len(text)
            self.entry2.delete(temp_len-1,temp_len)
        self.entry_sum(1)
        self.entry2.focus_set()

    # 插入指定字符
    def entry_add(self,x:str):
        text=self.entry2.get()
        if text=="表达式错误!":
            self.entry2.delete(0,"end")
        self.entry2.insert("insert",x)
        self.entry_sum(1)
        self.entry2.focus_set()

    # 计算表达式
    def entry_sum(self,row):
        if row==1:
            text = self.entry2.get()
            text = text.replace('÷', '/')
            text = text.replace('x', '*')
            if text=="":
                self.entry1.delete(0, "end")
                return None
            try:
                temp=eval(text)  # 将文本输入框的字符串解析成表达式
                temp_int = int(temp)
                if temp == temp_int:  # 判断是否是整数
                    temp = temp_int
                else:
                    temp = float(temp)  # 将小数的0尾数去除
            except Exception:
                temp="表达式错误!"
            self.entry1.delete(0,"end")
            self.entry1.insert(0,temp)
        else:
            text=self.entry2.get()
            text=text.replace('÷', '/')
            text=text.replace('x', '*')
            if text=="表达式错误!":
                self.entry2.delete(0,"end")
            elif text=="":
                return None
            else:
                try:
                    temp=eval(text)  # 将文本输入框的字符串解析成表达式
                    temp_int=int(temp)
                    if temp==temp_int:   # 判断是否是整数
                        temp=temp_int
                    else:
                        temp=float(temp)  # 将小数的0尾数去除
                except Exception:
                    temp="表达式错误!"
                self.entry1.delete(0, "end")
                self.entry2.delete(0,"end")
                self.entry2.insert(0,temp)
        self.entry2.focus_set()

    # 销毁计算器组件
    def widget_replace(self):
        self.entry1.destroy()
        self.entry2.destroy()
        self.frame1.destroy()
# 科学计算器类
class Sum_Widget2(Sum_Widhet_Base):
    # 初始化科学计算器对象
    def __init__(self,root:tk.Tk):
        super().__init__(root)
        self.tk.title(setting.TITLE2)
        self.tk.geometry("570x450")  # 设置窗口大小和窗口位置
        self.widget_show()

    # 显示计算器组件
    def widget_show(self):
        # 创建输入框
        self.entry1 = tk.Entry(self.tk, font=setting.SUM_WIDGET2_ENTRY_FONT,
                               justify="right",width=25,relief=tk.FLAT)
        self.entry1.place_configure(x=85, y=18)
        self.entry2 = tk.Entry(self.tk, font=setting.SUM_WIDGET2_ENTRY_FONT,
                               justify="right",width=25,relief=tk.FLAT,insertbackground="#0033cc")
        self.entry2.place_configure(x=85, y=50)
        # 在2号输入框设置初始焦点
        self.entry2.focus_set()

        # 放置计算按钮
        self.frame1 = tk.Frame(self.tk)
        self.style.configure("left_right.TButton",font=setting.SUM_WIDGET2_BUTTON_FONT)
        self.button1_1 = ttk.Button(self.frame1, text="(", width=7,style="left_right.TButton",
                                   command=lambda: self.entry_add("("),padding=[0,10])
        self.button1_1.grid_configure(row=0, column=0)
        self.button1_1 = ttk.Button(self.frame1, text=")", width=7,style="left_right.TButton",
                                   command=lambda: self.entry_add(")"),padding=[0,10])
        self.button1_1.grid_configure(row=0, column=1)
        self.style.configure("clear_pop.TButton", font=setting.SUM_WIDGET2_BUTTON_FONT)
        self.button1_1 = ttk.Button(self.frame1, text="清空", width=7,style="clear_pop.TButton",
                                   command=self.entry_clear,padding=[0,10])
        self.button1_1.grid_configure(row=0, column=2, columnspan=2, sticky="ew")
        self.button1_1 = ttk.Button(self.frame1, text="删除", width=7,style="clear_pop.TButton",
                                   command=self.entry_pop,padding=[0,10])
        self.button1_1.grid_configure(row=0, column=4, columnspan=2, sticky="ew")
        self.style.configure("sum.TButton",font=setting.SUM_WIDGET2_BUTTON_FONT)
        for i in range(len(setting.SUM_WIDGET2)):
            for j in range(len(setting.SUM_WIDGET2[0])):
                if setting.SUM_WIDGET2[i][j]!="=":
                    temp = ttk.Button(self.frame1, text=setting.SUM_WIDGET2[i][j],
                                     width=7, style="sum.TButton",padding=[0,10],
                                     command=lambda x=i, y=j: self.entry_add(setting.SUM_WIDGET2[x][y]))
                    temp.grid_configure(row=i + 1, column=j)
                else:
                    temp = ttk.Button(self.frame1, text=setting.SUM_WIDGET2[i][j],
                                     width=7, style="sum.TButton",padding=[0,10],
                                      command=lambda: self.entry_sum(2))
                    temp.grid_configure(row=i + 1, column=j, columnspan=3, sticky="ew")
                    break
        self.frame1.place_configure(x=10, y=100)

    # 清空表达式
    def entry_clear(self):
        self.entry1.delete(0,"end")
        self.entry2.delete(0,"end")
        self.entry2.focus_set()

    # 删除表达式尾项
    def entry_pop(self):
        text=self.entry2.get()
        if text=="表达式错误!":
            self.entry2.delete(0,"end")
        else:
            temp_len=len(text)
            self.entry2.delete(temp_len-1,temp_len)
        self.entry_sum(1)
        self.entry2.focus_set()

    # 插入指定字符

    def entry_add(self,x:str):
        text=self.entry2.get()
        if text=="表达式错误!":
            self.entry2.delete(0,"end")
        operator_replace_dict={"x!":"!","√x":"√","x²":"^(2)","x^y":"^(",
                               "sin":"sin(","cos":"cos(","tan":"tan(",
                               "ln":"ln(","lg":"lg("}
        self.entry2.insert("insert",operator_replace_dict.get(x,x))  # 将符合字段要求的字符串替换成指定字符串，
                                                                            # 不符合要求则直接传入
        self.entry_sum(1)
        self.entry2.focus_set()

    # 计算表达式
    def entry_sum(self,row):
        if row==1:
            text = self.entry2.get()
            if text == "":
                self.entry1.delete(0,"end")
                return None
            else:
                temp_tuple1 = ("x", "÷", "e", "π")
                temp_tuple2 = ("*", "/", f"{math.e}", f"{math.pi}")  # 将数学特殊符号替换成对应数值
                for i in range(len(temp_tuple1)):
                    text = text.replace(temp_tuple1[i], temp_tuple2[i])
                try:
                    temp_tuple1 = setting.SUM_WIDGET2_OPERATOR_RE
                    temp_tuple2 = setting.SUM_WIDGET2_OPERATOR_LEFT
                    temp_tuple3 = setting.SUM_WIDGET2_OPERATOR_RIGHT
                    temp_func_tuple = setting.SUM_WIDGET2_FUNC
                    for i in range(len(temp_tuple1)):
                        temp = re.compile(temp_tuple1[i])  # 构建正则表达式的模式对象
                        temp_list = temp.findall(text)  # 匹配符合要求的数据以列表形式返回
                        for j in temp_list:
                            if i != 3:
                                if i == 0:
                                    # x的阶乘函数的处理
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](int(j))}")
                                elif i == 2:
                                    # x的平方函数的处理
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j), 2)}")
                                elif i == 7:
                                    # log函数的处理
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j), math.e)}")
                                else:
                                    # 三角函数的处理
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j))}")
                            else:
                                # x的y次方的函数处理
                                text = text.replace(f"{j[0]}^({j[1]})", f"{math.pow(float(j[0]), float(j[1]))}")
                    temp = eval(text)  # 将字符串解析成表达式
                except Exception:
                    temp = "表达式错误!"
                self.entry1.delete(0, "end")
                self.entry1.insert(0, temp)
        else:
            text=self.entry2.get()
            if text=="表达式错误!":
                self.entry1.delete(0,"end")
                self.entry2.delete(0,"end")
            elif text=="":
                return None
            else:
                temp_tuple1=("x","÷","e","π")
                temp_tuple2=("*","/",f"{math.e}",f"{math.pi}")  # 将数学特殊符号替换成对应数值
                for i in range(len(temp_tuple1)):
                    text=text.replace(temp_tuple1[i],temp_tuple2[i])
                try:
                    temp_tuple1 = setting.SUM_WIDGET2_OPERATOR_RE
                    temp_tuple2 = setting.SUM_WIDGET2_OPERATOR_LEFT
                    temp_tuple3 = setting.SUM_WIDGET2_OPERATOR_RIGHT
                    temp_func_tuple=(math.factorial,math.sqrt,math.pow,None,math.sin,math.cos,math.tan,math.log,math.log10)
                    for i in range(len(temp_tuple1)):
                        temp=re.compile(temp_tuple1[i])  # 构建正则表达式的模式对象
                        temp_list=temp.findall(text)  # 匹配符合要求的数据以列表形式返回
                        for j in temp_list:
                            if i!=3:
                                if i==0:
                                    # x的阶乘函数的处理
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](int(j))}")
                                elif i==2:
                                    # x的平方函数的处理
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j), 2)}")
                                elif i==7:
                                    # log函数的处理
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j),math.e)}")
                                else:
                                    # 三角函数的处理
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j))}")
                            else:
                                # x的y次方的函数处理
                                text = text.replace(f"{j[0]}^({j[1]})",f"{math.pow(float(j[0]),float(j[1]))}")
                    temp=eval(text)  # 将字符串解析成表达式
                except Exception:
                    temp="表达式错误!"
                self.entry1.delete(0,"end")
                self.entry2.delete(0,"end")
                self.entry2.insert(0,temp)
        self.entry2.focus_set()

    # 销毁计算器组件
    def widget_replace(self):   # 销毁计算器组件
        self.entry1.destroy()
        self.entry2.destroy()
        self.frame1.destroy()