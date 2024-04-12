import tkinter as tk
from os import path
import setting
import map
import sprite
import random
class Game:  # 游戏类
    def __init__(self,root:tk.Tk):
        self.tk=root   # 存放主窗口对象
        self.image_dict={}   # 存放加载的图片
        self.map_dict={}  # 存放各难度地图文件路径
        self.label_list=[]  # 存放地图地块组件
        self.all_sprite={"wall":[],"trap":[],"mob":[],"channel":[]}  # 存放地图中出现的所有精灵
        self.walls=[]  # 存放地图中的墙对象
        self.traps=[]  # 存放地图中的陷阱对象
        self.mobs=[]  # 存放地图中的敌人对象
        self.channels=[]  # 存放地图中的传送墙对象
        self.time_is_continue=True  # 计时标志
        self.time=0  # 用时
        self.load_image()  # 加载图片
        self.load_map()  # 加载各难度地图路径
        self.using="easy"   # 当前地图的难度
        self.mode_var_name="简单"  # 记录在变量中的使用地图难度
        self.root_status="start"  # 当前使用的界面(初始化后由窗口类调用开始界面函数)
    def load_image(self):  # 加载图片函数
        dir_image_base=""
        dir_image=path.join(dir_image_base,"image")  # 拼接出图片总文件夹
        temp_tuple=("normal","wall","player","exit","trap","mob","channel")
        for i in temp_tuple:
            self.image_dict[i]=tk.PhotoImage(file=path.join(dir_image,f"{i}.png"),format="png")
    def load_map(self):  # 加载各难度地图路径
        dir_map_base=""
        dir_map=path.join(dir_map_base,"map")  # 拼接出地图总文件夹路径
        dir_easy_map=path.join(dir_map,"easy_map")  # 拼接出简单难度的地图文件夹总路径
        dir_normal_map=path.join(dir_map,"normal_map")  # 拼接处普通难度的地图文件夹总路径
        dir_trouble_map=path.join(dir_map,"trouble_map")  # 拼接出困难难度的地图文件夹总路径
        temp_list=[]
        for i in range(1,5):
            temp_list.append(path.join(dir_easy_map,f"easy_map{i}.txt"))
        self.map_dict["easy"] = temp_list
        temp_list=[]
        for i in range(1,2):
            temp_list.append(path.join(dir_normal_map,f"normal_map{i}.txt"))
        self.map_dict["normal"]=temp_list
        temp_list=[]
        for i in range(1,2):
            temp_list.append(path.join(dir_trouble_map,f"trouble_map{i}.txt"))
        self.map_dict["trouble"] = temp_list
    def new(self):  # 初始化地图数据
        self.frame1.destroy()  # 销毁开始界面
        self.label_list = []  # 初始化地图地块组件
        self.all_sprite = {"wall": [], "trap": [], "mob": [], "channel": []}  # 初始化地图总精灵列表
        self.walls = []  # 初始化地图墙对象列表
        self.traps = []  # 初始化地图陷阱对象列表
        self.mobs = []  # 初始化地图敌人对象列表
        self.channels = []  # 初始化地图传送墙对象列表
        self.time_is_continue = True  # 开始计时标志
        self.time = 0  # 重置用时
        self.root_status="game"  # 更新所在界面信息(初始化会显示游戏界面)
        self.frame2=tk.Frame()
        self.map=map.Map(random.choice(self.map_dict.get(self.using)))  # 生成使用的地图对象
        for i in range(self.map.height):
            temp_list=[]
            for j in range(self.map.width):
                temp=tk.Label(self.frame2,image=self.image_dict.get("normal"))  # 生成地图地块组件
                temp.grid(row=i,column=j)
                # 从加载的地图数据中根据对应位置的标志生成对应对象
                if self.map.data_list[i][j]=="1":  # 生成墙对象
                    temp.config(image=self.image_dict.get("wall"))
                    wall=sprite.Wall(self,i,j)
                    self.all_sprite.get("wall").append(wall)
                    self.walls.append(wall)
                elif self.map.data_list[i][j]=="P":  # 生成玩家对象
                    temp.config(image=self.image_dict.get("player"))
                    self.player=sprite.Player(self,i,j)
                    self.all_sprite["player"]=self.player
                elif self.map.data_list[i][j]=="E":  # 生成出口对象
                    temp.config(image=self.image_dict.get("exit"))
                    exit=sprite.Exit(self,i,j)
                    self.all_sprite["exit"]=exit
                elif self.map.data_list[i][j]=="T":  # 生成陷阱对象
                    temp.config(image=self.image_dict.get("trap"))
                    trap=sprite.Trap(self,i,j)
                    self.all_sprite["trap"].append(trap)
                    self.traps.append(trap)
                elif self.map.data_list[i][j]=="M":   # 生成敌人对象
                    temp.config(image=self.image_dict.get("mob"))
                    mob=sprite.Mob(self,i,j)
                    self.all_sprite.get("mob").append(mob)
                    self.mobs.append(mob)
                elif self.map.data_list[i][j]=="C":  # 生成传送墙对象
                    temp.config(image=self.image_dict.get("channel"))
                    channel=sprite.Channel(self,i,j)
                    self.all_sprite.get("channel").append(channel)
                    self.channels.append(channel)
                temp_list.append(temp)
            self.label_list.append(temp_list)
        self.frame2.pack()
        self.tk.after(1000,self.time_counter)  # 开始计时
    def time_counter(self):  # 计时函数
        if self.time_is_continue:  # 判断是否继续计时
            self.time+=1
            for i in self.mobs:   # 将所有敌人依次执行移动函数
                i.move()
            self.tk.after(1000,self.time_counter)  # 继续计时
    def show_start_game(self):  # 显示开始界面函数
        self.frame1=tk.Frame(self.tk)
        self.label1_1=tk.Label(self.frame1,text="方格游戏",font=setting.GAME_FONT,width=20)
        self.label1_1.pack(pady=20)
        self.button1_1=tk.Button(self.frame1,text="开始游戏",font=setting.GAME_FONT,command=self.new)
        self.button1_1.pack(pady=20)
        self.root_status = "start"  # 更新当前所处界面信息
        self.frame1.pack()
    def show_over_game(self,is_over:bool):  # 显示游戏结束函数
        self.frame2.destroy()
        self.root_status="over"  # 更新当前所处界面信息
        self.time_is_continue=False  # 停止计时
        self.frame3=tk.Frame(self.tk)
        self.label3_1=tk.Label(self.frame3,text="恭喜通关!",font=setting.GAME_FONT,width=20)
        self.label3_1.pack(pady=20)
        self.button3_1=tk.Button(self.frame3,text="重新开始",command=self.once_again,font=setting.GAME_FONT)
        self.button3_1.pack(pady=20)
        if is_over:  # 判断是否为游戏失败
            self.label3_1.config(text="游戏结束!")
        self.frame3.pack()
    def once_again(self):  # 重新开始执行函数
        self.frame3.destroy()  # 销毁游戏结束界面
        self.new()  # 重新初始化地图数据