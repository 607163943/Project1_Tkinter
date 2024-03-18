import tkinter as tk
import setting
import math
import re
class Sum_Widhet_Base:
    def __init__(self,root:tk.Tk):
        self.tk=root
        self.tk.title(setting.TITLE1)
    def widget_show(self):
        pass
    def entry_clear(self):
        pass
    def entry_pop(self):
        pass
    def entry_add(self,x:str):
        pass
    def entry_sum(self,row):
        pass
    def widget_replace(self):
        pass
class Sum_Widget1(Sum_Widhet_Base):
    def __init__(self,root:tk.Tk):
        super().__init__(root)
        self.widget_show()
        self.tk.geometry("450x340+500+200")
    def widget_show(self):
        self.entry1=tk.Entry(self.tk,font=setting.SUM_WIDGET1_ENTRY_FONT,justify="right")
        self.entry1.place_configure(x=60,y=18)
        self.entry2 = tk.Entry(self.tk, font=setting.SUM_WIDGET1_ENTRY_FONT, justify="right")
        self.entry2.place_configure(x=60, y=50)
        self.frame1=tk.Frame(self.tk)
        temp=tk.Button(self.frame1,text="清空",font=setting.SUM_WIDGET1_BUTTON_FONT,command=self.entry_clear)
        temp.grid(row=0,column=0,columnspan=2,sticky="ew")
        temp = tk.Button(self.frame1, text="删除",font=setting.SUM_WIDGET1_BUTTON_FONT,command=self.entry_pop)
        temp.grid(row=0, column=2, columnspan=2,sticky="ew")
        for i in range(len(setting.SUM_WIDGET1)):
            for j in range(len(setting.SUM_WIDGET1[0])):
                temp=tk.Button(self.frame1,text=setting.SUM_WIDGET1[i][j],
                               width=8,font=setting.SUM_WIDGET1_BUTTON_FONT,
                               command=lambda x=setting.SUM_WIDGET1[i][j]:self.entry_add(x))
                temp.grid(row=i+1,column=j)
                if setting.SUM_WIDGET1[i][j]=="=":
                    temp.config(command=lambda :self.entry_sum(2))
        self.frame1.place_configure(x=10,y=100)
    def entry_clear(self):
        self.entry1.delete(0,"end")
        self.entry2.delete(0,"end")
    def entry_pop(self):
        text=self.entry2.get()
        if text=="表达式错误!":
            self.entry2.delete(0,"end")
        else:
            temp_len=len(text)
            self.entry2.delete(temp_len-1,temp_len)
        self.entry_sum(1)
    def entry_add(self,x:str):
        text=self.entry2.get()
        if text=="表达式错误!":
            self.entry2.delete(0,"end")
        self.entry2.insert("insert",x)
        self.entry_sum(1)
    def entry_sum(self,row):
        if row==1:
            text = self.entry2.get()
            text = text.replace('÷', '/')
            text = text.replace('x', '*')
            if text=="":
                self.entry1.delete(0, "end")
                return None
            try:
                temp=eval(text)
                temp_int = int(temp)
                if temp == temp_int:
                    temp = temp_int
                else:
                    temp = float(temp)
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
                    temp=eval(text)
                    temp_int=int(temp)
                    if temp==temp_int:
                        temp=temp_int
                    else:
                        temp=float(temp)
                except Exception:
                    temp="表达式错误!"
                self.entry1.delete(0, "end")
                self.entry2.delete(0,"end")
                self.entry2.insert(0,temp)
    def widget_replace(self):
        self.entry1.destroy()
        self.entry2.destroy()
        self.frame1.destroy()
    def __del__(self):
        print("计算器已删除")
