class Map:  # 地图类
    def __init__(self,filename:str):
        self.data_list=[]  # 存放地图文件中加载的数据
        with open(filename,mode="r+",encoding="UTF-8")as f:
            for i in f:
                self.data_list.append(i.strip('\n'))  # 将每行末尾的换行符去除
        self.width=len(self.data_list[0])  # 获取地图长度
        self.height=len(self.data_list)  # 获取地图宽度