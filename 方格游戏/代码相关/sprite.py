import random
class Player:
    def __init__(self,game,x,y):
        self.game=game  # 存放游戏界面对象
        self.x=x  # 存放玩家在地图上的初始x坐标
        self.y=y  # 存放玩家在地图上的初始y坐标
        self.is_channel=False  # 记录玩家是否经过传送门
        self.move_set()  # 绑定玩家按键事件
    def move_set(self):  # 绑定玩家按键事件
        temp_tuple=("a","s","d","w")  # 将对应a,s,d,w键的按键事件绑定
        for i in temp_tuple:
            self.game.tk.bind(f"<Key-{i}>",lambda event,x=i:self.move(x))
    def move_unset(self):  # 解除按钮绑定事件
        temp_tuple = ("a", "s", "d", "w")
        for i in temp_tuple:
            self.game.tk.unbind(f"<Key-{i}>")
    def move(self,mode:str):  # 玩家移动函数
        temp_list=[self.x,self.y]  # 记录玩家当前位置
        # 根据玩家的按键来进行预移动
        if mode=="a":
            temp_list[1]-=1
        elif mode=="d":
            temp_list[1]+=1
        elif mode=="s":
            temp_list[0]+=1
        else:
            temp_list[0]-=1
        # 判断将要移动的位置是否遇到墙和是否遇到出口
        if not self.wall_hit(*temp_list) and not self.exit_hit(*temp_list):
            # 判断将要移动的位置是否遇到陷阱和是否遇到敌人
            if not self.trap_hit(*temp_list) and not self.mob_hit(*temp_list):
                # 判断玩家是否刚经历传送门
                if self.is_channel:
                    # 将传送玩家的传送门图像恢复
                    self.game.label_list[self.x][self.y].config(image=self.game.image_dict.get("channel"))
                    self.is_channel=False  # 重置是否经过传送门的标志
                else:  # 将上一次玩家所在地块的图像恢复
                    self.game.label_list[self.x][self.y].config(image=self.game.image_dict.get("normal"))
                temp_list=self.channel_hit(*temp_list) # 判断玩家是否到达传送门
                self.x,self.y=temp_list  # 更新玩家的位置坐标
                # 更新玩家所在位置的图像
                self.game.label_list[self.x][self.y].config(image=self.game.image_dict.get("player"))
    def wall_hit(self,x,y):  # 判断是否撞墙的函数
        for i in self.game.walls:  # 遍历所有在地图上的墙,判断是否有坐标的重合
            if x==i.x and y==i.y:
                return True
        return False
    def exit_hit(self,x,y):  # 判断是否遇到出口的函数
        # 判断是否有坐标的重合
        if x==self.game.all_sprite.get("exit").x and y==self.game.all_sprite.get("exit").y:
            self.move_unset()  # 解除玩家的按键事件
            self.game.show_over_game(False)  # 进入通关情况下的游戏结束界面
            return True
        return False
    def trap_hit(self,x,y):  # 判断是否遇到陷阱的函数
        for i in self.game.traps:  # 遍历所有在地图上的陷阱,判断是否有坐标的重合
            if x==i.x and y==i.y:
                self.move_unset()  # 解除玩家的按键事件
                self.game.show_over_game(True)  # 进入游戏失败情况下的游戏结束界面
                return True
        return False
    def mob_hit(self,x,y):  # 判断是否遇到敌人的函数
        for i in self.game.mobs:  # 遍历地图上的敌人,判断坐标是否重合
            if x==i.x and y==i.y:
                self.move_unset()  # 解除玩家的按键事件
                self.game.show_over_game(True)  # 进入游戏失败情况下的游戏结束界面
                return True
        return False
    def channel_hit(self,x,y)->list:  # 判断是否遇到传送门的函数
        is_hit=False
        for i in self.game.channels:  # 遍历地图上的传送门,判断是否有坐标的重合
            if x==i.x and y==i.y:
                is_hit=True
        while is_hit:  # 遇到传送门将随机传送到该传送门之外的任意一个传送门处
            temp=random.choice(self.game.channels)
            if x!=temp.x and y!=temp.y:
                x,y=temp.x,temp.y
                self.is_channel=True
                break
        return [x,y]  # 返回传送后的新坐标
class Wall:  # 墙类
    def __init__(self,game,x,y):
        self.game=game  # 存放游戏类的对象
        self.x=x  # 存放墙在地图上的初始x坐标
        self.y=y # 存放墙在地图上的初始y坐标
class Exit:  # 出口类
    def __init__(self,game,x,y):
        self.game=game  # 存放游戏类的对象
        self.x=x  # 存放在地图上的初始x坐标
        self.y=y  # 存放在地图上的初始y坐标
class Trap:  # 陷阱类
    def __init__(self,game,x,y):
        self.game=game  # 存放游戏类的对象
        self.x=x  # 存放陷阱在地图上的初始x坐标
        self.y=y  # 存放陷阱在地图上的初始y坐标
class Mob:  # 敌人类
    def __init__(self,game,x,y):
        self.game=game  # 存放游戏类的对象
        self.x=x  # 存放地图上的敌人初始x坐标
        self.y=y  # 存放地图上的敌人初始y坐标
    def move(self):  # 敌人的移动函数
        temp_list=[self.x,self.y]  # 存放敌人的初始位置坐标
        x,y=random.randint(-1,1),random.randint(-1,1)  # 进行预随机移动
        if x!=0:  # 敌人不能进行x,y坐标同时加1或者同时减1的移动(斜方向移动)
            y=0
        # 记录预随即移动后的预移动位置
        temp_list[0]+=x
        temp_list[1]+=y
        # 判断是否撞墙和是否遇到陷阱
        if not self.wall_hit(*temp_list) and not self.trap_hit(*temp_list):
            # 判断是否遇到其他敌人
            if not self.mob_hit(*temp_list):
                # 将上一次敌人所在地块的图像恢复
                self.game.label_list[self.x][self.y].config(image=self.game.image_dict.get("normal"))
                # 更新敌人位置坐标
                self.x, self.y = temp_list
                # 更新敌人的图像位置
                self.game.label_list[self.x][self.y].config(image=self.game.image_dict.get("mob"))
    def wall_hit(self,x,y):  # 判断是否撞墙的函数
        for i in self.game.walls:  # 遍历地图上所有的墙,判断坐标是否重合
            if x==i.x and y==i.y:
                return True
        return False
    def trap_hit(self,x,y):  # 判断是否遇到陷阱的函数
        for i in self.game.traps:  # 遍历地图上所有的陷阱,判断坐标是否重合
            if x==i.x and y==i.y:
                return True
        return False
    def mob_hit(self,x,y):  # 判断是否遇到其他敌人的函数
        for i in self.game.traps:  # 遍历地图上所有的敌人,判断坐标是否与其他敌人重合(通过比较对象数据可以判断是否是对象本身)
            if i!=self and x==i.x and y==i.y:
                return True
        return False
class Channel:  # 传送门类
    def __init__(self,game,x,y):
        self.game=game  # 存放游戏类对象
        self.x=x  # 存放传送门在地图上的初始x坐标
        self.y=y  # 存放传送门在地图上的初始y坐标