class Sum_Widget2(Sum_Widhet_Base):
    def __init__(self,root:tk.Tk):
        super().__init__(root)
        self.tk.title(setting.TITLE2)
        self.tk.geometry("510x520+500+200")
        self.widget_show()
    def widget_show(self):
        self.entry1 = tk.Entry(self.tk, font=setting.SUM_WIDGET2_ENTRY_FONT, justify="right",width=25)
        self.entry1.place_configure(x=60, y=18)
        self.entry2 = tk.Entry(self.tk, font=setting.SUM_WIDGET2_ENTRY_FONT, justify="right",width=25)
        self.entry2.place_configure(x=60, y=50)
        self.frame1 = tk.Frame(self.tk)
        self.button1_1=tk.Button(self.frame1,text="(",font=setting.SUM_WIDGET2_BUTTON_FONT,width=6,height=1,
                                 command=lambda :self.entry_add("("))
        self.button1_1.grid_configure(row=0,column=0)
        self.button1_1 = tk.Button(self.frame1, text=")", font=setting.SUM_WIDGET2_BUTTON_FONT, width=6, height=1,
                                   command=lambda :self.entry_add(")"))
        self.button1_1.grid_configure(row=0, column=1)
        self.button1_1 = tk.Button(self.frame1, text="清空",font=setting.SUM_WIDGET2_BUTTON_FONT,width=6,height=1,
                                   command=self.entry_clear)
        self.button1_1.grid_configure(row=0, column=2, columnspan=2,sticky="ew")
        self.button1_1 = tk.Button(self.frame1, text="删除",font=setting.SUM_WIDGET2_BUTTON_FONT,width=6,height=1,
                                   command=self.entry_pop)
        self.button1_1.grid_configure(row=0, column=4, columnspan=2,sticky="ew")
        for i in range(len(setting.SUM_WIDGET2)):
            for j in range(len(setting.SUM_WIDGET2[0])):
                if setting.SUM_WIDGET2[i][j]!="=":
                    temp=tk.Button(self.frame1,text=setting.SUM_WIDGET2[i][j],font=setting.SUM_WIDGET2_BUTTON_FONT,
                                   width=6,height=2,command=lambda x=i,y=j:self.entry_add(setting.SUM_WIDGET2[x][y]))
                    temp.grid_configure(row=i+1,column=j)
                else:
                    temp=tk.Button(self.frame1,text=setting.SUM_WIDGET2[i][j],font=setting.SUM_WIDGET2_BUTTON_FONT,
                                   width=6,height=2,command=lambda :self.entry_sum(2))
                    temp.grid_configure(row=i+1,column=j,columnspan=3,sticky="ew")
                    break
        self.frame1.place_configure(x=10, y=100)
    def entry_clear(self):
        self.entry1.delete(0,"end")
        self.entry2.delete(0,"end")
    def entry_pop(self):
        text=self.entry2.get()
        if text=="表达式错误!":
            self.entry2.delete(0,"end")
        else:
            temp_len=len(text)
            self.entry2.delete(temp_len-1,temp_len)
        self.entry_sum(1)

    def entry_add(self,x:str):
        text=self.entry2.get()
        if text=="表达式错误!":
            self.entry2.delete(0,"end")
        operator_replace_dict={"x!":"!","√x":"√","x²":"^(2)","x^y":"^(",
                               "sin":"sin(","cos":"cos(","tan":"tan(",
                               "ln":"ln(","lg":"lg("}
        self.entry2.insert("insert",operator_replace_dict.get(x,x))
        self.entry_sum(1)
    def entry_sum(self,row):
        if row==1:
            text = self.entry2.get()
            if text == "":
                self.entry1.delete(0,"end")
                return None
            else:
                temp_tuple1 = ("x", "÷", "e", "π")
                temp_tuple2 = ("*", "/", f"{math.e}", f"{math.pi}")
                for i in range(len(temp_tuple1)):
                    text = text.replace(temp_tuple1[i], temp_tuple2[i])
                try:
                    temp_tuple1 = setting.SUM_WIDGET2_OPERATOR_RE
                    temp_tuple2 = setting.SUM_WIDGET2_OPERATOR_LEFT
                    temp_tuple3 = setting.SUM_WIDGET2_OPERATOR_RIGHT
                    temp_func_tuple = setting.SUM_WIDGET2_FUNC
                    for i in range(len(temp_tuple1)):
                        temp = re.compile(temp_tuple1[i])
                        temp_list = temp.findall(text)
                        for j in temp_list:
                            if i != 3:
                                if i == 0:
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](int(j))}")
                                elif i == 2:
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j), 2)}")
                                elif i == 7:
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j), math.e)}")
                                else:
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j))}")
                            else:
                                text = text.replace(f"{j[0]}^({j[1]})", f"{math.pow(float(j[0]), float(j[1]))}")
                    temp = eval(text)
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
                temp_tuple2=("*","/",f"{math.e}",f"{math.pi}")
                for i in range(len(temp_tuple1)):
                    text=text.replace(temp_tuple1[i],temp_tuple2[i])
                try:
                    temp_tuple1=("(\d*?)!","√([0-9.]*)","([0-9.]*)\^\(2\)","([0-9.]*)\^\(([0-9.]*)\)",
                                 "sin\(([0-9.]*)\)","cos\(([0-9.]*)\)","tan\(([0-9.]*)\)","ln\(([0-9.]*)\)",
                                 "lg\(([0-9.]*)\)")
                    temp_tuple2=("","√","",None,"sin(","cos(","tan(","ln(","lg(")
                    temp_tuple3=("!","","^(2)",None,")",")",")",")",")")
                    temp_func_tuple=(math.factorial,math.sqrt,math.pow,None,math.sin,math.cos,math.tan,math.log,math.log10)
                    for i in range(len(temp_tuple1)):
                        temp=re.compile(temp_tuple1[i])
                        temp_list=temp.findall(text)
                        for j in temp_list:
                            if i!=3:
                                if i==0:
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](int(j))}")
                                elif i==2:
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j), 2)}")
                                elif i==7:
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j),math.e)}")
                                else:
                                    text = text.replace(temp_tuple2[i] + f"{j}" + temp_tuple3[i],
                                                        f"{temp_func_tuple[i](float(j))}")
                            else:
                                text = text.replace(f"{j[0]}^({j[1]})",f"{math.pow(float(j[0]),float(j[1]))}")
                    temp=eval(text)
                except Exception:
                    temp="表达式错误!"
                self.entry1.delete(0,"end")
                self.entry2.delete(0,"end")
                self.entry2.insert(0,temp)
    def widget_replace(self):
        self.entry1.destroy()
        self.entry2.destroy()
        self.frame1.destroy()
    def __del__(self):
        print("科学计算器已删除")