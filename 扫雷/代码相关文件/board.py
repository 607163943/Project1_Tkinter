import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from os import path
import random
import setting
import csv
class Board:
    def __init__(self,root:tk.Tk):
        self.tk=root
        self.image_dict={"face":[],"mine":[],"safe":[]}
        self.board_dict={"row":9,"col":9,"boom":10,"flag":10,"time":0}
        self.using="简单"
        self.board1=[]
        self.board2=[]
        self.board3=[]
        self.time=0
        self.flag=self.board_dict.get("flag")
        self.button_list=[]
        self.time_continue=True
        self.flag_list=[]
        self.flag_text=f"红旗数:{self.flag}"
        self.time_text=f"用时:{self.time}"
        self.is_menu_set_window_show=True
        self.score_dict={'easy':0,'normal':0,'trouble':0}
        self.file_start()
        self.load_image()
    def __del__(self):
        self.file.seek(0)
        self.csv_file.writerow(self.score_dict.values())
        self.file.close()
    def load_image(self):
        dir_image_base=""
        dir_image=path.join(dir_image_base,"image")
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
    def file_start(self):
        dir_path_base=""
        dir_data_path=path.join(dir_path_base,"data")
        csv_file=open(path.join(dir_data_path,"score.csv"),mode="r+",encoding="UTF-8",newline="")
        self.file=csv_file
        for i in self.file:
            temp_list=i.split(',')
            self.score_dict["easy"]=int(temp_list[0])
            self.score_dict["normal"]=int(temp_list[1])
            self.score_dict["trouble"]=int(temp_list[2])
            break
        self.csv_file=csv.writer(csv_file)
    def show_start_window(self):
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
    def start(self):
        if self.is_menu_set_window_show:
            self.frame1.destroy()
            self.is_menu_set_window_show=False
        self.board1=[[0 for j in range(self.board_dict.get("col")+2)] for i in range(self.board_dict.get("row")+2)]
        self.board2=[[0 for j in range(self.board_dict.get("col")+2)] for i in range(self.board_dict.get("row")+2)]
        self.board3=[["*" for j in range(self.board_dict.get("col")+2)] for i in range(self.board_dict.get("row")+2)]
        temp=self.board_dict.get("boom")
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
        self.time = 0
        self.flag = self.board_dict.get("flag")
        self.button_list = []
        self.time_continue = True
        self.flag_list = []
        self.widget_show()

    def widget_show(self):
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
        for i in range(self.board_dict.get("row")):
            temp_list=[]
            for j in range(self.board_dict.get("col")):
                temp=tk.Button(self.frame2_2, image=self.image_dict["normal"], command=lambda x=i, y=j :self.button_show(x, y))
                temp.grid(row=i,column=j)
                temp.bind("<Button-3>",lambda event,x=i,y=j:self.flag_show_or_cancel(x,y))
                temp_list.append(temp)
            self.button_list.append(temp_list)
        self.frame2_2.pack()
        self.frame2.pack()
        self.tk.after(1000,self.time_counter)
    def once_again(self):
        self.frame2.destroy()
        self.start()
    def time_counter(self):
        if self.time_continue:
            self.time+=1
            self.time_text=f"用时:{self.time}"
            self.label2_1_2.config(text=f"用时:{self.time}")
            self.tk.after(1000,self.time_counter)
    def button_show(self,x,y):
        if self.board1[x+1][y+1]==1:
            self.game_over(x,y)
        else:
            self.blank_show2(x,y)
            if self.is_win():
                self.game_win()
    def flag_show_or_cancel(self,x,y):
        if (x,y) not in self.flag_list:
            if self.flag>0:
                self.flag-=1
                self.flag_list.append((x,y))
                self.button_list[x][y].config(image=self.image_dict["flag"])
        else:
            self.flag+=1
            self.flag_list.pop(self.flag_list.index((x,y)))
            self.button_list[x][y].config(image=self.image_dict["normal"])
        self.label2_1_1.config(text=f"红旗数:{self.flag}")
    def game_over(self,x,y):
        self.time_continue=False
        for i in range(self.board_dict.get("row")):
            for j in range(self.board_dict.get("col")):
                self.button_list[i][j].config(command=lambda :None)
                self.button_list[i][j].unbind("<Button-3>")
                if self.board1[i+1][j+1]==1:
                    self.button_list[i][j].config(image=self.image_dict.get("mine")[0])
        self.button2_1_1.config(image=self.image_dict.get("face")[1])
        self.button_list[x][y].config(image=self.image_dict.get("mine")[1])
    def is_win(self):
        for i in range(self.board_dict.get("row")):
            for j in range(self.board_dict.get("col")):
                if self.board1[i+1][j+1]==0 and self.board3[i+1][j+1]=="*":
                    return False
        return True
    def game_win(self):
        self.time_continue=False
        for i in range(self.board_dict.get("row")):
            for j in range(self.board_dict.get("col")):
                self.button_list[i][j].config(command=lambda :None)
                self.button_list[i][j].unbind("<Button-3>")
                if self.board1[i+1][j+1]==1:
                    self.button_list[i][j].config(image=self.image_dict.get("mine")[0])
        self.button2_1_1.config(image=self.image_dict.get("face")[2])
        if self.using=="简单":
            if self.score_dict["easy"]==0:
                self.score_dict["easy"]=self.time
            else:
                if self.time<self.score_dict.get("easy"):
                    self.score_dict["easy"]=self.time
        elif self.using=="普通":
            if self.score_dict["normal"]==0:
                self.score_dict["normal"]=self.time
            else:
                self.score_dict["normal"]=self.time
        elif self.using=="困难":
            if self.score_dict["trouble"]==0:
                self.score_dict["trouble"]=self.time
            else:
                self.score_dict["trouble"]=self.time


    def blank_show2(self,x,y):
        if x<0 or y<0:
            return None
        elif x>=self.board_dict.get("row") or y>=self.board_dict.get("col"):
            return None
        elif self.board3[x+1][y+1]==' ':
            return None
        else:
            if self.board1[x+1][y+1]==0:
                self.board3[x+1][y+1]=' '
                self.button_list[x][y].grid_forget()
                temp=tk.Label(self.frame2_2, image=self.image_dict.get("safe")[self.board2[x + 1][y + 1]])
                temp.grid(row=x,column=y)
                if (x, y) in self.flag_list:
                    self.flag += 1
                    self.flag_list.pop(self.flag_list.index((x, y)))
                    self.label2_1_1.config(text=f"红旗数:{self.flag}")
                if self.board2[x+1][y+1]==0:
                    self.blank_show2(x+1,y)
                    self.blank_show2(x,y+1)
                    self.blank_show2(x+1,y+1)
                    self.blank_show2(x-1,y)
                    self.blank_show2(x,y-1)
                    self.blank_show2(x-1,y-1)
                    self.blank_show2(x+1,y-1)
                    self.blank_show2(x-1,y+1)
    def board_set(self):
        self.time_continue=False
        if not self.is_menu_set_window_show:
            self.frame2.destroy()
        else:
            self.frame1.destroy()
        self.style = ttk.Style(self.tk)
        self.frame3=tk.Frame(self.tk)
        self.frame3_1=tk.Frame(self.frame3)
        self.label3_1_1=tk.Label(self.frame3_1, text="难度", font=setting.BOARD_FONT)
        self.label3_1_1.grid(row=0, column=0)
        self.board_var=tk.Variable(value=self.using)
        self.label3_1_2=tk.Label(self.frame3_1, width=10)
        self.label3_1_2.grid(row=0, column=1)
        self.style.configure("TMenubutton",font=setting.BOARD_FONT)
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
        self.style.configure("TButton",font=setting.BOARD_FONT)
        self.button3_2_1=ttk.Button(self.frame3_2, text="完成", command=self.set_true)
        self.button3_2_1.grid(row=0, column=0)
        self.label3_2_1=tk.Label(self.frame3_2, width=10)
        self.label3_2_1.grid(row=0, column=1)
        self.button3_2_2=ttk.Button(self.frame3_2, text="取消", command=self.set_return)
        self.button3_2_2.grid(row=0, column=2)
        self.frame3_2.pack()
        self.frame3.pack()
        self.entry3_1.insert("end", str(self.board_dict.get("row")))
        self.entry3_2.insert("end", str(self.board_dict.get("col")))
        self.entry3_3.insert("end", str(self.board_dict.get("boom")))
        self.entry3_1.configure(state="disable")
        self.entry3_2.configure(state="disable")
        self.entry3_3.configure(state="disable")
    def board_replace(self,x):
        self.entry3_1.configure(state="normal")
        self.entry3_2.configure(state="normal")
        self.entry3_3.configure(state="normal")
        self.entry3_1.delete(0, "end")
        self.entry3_2.delete(0, "end")
        self.entry3_3.delete(0, "end")
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
            self.entry3_1.configure(state="disable")
            self.entry3_2.configure(state="disable")
            self.entry3_3.configure(state="disable")
    def set_true(self):
        try:
            row = int(self.entry3_1.get())
            col = int(self.entry3_2.get())
            booms = int(self.entry3_3.get())
            flags = int(self.entry3_3.get())
        except Exception:
            messagebox.showerror(title="错误",message="请输入合法的自定义数据!")
        else:
            self.using = self.board_var.get()
            self.board_dict["row"]=row
            self.board_dict["col"]=col
            self.board_dict["boom"]=booms
            self.board_dict["flag"]=flags
            self.frame3.destroy()
            if self.is_menu_set_window_show:
                self.show_start_window()
            else:
                self.start()
    def set_return(self):
        self.frame3.destroy()
        if self.is_menu_set_window_show:
            self.show_start_window()
        else:
            self.start()