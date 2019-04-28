import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
import math
import time

start = time.clock()


def timetrans(s):             #将时间化为分钟
    a=s.split(':')
    a[0]=int(a[0])*60+int(a[1])-8*60
    a.pop()
    return(a[0])


def charimf():
    charger = []
    for line in open('charger.txt').readlines():  # 充电桩信息
        line = line.strip('\n')
        a = line.split(',')
        a[0] = int(a[0]) - 1000
        a[1] = float(a[2])
        a[2] = float(a[3])
        del a[3], a[4], a[5], a[4], a[3]

        charger.append(a)
    return charger


class graph():                #地图显示
    def __init__(self,depot):      #配置中心[116.571614 ,39.792844]
        self.depot=depot
        self.customernum = 1000
        self.customerloc = {}
        self.package = {}
        self.timewindows = {}
        self.charger = {}
        self.cusimf = []
        self.angle = []           #每个客户的角度
        self.dis = []           #相邻距离取最近的20个 包括
        self.orig = []            #每个到原点距离  从0开始
        self.chardis = []           #每个点到充电桩的距离取最近的10个 包括0点
        self.cuss=[]         #各个点之间的距离  为1100*1101个
        self.solution=[]              #解决
        self.left=[]                       #除了一组特殊外剩下的
        self.ts=[]             #时间特殊组

    def get_cusimf(self):
        cus = []
        # with open('dis.csv') as file:
        #    count=len(file.readlines())
        #    print(count)
        for line in open('customers.txt').readlines():  # 顾客信息
            line = line.strip('\n')
            a = line.split(',')
            a[0] = int(a[0])
            a[1] = (float(a[2])-self.depot[0])*111000
            a[2] = (float(a[3])-self.depot[1])*111000*math.cos(float(a[3])/180*math.pi)
            a[3] = float(a[4])
            a[4] = float(a[5])
            a[5] = timetrans(a[6])
            a[6] = timetrans(a[7])
            del a[7]
            cus.append(a)
        self.cusimf= cus  # cus将会是一个[[序号，经度，纬度， 重量，体积，时间窗]]的向量
    def get_loc(self):
        a=self.cusimf
        b={}
        for i in range(len(a)):
            e0=a[i][1]
            f0=a[i][2]
            g0=[e0,f0]
            b[i+1]=g0
        self.customerloc=b
        c=charimf()
        d={}
        for j in range(len(c)):
            e1=(c[j][1]-self.depot[0])*111000
            f1=(c[j][2]-self.depot[1])*111000*math.cos(c[j][2]/180*math.pi)
            g1=[e1,f1]
            d[j+1]=g1
        self.charger=d
    def get_item(self):
        a=self.cusimf
        b={}
        for i in range(len(a)):
            c = a[i][3]
            d = a[i][4]
            b[i + 1] = [c, d]
        self.package=b
    def get_time(self):
        a=self.cusimf
        b={}
        for i in range(len(a)):
            c = a[i][5]
            d = a[i][6]
            b[i + 1] = [c, d]
        self.timewindows=b
    def readinput(self):
        dis = []
        for line in open('input_distance-time.txt').readlines():
            line = line.strip('\n')
            a = line.split(',')
            a[0] = int(a[1])
            a[1] = int(a[2])
            a[2] = int(a[3])
            a[3] = int(a[4])
            del a[4]
            dis.append(a)
        gro = []  # 客户点到各地距离
        char = []
        start = []  # 原点距离
        mut = []
        for i in range(1101):
            b=[i,dis[i*1100:(i+1)*1100]]
            mut.append(b)
        for i in range(1100):               #前1000为原点距离
            start.append(dis[i])
        del dis[:1100]  # dis为客户

        for j in range(1000):
            gro.append([j + 1, dis[j * 1100:(j + 1) * 1100]])
        for i in range(len(gro)):
            char.append([i + 1, gro[i][1][1000:]])       #得出充电桩距离
        for i in range(len(char)):
            char[i][1] = sorted(char[i][1], key=lambda x: x[2])     #按距离排序
            del (char[i][1])[10:]               #得出前十

        for i in range(len(gro)):
            del (gro[i][1])[0]         #减去原点
            del (gro[i][1])[999:]      #减去充电桩
            gro[i][1] = sorted(gro[i][1], key=lambda x: x[2])
            del (gro[i][1])[20:]          #保留前20
        for i in range(len(mut)):
            c={}
            for j in range(len(mut[i][1])):
                c[mut[i][1][j][1]]=[mut[i][1][j][2],mut[i][1][j][3]]
            mut[i][1]=c
        self.cuss=mut                    #mut 为各个点之间的距离时间
        self.orig=start
        self.chardis=char
        self.dis=gro
    def get_graph(self):       #展示顾客，充电站，配送点地理信息
        xi=[]              #客户x轴集合
        yi=[]             #客户y轴集合
        for i in range(len(self.customerloc)):
            xi.append(self.customerloc[i+1][0])
            yi.append(self.customerloc[i+1][1])
        plt.scatter(xi,yi,color='r')

        xj=[]               #充电站x轴集合
        yj=[]                #充电站y轴集合
        for j in range(len(self.charger)):
            xj.append(self.charger[j+1][0])
            yj.append(self.charger[j+1][1])
        plt.scatter(xj,yj,color='b')
        plt.scatter(0,0,c='y',s=60)
        plt.show()
    def get_splitangle(self):       #按角度分离
        x=np.array([0,1])
        a=[]
        for i in range(len(self.charger)):
            y=np.array(self.charger[i+1])
            Ly=np.sqrt(y.dot(y))
            cosangle=x.dot(y)/Ly
            angle=np.arccos(cosangle)
            a.append(angle)                  #每个充电桩与y轴的夹角
        a.sort()                   #按从小到大
        c=2*np.pi-a[-1]+a[0]              #第一个与最后一个的夹角
        b=[]
        for j in range(len(a)-1):
            b.append(a[j+1]-a[j])             #相邻之间的夹角
        b.append(c)
        s=[]
        for k in range(len(a)-1): #求角平分线
            e=a[k]+b[k]/2                 #第k个角平分线与y轴的夹角
            f=[np.sin(e),np.cos(e)]          #角平分线的坐标
            s.append(f)
        a1=[np.sin(a[0]),np.cos(a[0])]   #最小角的单位坐标
        a0=[np.sin(a[-1]),np.cos(a[-1])]#最大角的单位坐标
        s0=[(a1[0]+a0[0])/2,(a1[1]+a0[1])/2]   #最大与最小的角平分线
        s.append(s0)             #所有角平分线
    def get_splitt(self):            #按时间分离
        self.a = []  # 9-10       1
        self.b = []  # 9.5-10.5    1
        self.c = []  # 9-11      2
        self.d = []  # 9.5-11    1.5
        self.e = []  # 10-11     1
        self.f = []  # 9-12      3
        self.g = []  # 9.5-12    2.5
        self.h = []  # 10-12     2
        self.i = []  # 11-12     1
        self.j = []  # 11-13     2
        self.k = []  # 11.5-13   1.5
        self.l = []  # 11-13.5   2.5
        self.m = []  # 11.5-13.5  2
        self.n = []  # 13-14      1
        self.o = []  # 13.5-14    0.5        ****
        self.p = []  # 13-14.5    1.5
        self.q = []  # 13.5-14.5   1
        self.r = []  # 13-15       2
        self.s = []  # 13.5-15     1.5
        self.t = []  # 13-15.5     2.5
        self.u = []  # 13.5-15.5    2
        x = self.cusimf
        for v in range(len(x)):
            if x[v][5] == 60 and x[v][6] == 120:
                self.a.append(x[v])
            elif x[v][5] == 90 and x[v][6] == 150:
                self.b.append(x[v])
            elif x[v][5] == 60 and x[v][6] == 180:
                self.c.append(x[v])
            elif x[v][5] == 90 and x[v][6] == 180:
                self.d.append(x[v])
            elif x[v][5] == 120 and x[v][6] == 180:
                self.e.append(x[v])
            elif x[v][5] == 60 and x[v][6] == 240:
                self.f.append(x[v])
            elif x[v][5] == 90 and x[v][6] == 240:
                self.g.append(x[v])
            elif x[v][5] == 120 and x[v][6]== 240:
                self.h.append(x[v])
            elif x[v][5] == 180 and x[v][6] == 240:
                self.i.append(x[v])
            elif x[v][5] == 180 and x[v][6] == 300:
                self.j.append(x[v])
            elif x[v][5] == 210 and x[v][6] == 300:
                self.k.append(x[v])
            elif x[v][5] == 180 and x[v][6] == 330:
                self.l.append(x[v])
            elif x[v][5] == 210 and x[v][6]== 330:
                self.m.append(x[v])
            elif x[v][5] == 300 and x[v][6] == 360:
                self.n.append(x[v])
            elif x[v][5] == 330 and x[v][6] == 360:
                self.o.append(x[v])
            elif x[v][5] == 300 and x[v][6] == 390:
                self.p.append(x[v])
            elif x[v][5] == 330 and x[v][6] == 390:
                self.q.append(x[v])
            elif x[v][5]== 300 and x[v][6] == 420:
                self.r.append(x[v])
            elif x[v][5] == 330 and x[v][6]== 420:
                self.s.append(x[v])
            elif x[v][5]== 300 and x[v][6] == 450:
                self.t.append(x[v])
            elif x[v][5] == 330 and x[v][6] == 450:
                self.u.append(x[v])
            else:
                print('error')
    def get_grapho(self):        #特殊组合
        x=[]
        y=[]
        for i in range(len(self.o)):
            x.append(self.o[i][1])
            y.append(self.o[i][2])
        plt.scatter(x,y,c='r')
        plt.show()
    def minchar(self):      #得出充电桩最小距离的最大值
        M = []
        for i in range(len(self.chardis)):
            m = []

            for j in range(len(self.chardis[i][1])):
                m.append(self.chardis[i][1][j][2])
            M.append(min(m))               #最大值为15990
    def groupO(self):
        x = np.array([0, 1])
        a = []
        for i in range(len(self.o)):
            b=[]
            b.append(self.o[i][0])
            y = np.array([self.o[i][1],self.o[i][2]])
            Ly = np.sqrt(y.dot(y))   #长度
            cosangle = x.dot(y) / Ly
            if self.o[i][1]<0:
                angle = np.arccos(cosangle)*360/2/np.pi
            else:
                angle=-np.arccos(cosangle)*360/2/np.pi
            b.append(angle)
            b.append(Ly)
            a.append(b)  # 每个o与y轴的夹角
        a.sort()  # 按从小到大
        #print(a)
        c=[]               #c为所有顾客群体的角度
        for j in range(len(self.customerloc)):
            d=[]
            d.append(j+1)
            y = np.array([self.customerloc[j+1][0],self.customerloc[j+1][1]])
            Ly = np.sqrt(y.dot(y))
            cosangle = x.dot(y) / Ly
            if self.customerloc[j+1][0]<0:
                angle = np.arccos(cosangle)*360/2/np.pi
            else:
                angle=-np.arccos(cosangle)*360/2/np.pi
            d.append(angle)
            d.append(Ly)
            c.append(d)  # 每个o与y轴的夹角
        self.angle=c
        #print(c)
        g={}
        for k in range(len(a)):
            s = [a[k][2]]
            for l in range(len(c)):
                #print(c[l][1]-a[k][1])
                if (c[l][1]-a[k][1]<1 and c[l][1]-a[k][1]>-1 and c[l][1]-a[k][1]!=0 and
                a[k][2]>c[l][2]):
                    s.append(c[l][0])
            g[a[k][0]]=s      #夹角之差在一定范围内且不超出
        gs=sorted(g.items(),key=lambda x:x[1])            #按距离排序
        gu=[]           #所有地点集合 按从近到远顺序
        for i in range(len(gs)):
            a=gs[i][1][1:]
            gu.append(a)
        #print(gu)

        for i in range(len(gu)):
            for j in range(len(gu[i])):
                for k in range(len(gu)-i-1):
                     if gu[i][j] in gu[i+k+1]:
                         gu[i+k+1].remove(gu[i][j])
        #print(gu)        #现在删除了重复的元素
        for i in range(len(gu)):
            gu[i]=[gs[i][0],gu[i]]
        #print(gu)         #更新数据添加标号
        for i in range(len(gu)):
           # if len(gu[i][1])<8:
                for j in range(20):
                    gu[i][1].append(self.dis[gu[i][0]-1][1][j][1])
        #print(gu)       #加上最近的点
        for i in range(len(gu)):                 #删除添加的重复项
             a=list(set(gu[i][1]))
             a.sort(key=gu[i][1].index)
             a.insert(0,gu[i][0])
             gu[i][1]=a                         #加上中心点
        #print(gu)
        gt=[]
        for i in range(len(gu)):
            t=[]                      #将储存以最晚时间形式
            for j in range(len(gu[i][1])):
                g=[]
                g.append(gu[i][1][j])
                g.append(self.orig[gu[i][1][j]-1][2])
                g.append(self.timewindows[gu[i][1][j]])     #加入时间窗
                g.append(self.package[gu[i][1][j]])           #加入物品信息
                t.append(g)
                t.sort(key=lambda x:(x[2][0],x[2][1]))   #根据开放时间排序，若相同则按结束时间
            gt.append(t)
            gu[i][1]=t
       # print(gu)          #gt包含了点 距离和时间窗
        RT=[]   #这一组的车辆集合           未计算返航
        #for i in range(len(gu)):
        #    for j in range(len(gu[i][1])):
        #        for k in range(len(gu)-i-1):
        #             if gu[i][1][j] in gu[i+k+1][1]:
        #                 gu[i+k+1][1].remove(gu[i][1][j])
        #print(gu)        #删除重复的点
        #print(gu)# 将规定点的位置加入
        grp=[]
        result=[]
        for i in range(len(gu)):        #全部用小车
            for j in range(len(gu[i][1])):
                if gu[i][0] in gu[i][1][j]:
                    gu[i].append(j)
            route = [[], [0, 0, ], 0, 0, 360, 100000, 0]
            # 包含车辆的路线信息 路程 时间 出发时间 充电次数  容纳量 剩余公里
            route[0].append(gu[i][0])                                #加上指定点
            route[1][0] += gu[i][1][gu[i][2]][3][0]                  #加上指点重量
            route[1][1] += gu[i][1][gu[i][2]][3][1]                  #加上指定体积
            route[3] += 30                                          #加上指定点的卸货时间
            for j in range(gu[i][2]-1, -1, -1):      #向前遍历
                if gu[i][1][j][2][0] < route[4]-(self.cuss[route[0][0]][1][gu[i][1][j][0]][1]+30) < gu[i][1][j][2][1]:
                    route[0].insert(0, gu[i][1][j][0])
                    route[1][0] += gu[i][1][j][3][0]  # 加上重量
                    route[1][1] += gu[i][1][j][3][1]  # 加上体积
                    route[2] += self.cuss[route[0][0]][1][route[0][1]][0]  # 加上距离
                    route[3] += (self.cuss[route[0][0]][1][route[0][1]][1] + 30)
                    route[4] -= (self.cuss[route[0][0]][1][route[0][1]][1] + 30)
                    route[5] -= self.cuss[route[0][0]][1][route[0][1]][0]  # 剩余里程
                    if route[1][0] > 2 or route[1][1] > 12:          #若超出配额则减去
                        route[1][0] -= gu[i][1][j][3][0]
                        route[1][1] -= gu[i][1][j][3][1]
                        route[2] -= self.cuss[route[0][0]][1][route[0][1]][0]
                        route[3] -= (self.cuss[route[0][0]][1][route[0][1]][1] + 30)
                        route[4] += (self.cuss[route[0][0]][1][route[0][1]][1] + 30)
                        route[5] += self.cuss[route[0][0]][1][route[0][1]][0]
                        route[0].pop(0)
            if route[1][0]+gu[i][1][gu[i][2]][3][0] < 2 and route[1][1]++gu[i][1][gu[i][2]][3][1] < 12:      #当还有剩余空间
                route.append(390)
                for k in range(gu[i][2]+1, len(gu[i][1])):   #向后遍历
                    if gu[i][1][k][2][0] < route[7] + (self.cuss[route[0][-1]][1][gu[i][1][k][0]][1] + 30) < \
                            gu[i][1][k][2][1]:
                        route[1][0] += gu[i][1][k][3][0]  # 加上重量
                        route[1][1] += gu[i][1][k][3][1]  # 加上体积
                        if route[1][0] > 2 or route[1][1] > 12:  # 若超出配额则减去
                            route[1][0] -= gu[i][1][k][3][0]
                            route[1][1] -= gu[i][1][k][3][1]
                            continue
                        route[2] += self.cuss[route[0][-1]][1][gu[i][1][k][0]][0]  # 加上距离
                        route[3] += (self.cuss[route[0][-1]][1][gu[i][1][k][0]][1] + 30)
                        route[7] += (self.cuss[route[0][-1]][1][gu[i][1][k][0]][1] + 30)
                        route[5] -= self.cuss[route[0][-1]][1][gu[i][1][k][0]][0]  # 剩余里程
                        route[0].append(gu[i][1][k][0])  # 在后面加上
            else:
                route.append(390)

            route[2] += self.orig[route[0][0] - 1][2]  # 起点距离
            route[3] += self.orig[route[0][0] - 1][3]  # 起点时间
            route[4] -= self.orig[route[0][0] - 1][3]
            route[5] -= self.orig[route[0][0] - 1][2]
            route[0].insert(0, 0)
            route.append(gu[i][0])

            if route[4] < 0:               #若不能到达原点
                route[1][0] -= self.package[route[0][1]][0]          #减去第一个点的包重量
                route[1][1] -= self.package[route[0][1]][1]            #减去第一个点的包裹体积
                route[2] -= self.orig[route[0][1] - 1][2]              #减去原点到第一个点的距离
                route[3] -= self.orig[route[0][1] - 1][3]              #减去原点到第一个点的时间
                route[4] += self.orig[route[0][1] - 1][3]            #时间补回
                route[5] += self.orig[route[0][1] - 1][2]         #里程补回
                route[2] -= self.cuss[route[0][1]][1][route[0][2]][0]      #减去第一个到第二个的距离
                route[3] -= (self.cuss[route[0][1]][1][route[0][2]][1] +30)           #减去第一个到第二个的时间
                route[4] += (self.cuss[route[0][1]][1][route[0][2]][1] + 30)             #加回时间
                route[5] += self.cuss[route[0][1]][1][route[0][2]][0]                   #补回里程
                route[2] += self.orig[route[0][2] - 1][2]                    #加上第二个点到原点的距离
                route[3] += self.orig[route[0][2] - 1][3]                   #加上第二个点的时间
                route[4] -= self.orig[route[0][2] - 1][3]
                route[5] -= self.orig[route[0][2] - 1][2]
                route[0].pop(1)
                route[7] = route[4]+route[3]

            for j in range(len(route[0])):  # 对于每个已经接待过的顾客
                for k in range(i + 1, len(gu)):  # 对于以后的所有待接待顾客群中
                    p = []
                    for h in range(len(gu[k][1])):  # 对于之后的每一个群体中
                        if route[0][j] in gu[k][1][h]:
                            p.append(h)  # p存着重复元素 从小到大
                    for g in range(len(p) - 1, -1, -1):
                        gu[k][1].pop(p[g])  # 删除重复元素

            if i==12 or i==33 or i==40 or i==15 or i==29:    #处理三个特殊点
                for n in range(len(route[0])):
                    if route[8] == route[0][n]:
                        x = n
                route[2] = self.orig[route[0][1] - 1][2]
                route[3] = self.orig[route[0][1] - 1][3]
                route[4] = self.timewindows[route[0][1]][0] + 30  # 为第一个点最早的点加卸货时间
                route[5] = 100000 - self.orig[route[0][1] - 1][2]
                if self.timewindows[route[0][1]][0] > self.orig[route[0][1] - 1][3]:
                    route[7] = self.timewindows[route[0][1]][0] - self.orig[route[0][1] - 1][3]
                else:
                    print('aadvance')
                for m in range(1, x - 2):  # 所有的剩余里程都为正
                    if self.timewindows[route[0][m + 1]][0]<= route[4] +self.cuss[route[0][m]][1][route[0][m + 1]][1]<=self.timewindows[route[0][m + 1]][1]:
                        route[2] += self.cuss[route[0][m]][1][route[0][m + 1]][0]  # 加上距离
                        route[3] += (self.cuss[route[0][m]][1][route[0][m + 1]][1] + 30)  # 加上时间
                        route[4] += (self.cuss[route[0][m]][1][route[0][m + 1]][1] + 30)
                        route[5] -= self.cuss[route[0][m]][1][route[0][m + 1]][0]  # 剩余里程
                    elif self.timewindows[route[0][m + 1]][0] > route[4] +self.cuss[route[0][m]][1][route[0][m + 1]][1]:
                        route.append(self.timewindows[route[0][m + 1]][0] - route[4] -self.cuss[route[0][m]][1][route[0][m + 1]][1])
                        route[2] += self.cuss[route[0][m]][1][route[0][m + 1]][0]  # 加上距离
                        route[3] += (self.cuss[route[0][m]][1][route[0][m + 1]][1] + 30)  # 加上时间
                        route[4] = self.timewindows[route[0][m + 1]][0]+30
                        route[5] -= self.cuss[route[0][m]][1][route[0][m + 1]][0]  # 剩余里程
                    else:print('error')

                route[2] += self.chardis[route[0][x - 2] - 1][1][0][2]
                route[3] += (self.chardis[route[0][x - 2] - 1][1][0][3] + 30)
                route[4] += (self.chardis[route[0][x - 2] - 1][1][0][3] + 30)
                route[5] = 100000
                R = route[0][x - 1]
                route[0][x - 1] = self.chardis[route[0][x - 2] - 1][1][0][1]  # 将x-2变为充电站
                route[1][0] -= self.package[R][0]
                route[1][1] -= self.package[R][1]
                route[6] += 1
                if self.timewindows[route[0][x]][0] <= route[4] + self.cuss[route[0][x - 1]][1][route[0][x]][1] <= \
                        self.timewindows[route[0][x]][1]:
                    route[2] += self.cuss[route[0][x - 1]][1][route[0][x]][0]
                    route[3] += (self.cuss[route[0][x - 1]][1][route[0][x]][1] + 30)
                    route[4] += (self.cuss[route[0][x - 1]][1][route[0][x]][1] + 30)
                    route[5] -= self.cuss[route[0][x - 1]][1][route[0][x]][0]
                if len(route[0])>x+1:
                    if self.timewindows[route[0][x+1]][0] <= route[4] + self.cuss[route[0][x ]][1][route[0][x+1]][1] <= \
                            self.timewindows[route[0][x+1]][1]:
                        route[2] += self.cuss[route[0][x]][1][route[0][x+1]][0]
                        route[3] += (self.cuss[route[0][x]][1][route[0][x+1]][1] + 30)
                        route[4] += (self.cuss[route[0][x]][1][route[0][x+1]][1] + 30)
                        route[5] -= self.cuss[route[0][x]][1][route[0][x+1]][0]
                route[2] += self.orig[route[0][-1] - 1][2]  # 回到原点距离
                route[3] += self.orig[route[0][-1] - 1][3]  # 总共用时时间
                route[4] += self.orig[route[0][-1] - 1][3]  # 回到原点时间
                route[5] -= self.orig[route[0][-1] - 1][2]  # 回到原点剩余里程
                route[0].append(0)  # 处理完等待的路线 剩余里程能够返回
                swap=route[4]
                route[4]=route[7]
                route[7]=swap
                continue
            if route[5]-self.orig[route[0][-1]-1][2]<0:                       #如果不能在里程内返航
                if route[5]-self.chardis[route[0][-1]-1][1][0][2]<0:         #只能中途充电 重新分配
                    for l in range(len(route[0])):
                        if route[8] == route[0][l]:
                             x = l
                    if len(route[0]) > x + 1: #满足基本点之后还有点
                        if route[5] + self.cuss[route[0][x]][1][route[0][x+1]][0] > self.chardis[route[0][x]-1][1][0][2]:
                            #如果减去最后一个之后能到达最近的充电站
                            route[1][0] -= self.package[route[0][-1]][0]
                            route[1][1] -= self.package[route[0][-1]][1]
                            route[2] -= self.cuss[route[0][x]][1][route[0][x+1]][0]
                            route[3] -= (self.cuss[route[0][x]][1][route[0][x+1]][1]+30)
                            route[7] -= (self.cuss[route[0][x]][1][route[0][x+1]][1]+30)
                            route[5] += self.cuss[route[0][x]][1][route[0][x+1]][0]
                            route[0].pop()
                            route[2] += self.chardis[route[0][-1] - 1][1][0][2]  # 加上去充电桩的距离
                            route[3] += (self.chardis[route[0][-1] - 1][1][0][3] + 30)
                            route[7] += (self.chardis[route[0][-1] - 1][1][0][3] + 30)
                            route[6] += 1
                            route[0].append(self.chardis[route[0][-1] - 1][1][0][1])  # 最后加上充电点
                            route[2] += self.orig[route[0][-1] - 1][2]  # 回到原点距离
                            route[3] += self.orig[route[0][-1] - 1][3]  # 总共用时时间
                            route[7] += self.orig[route[0][-1] - 1][3]  # 回到原点时间
                            route[0].append(0)  # 回到原点
                            continue           #结束此次循环
                    #print(route)
                    if self.timewindows[route[0][1]][0]>self.orig[route[0][1] - 1][3]:
                        route[4] = self.timewindows[route[0][1]][0] + 30  # 为第一个点最早的点加卸货时间
                    else:
                        route[4] = self.orig[route[0][1] - 1][3] + 30 #当前时间就为路上花费时间加卸货时间
                    route[3] = self.orig[route[0][1] - 1][3] + 30  # 第一个点卸货
                    route[2] = self.orig[route[0][1] - 1][2]
                    route[5] = 100000 - self.orig[route[0][1] - 1][2]
                    route.append(0)            #等待时间
                    if self.timewindows[route[0][1]][0] - self.orig[route[0][1] - 1][3]>0:
                        route[7] = self.timewindows[route[0][1]][0] - self.orig[route[0][1] - 1][3]  # 出发时间
                    else: route[7]=0     #若客户规定的最早时间不可以到达，则直接在8点出发
                    if x>3:
                        for m in range(1, x - 3):  # 所有的剩余里程都为正  不用检查时间窗 因为已经满足
                            if self.timewindows[route[0][m + 1]][0] <= route[4] +\
                                self.cuss[route[0][m]][1][route[0][m + 1]][1] <= self.timewindows[route[0][m + 1]][1]:
                                route[2] += self.cuss[route[0][m]][1][route[0][m + 1]][0]  # 加上距离
                                route[3] += (self.cuss[route[0][m]][1][route[0][m + 1]][1] + 30)  # 加上时间
                                route[4] += (self.cuss[route[0][m]][1][route[0][m + 1]][1] + 30)
                                route[5] -= self.cuss[route[0][m]][1][route[0][m + 1]][0]  # 剩余里程
                            elif self.timewindows[route[0][m + 1]][0] > route[4] +\
                                self.cuss[route[0][m]][1][route[0][m + 1]][1]:        #需要等待
                                route[9] += (
                                self.timewindows[route[0][m + 1]][0] - self.cuss[route[0][m]][1][route[0][m + 1]][1] -
                                route[4])
                                route[2] += self.cuss[route[0][m]][1][route[0][m + 1]][0]  # 加上距离
                                route[3] += (self.cuss[route[0][m]][1][route[0][m + 1]][1] + 30)  # 加上时间
                                route[4] = self.timewindows[route[0][m + 1]][0]+30
                                route[5] -= self.cuss[route[0][m]][1][route[0][m + 1]][0]  # 剩余里程
                            else:
                                print(self.timewindows[route[0][m + 1]])
                                print(route[3])
                    else: print('er')

                    if route[5]-self.chardis[route[0][x-3]-1][1][0][2]>0:     #若剩余里程能到充电站
                        route[2] += self.chardis[route[0][x-3]-1][1][0][2]
                        route[3] += (self.chardis[route[0][x-3]-1][1][0][3]+30)
                        route[4] += (self.chardis[route[0][x-3]-1][1][0][3]+30)
                        route[5] = 100000
                        R = route[0][x-2]
                        route[0][x-2]=self.chardis[route[0][x-3]-1][1][0][1]        #将x-2变为充电站
                        route[1][0] -= self.package[R][0]
                        route[1][1] -= self.package[R][1]
                        route[6] += 1

                        if self.timewindows[route[0][x-1]][0]<route[4] + self.cuss[route[0][x-2]][1][route[0][x-1]][1]<self.timewindows[route[0][x-1]][1]:
                            route[2] += self.cuss[route[0][x-2]][1][route[0][x-1]][0]
                            route[3] += (self.cuss[route[0][x-2]][1][route[0][x-1]][1]+30)
                            route[4] += (self.cuss[route[0][x-2]][1][route[0][x-1]][1]+30)
                            route[5] -= self.cuss[route[0][x-2]][1][route[0][x-1]][0]

                            if self.timewindows[route[0][x]][0]<=route[4] + self.cuss[route[0][x-1]][1][route[0][x]][1]<=self.timewindows[route[0][x]][1]:
                                route[2] += self.cuss[route[0][x - 1]][1][route[0][x]][0]
                                route[3] += (self.cuss[route[0][x - 1]][1][route[0][x]][1] + 30)
                                route[4] += (self.cuss[route[0][x - 1]][1][route[0][x]][1] + 30)
                                route[5] -= self.cuss[route[0][x - 1]][1][route[0][x]][0]
                                if len(route[0]) > x + 1:
                                    if self.timewindows[route[0][x + 1]][0] <= route[4] + \
                                            self.cuss[route[0][x]][1][route[0][x + 1]][1] <= \
                                            self.timewindows[route[0][x + 1]][1]:
                                        route[2] += self.cuss[route[0][x]][1][route[0][x + 1]][0]
                                        route[3] += (self.cuss[route[0][x]][1][route[0][x + 1]][1] + 30)
                                        route[4] += (self.cuss[route[0][x]][1][route[0][x + 1]][1] + 30)
                                        route[5] -= self.cuss[route[0][x]][1][route[0][x + 1]][0] #里程能返回

                            elif self.timewindows[route[0][x ]][0] > route[4] + self.cuss[route[0][x -1]][1][route[0][x]][1]:
                                route[9] += (self.timewindows[route[0][x]][0] - route[4] -self.cuss[route[0][x - 1]][1][route[0][x]][1])
                                route[2] += self.cuss[route[0][x-1]][1][route[0][x]][0]
                                route[3] += (self.cuss[route[0][x-1]][1][route[0][x]][1]+30)
                                route[4] = self.timewindows[route[0][x]][0]+30
                                route[5] -= self.cuss[route[0][x-1]][1][route[0][x]][0]

                            elif route[4] + self.cuss[route[0][x - 1]][1][route[0][x]][1] > self.timewindows[route[0][x]][1]:
                               # print(route[4] + self.cuss[route[0][x - 1]][1][route[0][x]][1])  #分别超时 1 3 1分钟
                              #  print(route)  #这三个已经提到前面解决
                                print('error')
                                print(route)
                                print(i)
                            route[2] += self.orig[route[0][-1] - 1][2]  # 回到原点距离
                            route[3] += self.orig[route[0][-1] - 1][3]  # 总共用时时间
                            route[4] += self.orig[route[0][-1] - 1][3]  # 回到原点时间
                            route[5] -= self.orig[route[0][-1] - 1][2]  # 回到原点剩余里程
                            route[0].append(0)  # 处理完等待的路线 剩余里程能够返回

                        elif self.timewindows[route[0][x-1]][0]>route[4] + self.cuss[route[0][x-2]][1][route[0][x-1]][1]: #若在规定时间之前到达
                            route[9] += (self.timewindows[route[0][x - 1]][0] - route[4] -self.cuss[route[0][x - 2]][1][route[0][x - 1]][1])  # 等待时间
                            route[2] += self.cuss[route[0][x - 2]][1][route[0][x - 1]][0]
                            route[3] += (self.cuss[route[0][x - 2]][1][route[0][x - 1]][1] + 30)
                            route[5] -= self.cuss[route[0][x - 2]][1][route[0][x - 1]][0]
                            route[4] = self.timewindows[route[0][x - 1]][0] + 30  # 车辆等待到临界时间去服务卸货

                            if self.timewindows[route[0][x]][0]<=route[4] + self.cuss[route[0][x-1]][1][route[0][x]][1]<=self.timewindows[route[0][x]][1]:
                                route[2] += self.cuss[route[0][x-1]][1][route[0][x]][0]
                                route[3] += (self.cuss[route[0][x-1]][1][route[0][x]][1]+30)
                                route[4] += (self.cuss[route[0][x-1]][1][route[0][x]][1]+30)
                                route[5] -= self.cuss[route[0][x-1]][1][route[0][x]][0]
                                if len(route[0])>x+1:
                                    if self.timewindows[route[0][x+1]][0]<=route[4]+self.cuss[route[0][x]][1][route[0][x+1]][1]<=self.timewindows[route[0][x+1]][1]:
                                        route[2] += self.cuss[route[0][x ]][1][route[0][x+1]][0]
                                        route[3] += (self.cuss[route[0][x ]][1][route[0][x+1]][1] + 30)
                                        route[4] += (self.cuss[route[0][x ]][1][route[0][x+1]][1] + 30)
                                        route[5] -= self.cuss[route[0][x ]][1][route[0][x+1]][0]    #里程能返回
                            elif self.timewindows[route[0][x ]][0] > route[4] + self.cuss[route[0][x -1]][1][route[0][x]][1]:
                                print(2)         #需要等待其实不存在
                                print('bucunzai')
                            elif route[4] + self.cuss[route[0][x - 1]][1][route[0][x]][1] > self.timewindows[route[0][x]][1]:
                                print(3)            #超出时间 其实不存在
                                print('bucunzaiaaa')
                            route[2] += self.orig[route[0][-1] - 1][2]  # 回到原点距离
                            route[3] += self.orig[route[0][-1] - 1][3]  # 总共用时时间
                            route[4] += self.orig[route[0][-1] - 1][3]  # 回到原点时间
                            route[5] -= self.orig[route[0][-1] - 1][2]  #回到原点剩余里程
                            route[0].append(0)   #处理完等待的路线 剩余里程能够返回

                        elif route[4] + self.cuss[route[0][x-2]][1][route[0][x-1]][1]>self.timewindows[route[0][x-1]][1]: #若会超时
                            print('ex')

                    else:     #x=7
                        route[2] += self.chardis[route[0][x - 4]-1][1][0][2]
                        route[3] += (self.chardis[route[0][x - 4]-1][1][0][3] + 30)
                        route[4] += (self.chardis[route[0][x - 4]-1][1][0][3] + 30)
                        route[5] = 100000
                        R = route[0][x - 3]
                        route[2] -= self.cuss[route[0][x - 4]][1][R][0]
                        route[3] -= (self.cuss[route[0][x - 4]][1][R][1]+30)
                        route[4] -= (self.cuss[route[0][x - 4]][1][R][1]+30)
                        route[0][x - 3] = self.chardis[route[0][x - 4]-1][1][0][1]
                        route[1][0] -= self.package[R][0]
                        route[1][1] -= self.package[R][1]
                        route[6] += 1
                        route[1][0] -= self.package[585][0]                 #我们减去了585这个点
                        route[1][1] -= self.package[585][1]
                        route[0].remove(585)                  #现在x为6
                        if self.timewindows[route[0][x-2]][0]<route[4] + self.cuss[route[0][x-3]][1][route[0][x-2]][1]<self.timewindows[route[0][x-2]][1]:
                            route[2] += self.cuss[route[0][x-3]][1][route[0][x-2]][0]
                            route[3] += (self.cuss[route[0][x-3]][1][route[0][x-2]][1]+30)
                            route[4] += (self.cuss[route[0][x-3]][1][route[0][x-2]][1]+30)
                            route[5] -= self.cuss[route[0][x-3]][1][route[0][x-2]][0]
                        else:
                            print('error')
                        if self.timewindows[route[0][x-1]][0]<route[4] + self.cuss[route[0][x-2]][1][route[0][x-1]][1]<self.timewindows[route[0][x-1]][1]:
                                route[2] += self.cuss[route[0][x - 2]][1][route[0][x - 1]][0]
                                route[3] += (self.cuss[route[0][x - 2]][1][route[0][x - 1]][1] + 30)
                                route[4] += (self.cuss[route[0][x - 2]][1][route[0][x - 1]][1] + 30)
                                route[5] -= self.cuss[route[0][x - 2]][1][route[0][x - 1]][0]
                        elif self.timewindows[route[0][x-1]][0]>route[4] + self.cuss[route[0][x-2]][1][route[0][x-1]][1]:
                            route[9] += self.timewindows[route[0][x-1]][0]-(route[4] + self.cuss[route[0][x-2]][1][route[0][x-1]][1])
                            route[2] += self.cuss[route[0][x - 2]][1][route[0][x - 1]][0]
                            route[3] += (self.cuss[route[0][x - 2]][1][route[0][x - 1]][1] + 30)
                            route[4] = self.timewindows[route[0][x-1]][0]+30
                            route[5] -= self.cuss[route[0][x - 2]][1][route[0][x - 1]][0]
                        else:
                            print('error')
                        if self.timewindows[route[0][x]][0]<=route[4] + self.cuss[route[0][x-1]][1][route[0][x]][1]<=self.timewindows[route[0][x]][1]:
                                    route[2] += self.cuss[route[0][x - 1]][1][route[0][x]][0]
                                    route[3] += (self.cuss[route[0][x - 1]][1][route[0][x]][1] + 30)
                                    route[4] += (self.cuss[route[0][x - 1]][1][route[0][x]][1] + 30)
                                    route[5] -= self.cuss[route[0][x - 1]][1][route[0][x]][0]     #里程能够回去
                        else:
                            print('error')
                        route[2] += self.orig[route[0][-1] - 1][2]  # 回到原点距离
                        route[3] += self.orig[route[0][-1] - 1][3]  # 总共用时时间
                        route[4] += self.orig[route[0][-1] - 1][3]  # 回到原点时间
                        route[5] -= self.orig[route[0][-1] - 1][2]  # 回到原点剩余里程
                        route[0].append(0)  # 处理完等待的路线 剩余里程能够返回
                    swap=route[4]
                    route[4]=route[7]
                    route[7]=swap
                else:               #如果剩余里程能够坚持去最近充电桩
                    route[2] += self.chardis[route[0][-1]-1][1][0][2]           #加上去充电桩的距离
                    route[3] += (self.chardis[route[0][-1]-1][1][0][3]+30)
                    route[7] += (self.chardis[route[0][-1]-1][1][0][3]+30)
                    route[6] += 1
                    route[0].append(self.chardis[route[0][-1]-1][1][0][1])  # 最后加上充电点
                    route[2] += self.orig[route[0][-1]-1][2]            #回到原点距离
                    route[3] += self.orig[route[0][-1]-1][3]            #总共用时时间
                    route[7] += self.orig[route[0][-1]-1][3]                    #回到原点时间
                    route[5] = 100000-self.orig[route[0][-1]-1][2]
                    route[0].append(0)  # 回到原点
            else:           #若能则直接返航
                route[2] += self.orig[route[0][-1] - 1][2]  # 回到原点距离
                route[3] += self.orig[route[0][-1] - 1][3]  # 总共用时时间
                route[7] += self.orig[route[0][-1] - 1][3]  # 回到原点时间
                route[5] -= self.orig[route[0][-1] - 1][2]
                route[0].append(0)

            for j in range(len(route[0])):  # 对于每个已经接待过的顾客
                for k in range(i + 1, len(gu)):  # 对于以后的所有待接待顾客群中
                    p = []
                    for h in range(len(gu[k][1])):  # 对于之后的每一个群体中
                        if route[0][j] in gu[k][1][h]:
                            p.append(h)  # p存着重复元素 从小到大
                    for g in range(len(p) - 1, -1, -1):
                        gu[k][1].pop(p[g])  # 删除重复元素
            if route[0][-1] != 0:
                print('omit')
            for p in route[0]:
                if p!=0 and p <=1000:
                    grp.append(p)
            if len(route)==10:
                re=[1, route[0], 8+route[4]//60 , route[4]%60, 8+route[7]//60, route[7]%60, route[2], route[2]*0.012, route[6]*50, route[9]*0.4 , 200]
            else:
                re = [1, route[0], 8 + route[4] // 60, route[4] % 60, 8 + route[7] // 60, route[7] % 60, route[2],
                      route[2] * 0.012, route[6] * 50, 0, 200]
            re.append(re[7]+re[8]+re[9]+re[10])
            re.append(route[6])
            result.append(re)
        for s in range(1,1001):
            if s not in grp:
                self.left.append(s)
        self.ts=grp
        return result
    def smag(self):     #全部用小车
        self.sm=[]            #用小车的集合
        self.la=[]                #用大车的集合
        for i in self.left:
            if self.orig[i-1][2]>25000:
                self.la.append(i)
            else:
                self.sm.append(i)
        a= []
        b= []
        c= []
        d= []
        for i in self.sm:
            if 0<self.angle[i-1][1]<60:
                a.append(i)
            elif 60<self.angle[i-1][1]<90:
                b.append(i)
            elif 90<self.angle[i-1][1]<180:
                c.append(i)
            elif -180<self.angle[i-1][1]<0:
                d.append(i)
            else:
                print(i)
        self.sm.clear()
        self.sm= [a, b, c, d]
    def largr(self):
        sp=[322, 499, 522, 979,394, 446, 512, 692, 803]
        for i in sp:
            self.la.remove(i)
        m=[]            #距离在25000到50000
        l=[]            #距离在50000以上
        s=[]
        for i in self.la:
            if self.orig[i-1][2] > 50000:
                l.append(i)                            #186
            elif 50000 > self.orig[i-1][2] > 36000:
                m.append(i)                            #192
            else:
                s.append(i)                             #182
        a = []
        b = []
        c = []
        d = []
        for i in l:
            if 20 < self.angle[i - 1][1] < 45:           #32个
                a.append(i)
            elif 45 < self.angle[i - 1][1] < 55:                  #44个
                b.append(i)
            elif 55 < self.angle[i - 1][1] < 65:                #59个
                c.append(i)
            elif 65 < self.angle[i - 1][1] < 81:                 #51个
                d.append(i)
            else:
                print(i)
        l.clear()
        l = [a, b, c, d]
        e = []
        f = []
        g = []
        h = []
        i = []
        j = []
        k = []
        o = []
        p = []
        for x in m:
            if 0 < self.angle[x - 1][1] < 40:           #34个
                e.append(x)
            elif 40 < self.angle[x - 1][1] < 70:                  #52个
                f.append(x)
            elif 70 < self.angle[x - 1][1] < 90:                #60个
                g.append(x)
            elif 90 < self.angle[x - 1][1] < 105:                    #32个
                h.append(x)
            elif -42 < self.angle[x - 1][1] < 0:                 #15个
                i.append(x)
            else:
                print(self.angle[x - 1])
        m.clear()
        m = [e, f, g, h, i]
        for x in s:
            if 0 < self.angle[x - 1][1] < 50:           #38个
                j.append(x)
            elif 50 < self.angle[x - 1][1] < 80:                  #66个
                k.append(x)
            elif 80 < self.angle[x - 1][1] < 110:                #47个
                o.append(x)
            elif -46 < self.angle[x - 1][1] < 0:                 #32个
                p.append(x)
            else:
                print(self.angle[x - 1])
        s.clear()
        s=[j ,k ,o , p]
        self.las=s
        self.lam=m
        self.lal=l
    def niche(self):
        a = [322, 499, 522, 979]
        am = {979:[[1.6, 9.996],[330, 390]], 522:[[0.1879, 0.2903], [90, 240]], 499:[[0.04024, 0.658],[330, 420]],
            322:[[0.02826, 0.0997], [330, 390]]}
        b = [394, 446, 512, 692, 803]
        bm = {394:[[0.08048,0.2328], [60,120]], 446:[[0.3688, 0.577],[60,240]], 512:[[0.22615,0.3522],[300, 420]],
            692:[[0.0105,0.08],[330, 450]], 803:[[0.93782, 1.4653],[300, 360]]}
        route1=[[], [1.8564 ,11.044], 0, 0, 0, 100000, 0, 0, 0, 1]   #地点 路程 花费时间 当前时间  剩余里程 开始时间 充电次数  车型 等待时间
        route2=[[], [1.62375 ,2.7073], 0, 0, 0, 100000, 0, 0, 0, 1]
        route1[0].append(522)
        route1[2]+= self.orig[521][2]
        route1[3]+= self.orig[521][3]+30
        route1[4]+= 240+30
        route1[5]-= self.orig[521][2]
        route1[6]+= 240-self.orig[521][3]
        route1[0].append(322)
        route1[2] += self.cuss[522][1][322][0]
        route1[3] += self.cuss[522][1][322][1]+30
        route1[4] = 330 + 30
        route1[5] -= self.cuss[522][1][322][0]
        route1[8] += 330-270-self.cuss[522][1][322][1]              #等待时间
        route1[0].append(979)
        route1[2] += self.cuss[322][1][979][0]
        route1[3] += self.cuss[322][1][979][1] + 30
        route1[4] += self.cuss[322][1][979][1] + 30
        route1[5] -= self.cuss[322][1][979][0]
        route1[0].append(499)
        route1[2] += self.cuss[499][1][979][0]
        route1[3] += self.cuss[499][1][979][1] + 30
        route1[4] += self.cuss[499][1][979][1] + 30
        route1[5] -= self.cuss[499][1][979][0]
        route1[0].append(self.chardis[498][1][0][1])
        route1[2] += self.chardis[498][1][0][2]
        route1[3] += self.chardis[498][1][0][3]+ 30
        route1[4] += self.chardis[498][1][0][3]+ 30
        route1[7] += 1
        route1[5] = 100000
        route1[2] += self.orig[route1[0][-1]-1][2]
        route1[3] += self.orig[route1[0][-1]-1][3]
        route1[4] += self.orig[route1[0][-1]-1][3]
        route1[5] -= self.orig[route1[0][-1]-1][2]
        route1[0].append(0)
        route2[0].append(394)
        route2[2]+= self.orig[393][2]
        route2[3] += self.orig[393][3]+30
        route2[4] += 120+30
        route2[5] -= self.orig[393][2]
        route2[6] = 120-self.orig[393][3]
        route2[0].append(446)
        route2[2] += self.cuss[394][1][446][0]
        route2[3] += self.cuss[394][1][446][1] + 30
        route2[4] += self.cuss[394][1][446][1] + 30
        route2[5] -= self.cuss[394][1][446][0]
        route2[0].append(512)
        route2[2] += self.cuss[512][1][446][0]
        route2[3] += self.cuss[512][1][446][1] + 30
        route2[4] = 300+30
        route2[5] -= self.cuss[512][1][446][0]
        route2[8] += 300-187-self.cuss[512][1][446][1]
        route2[0].append(803)
        route2[2] += self.cuss[512][1][803][0]
        route2[3] += self.cuss[512][1][803][1] + 30
        route2[4] += self.cuss[512][1][803][1] + 30
        route2[5] -= self.cuss[512][1][803][0]
        route2[0].append(692)
        route2[2] += self.cuss[692][1][803][0]
        route2[3] += self.cuss[692][1][803][1] + 30
        route2[4] += self.cuss[692][1][803][1] + 30
        route2[5] -= self.cuss[692][1][803][0]
        route2[0].append(0)
        route2[2] += self.orig[691][2]
        route2[3] += self.orig[691][3]
        route2[4] += self.orig[691][3]
        route2[5] -= self.orig[691][2]
        route2[0].insert(0,0)
        route1[0].insert(0,0)
        to=[route1,route2]
        result=[]
        for i in to:
            re = [1, i[0], 8 + i[6] // 60, i[6] % 60, 8 + i[4] // 60, i[4] % 60, i[2], i[2] * 0.012, i[7] * 50,
                  i[8] * 0.4, 200]
            re.append(re[7] + re[8] + re[9] + re[10])
            re.append(i[7])
            result.append(re)
        return result
    def checks(self,g,s):     #检查是否合格
        if s ==2:  #选择大车
            if sum(list(self.timewindows[i][0] for i in g)) < 2.5 and sum(list(self.timewindows[j][1] for j in g)) < 16:
                route=[[],0,0,0,120000,0,1]   #地点 路程 当前时间 开始时间  剩余里程 充电次数  车型 等待时间
                route[0].append(g[0])
                route[1]+=self.orig[g[0]-1][2]
                route[4]-=self.orig[g[0]-1][2]
                if self.timewindows[g[0]][0]>self.orig[g[0]-1][3]:
                    route[2]=self.timewindows[g[0]][0]
                    route[3]=self.timewindows[g[0]][0]-self.orig[g[0]-1][3]
                else:
                    route[2]=self.orig[g[0]-1][3]
                    route[3]=0
            else:
                return 'n'

        elif s ==1:   #选择小车 默认不用充电
            if sum(list(self.package[i][0] for i in g))< 2 and sum(list(self.package[j][1] for j in g)) < 12:
                route = [[], 0, 0, 0, 100000, 0, 1, 0]  # 地点 路程 当前时间 开始时间  剩余里程 充电次数  车型 等待时间
                route[0].append(g[0])
                route[1] += self.orig[g[0] - 1][2]
                route[4] -= self.orig[g[0] - 1][2]
                if self.timewindows[g[0]][0] > self.orig[g[0] - 1][3]:
                    route[2] = self.timewindows[g[0]][0]+30
                    route[3] = self.timewindows[g[0]][0] - self.orig[g[0] - 1][3]
                else:
                    route[2] = self.orig[g[0] - 1][3]+30
                    route[3] = 0
                for i in range(1,len(g)):   #从第二个到倒数第一个
                    if self.timewindows[g[i]][0] < route[2]+self.cuss[g[i-1]][1][g[i]][1] < self.timewindows[g[i]][1]:
                        route[0].append(g[i])
                        route[1] += self.cuss[g[i-1]][1][g[i]][0]
                        route[2] += self.cuss[g[i-1]][1][g[i]][1]+30
                        route[4] -= self.cuss[g[i-1]][1][g[i]][0]
                    elif route[2]+self.cuss[g[i-1]][1][g[i]][1] < self.timewindows[g[i]][0]:   #需要等待
                        route[0].append(g[i])
                        route[1] += self.cuss[g[i - 1]][1][g[i]][0]
                        route[2] += self.timewindows[g[i]][0] + 30
                        route[4] -= self.cuss[g[i - 1]][1][g[i]][0]
                        route[7] += self.timewindows[g[i]][0]-self.cuss[g[i-1]][1][g[i]][1]-route[2]  #等待时间

                    else:
                        return 0
                route[0].append(0)
                route[1] += self.orig[g[-1]-1][2]
                route[2] += self.orig[g[-1]-1][3]
                route[4] -= self.orig[g[-1]-1][2]
                route.append(route[1]*0.012+route[7]*0.4+200)       #成本
            else:
                return 0
            return route
        else:
            print('error')
    def smnew(self,group,size):
        gr={}
        g=group.copy()
        sm=self.sm
        for i in g:
            gr[i]=self.package[i]
        rc=[]

        while len(g) > 0:
            ra = [0, 0, []]
            if size == 0 :             #小于25000
                ran = random.choice([5, 6, 7])
            elif size== 1:            #2500-3600
                ran = random.choice([4, 5, 6, 7])
            elif size == 2:          #36000-50000
                ran = random.choice([5, 6, 4])
            elif size == 3:
                ran = random.choice([3, 4, 5, ])
            else:
                raise ValueError
            for j in range(ran):
                r = random.choice(g)
                ra[2].append(r)
                ra[0] += gr[r][0]
                ra[1] += gr[r][1]
                if ra[0] > 2 and ra[1] > 12:  # 超过便回溯
                    ra[2].pop()
                    ra[0] -= gr[r][0]
                    ra[1] -= gr[r][1]
                    break
                g.remove(r)
                if len(g) == 0:
                    break
            rd=[]
            for m in ra[2]:
                rd.append([m,self.timewindows[m]])
            rd.sort(key=lambda x:(x[1][0],x[1][1]))
            re=[]
            for l in rd:
                re.append(l[0])
            rc.append(re)
        #print(rc)
        return rc
    def smmain(self):
        gr=self.sm.copy()
        solution=[]
        result=[]
        for x in gr:
            de={}                                 #时间物品信息
            so=[]                              #时间排序
            for j in x:
                de[j]=[self.timewindows[j],self.package[j]]
                so.append([j,self.timewindows[j]])
            so.sort(key=lambda x:(x[1][0],x[1][1]))
            s=[]                               #按照时间排序
            for l in so:
                s.append(l[0])
            solu = []
            while len(s) > 0:
                route = [[], [0, 0], 0, 0, 0, 100000, 0, 1, 0]  # 地点 路程 当前时间 开始时间  剩余里程 充电次数  车型 等待时间
                route[0].append(s[0])
                route[1][0] += self.package[s[0]][0]
                route[1][1] += self.package[s[0]][1]
                route[2] += self.orig[s[0] - 1][2]
                if self.timewindows[s[0]][0] > self.orig[s[0] - 1][3]:
                    route[3] = self.timewindows[s[0]][0] + 30
                    route[4] = self.timewindows[s[0]][0] - self.orig[s[0] - 1][3]
                else:
                    route[3] = self.orig[s[0] - 1][3] + 30
                    route[4] = 0
                route[5] -= self.orig[s[0] - 1][2]  # 第一个的路程时间等信息
                s.remove(s[0])  # 第一个添加完成
                while route[1][0] < 2 and route[1][1] < 12:
                    if route[5] < self.chardis[route[0][-1] - 1][1][0][2]:
                        print(route)
                    if route[5] < 15000:
                        route[2] += self.chardis[route[0][-1]-1][1][0][2]
                        route[3] += self.chardis[route[0][-1]-1][1][0][3]+30
                        route[5] = 100000
                        route[0].append(self.chardis[route[0][-1]-1][1][0][1])
                        route[6] += 1
                    pre = []  # 备选按照距离排序
                    if route[0][-1] <1001:
                        for m in self.dis[route[0][-1] - 1][1]:  # m=[[1,2,3,4],[start,end,dis,time]]
                            if m[1] in s:
                                pre.append(m)
                    if len(pre) > 0:  # 如果备选集非空
                        L = len(route[0])  # 当前路径
                        for n in pre:
                            if self.timewindows[n[1]][0] < route[3] + n[3] < self.timewindows[n[1]][1]:
                                route[1][0] += self.package[n[1]][0]
                                route[1][1] += self.package[n[1]][1]
                                route[2] += n[2]
                                route[3] += n[3] + 30
                                route[5] -= n[2]
                                route[0].append(n[1])
                                s.remove(n[1])
                                break
                            elif 0 < self.timewindows[n[1]][0] - route[3] - n[3] < 30:  # 需要等待30分钟内
                                route[1][0] += self.package[n[1]][0]
                                route[1][1] += self.package[n[1]][1]
                                if route[1][0] > 2 or route[1][1] > 12:  # 超过则减去
                                    route[1][0] -= self.package[n[1]][0]
                                    route[1][1] -= self.package[n[1]][1]
                                    break
                                route[8] += (self.timewindows[n[1]][0] - route[3] - n[3])
                                route[2] += n[2]
                                route[3] = self.timewindows[n[1]][0] + 30
                                route[5] -= n[2]
                                route[0].append(n[1])
                                s.remove(n[1])
                                break
                        if L == len(route[0]):  # 如果上述没有添加
                            for i in s:
                                if self.timewindows[i][0] < route[3] + self.cuss[route[0][-1]][1][i][1] < \
                                        self.timewindows[i][1]:
                                    route[1][0] += self.package[i][0]
                                    route[1][1] += self.package[i][1]
                                    route[2] += self.cuss[route[0][-1]][1][i][0]
                                    route[3] += self.cuss[route[0][-1]][1][i][1] + 30
                                    route[5] -= self.cuss[route[0][-1]][1][i][0]
                                    route[0].append(i)
                                    s.remove(i)
                                    break
                                elif 0<self.timewindows[i][0] - route[3] - self.cuss[route[0][-1]][1][i][
                                    1] < 30:  # 需要等待
                                    route[1][0] += self.package[i][0]
                                    route[1][1] += self.package[i][1]
                                    if route[1][0] > 2 or route[1][1] > 12:  # 超过则减去
                                        route[1][0] -= self.package[i][0]
                                        route[1][1] -= self.package[i][1]
                                        break
                                    route[8] += (self.timewindows[i][0] - route[3]-self.cuss[route[0][-1]][1][i][1])
                                    route[2] += self.cuss[route[0][-1]][1][i][0]
                                    route[3] = self.timewindows[i][0] + 30
                                    route[5] -= self.cuss[route[0][-1]][1][i][0]
                                    route[0].append(i)
                                    s.remove(i)
                                    break
                        if L == len(route[0]):
                            break
                    else:  # 否则就直接添加下一个合法的
                        PL=len(route[0])
                        for i in s:
                            if self.timewindows[i][0] < route[3] + self.cuss[route[0][-1]][1][i][1] < \
                                    self.timewindows[i][1]:
                                route[1][0] += self.package[i][0]
                                route[1][1] += self.package[i][1]
                                route[2] += self.cuss[route[0][-1]][1][i][0]
                                route[3] += self.cuss[route[0][-1]][1][i][1] + 30
                                route[5] -= self.cuss[route[0][-1]][1][i][0]
                                route[0].append(i)
                                s.remove(i)
                                break
                            elif 0 < self.timewindows[i][0] - route[3] - self.cuss[route[0][-1]][1][i][1] < 30:  # 需要等待
                                route[1][0] += self.package[i][0]
                                route[1][1] += self.package[i][1]
                                if route[1][0] > 2 or route[1][1] > 12:  # 超过则减去
                                    route[1][0] -= self.package[i][0]
                                    route[1][1] -= self.package[i][1]
                                    break
                                route[8] += (self.timewindows[i][0] - route[3] - self.cuss[route[0][-1]][1][i][1])
                                route[2] += self.cuss[route[0][-1]][1][i][0]
                                route[3] = self.timewindows[i][0] + 30
                                route[5] -= self.cuss[route[0][-1]][1][i][0]
                                route[0].append(i)
                                s.remove(i)
                                break
                        if PL==len(route[0]):
                            break
                    if route[1][0] > 2 or route[1][1] > 12:  # 超过则减去
                        route[1][0] -= self.package[route[0][-1]][0]
                        route[1][1] -= self.package[route[0][-1]][1]
                        route[2] -= self.cuss[route[0][-1]][1][route[0][-2]][0]
                        route[3] -= (self.cuss[route[0][-1]][1][route[0][-2]][1]+30)
                        route[5] += self.cuss[route[0][-1]][1][route[0][-2]][0]
                        s.append(route[0][-1])
                        route[0].pop()
                        break
                    if route[5] < 0:
                        print('error')
                if route[5]< self.orig[route[0][-1]-1][2]:
                    route[2] += self.chardis[route[0][-1]-1][1][0][2]
                    route[3] += self.chardis[route[0][-1]-1][1][0][3]+30
                    route[5] = 100000
                    route[0].append(self.chardis[route[0][-1] - 1][1][0][1])
                    route[6] += 1
                route[2] += self.orig[route[0][-1]-1][2]
                route[3] += self.orig[route[0][-1]-1][3]
                route[5] -= self.orig[route[0][-1]-1][2]
                route[0].append(0)
                route[0].insert(0,0)
                solu.append(route)
                if route[5]<0:
                    print('charge')

                #print(route)
            #print(solu)
            solution.append(solu)
            mi=[]                  #个别值
            am=0
            solut = solu.copy()              #复制后删除
            for n in solu:
                am += len(n[0])           #每个长度
                if len(n[0]) < 5:
                    for m in n[0]:
                        if m != 0:
                            mi.append(m)
                    solu.remove(n)
            full=[]
            for i in mi:
                full.append([i,self.timewindows[i]])
            full.sort(key=lambda x:(x[1][0],x[1][1]))
            for i in range(len(full)):
                mi[i]=full[i][0]
            while len(mi) > 0:
                route = [[], [0, 0], 0, 0, 0, 100000, 0, 1, 0]  # 地点 路程 当前时间 开始时间  剩余里程 充电次数  车型 等待时间
                route[0].append(mi[0])
                route[1][0] += self.package[mi[0]][0]
                route[1][1] += self.package[mi[0]][1]
                route[2] += self.orig[mi[0] - 1][2]
                if self.timewindows[mi[0]][0] > self.orig[mi[0] - 1][3]:
                    route[3] = self.timewindows[mi[0]][0] + 30
                    route[4] = self.timewindows[mi[0]][0] - self.orig[mi[0] - 1][3]
                else:
                    route[3] = self.orig[mi[0] - 1][3] + 30
                    route[4] = 0
                route[5] -= self.orig[mi[0] - 1][2]  # 第一个的路程时间等信息
                mi.remove(mi[0])  # 第一个添加完成
                for i in mi:
                    if self.timewindows[i][0] < route[3] + self.cuss[route[0][-1]][1][i][1] < \
                            self.timewindows[i][1]:
                        route[1][0] += self.package[i][0]
                        route[1][1] += self.package[i][1]
                        route[2] += self.cuss[route[0][-1]][1][i][0]
                        route[3] += self.cuss[route[0][-1]][1][i][1] + 30
                        route[5] -= self.cuss[route[0][-1]][1][i][0]
                        route[0].append(i)
                        mi.remove(i)
                    elif self.timewindows[i][0] > route[3] + self.cuss[route[0][-1]][1][i][1]:  # 需要等待
                        route[1][0] += self.package[i][0]
                        route[1][1] += self.package[i][1]
                        if route[1][0] > 2 or route[1][1] > 12:  # 超过则减去
                            route[1][0] -= self.package[i][0]
                            route[1][1] -= self.package[i][1]
                        route[8] += (self.timewindows[i][0] - route[3] - self.cuss[route[0][-1]][1][i][1])
                        route[2] += self.cuss[route[0][-1]][1][i][0]
                        route[3] = self.timewindows[i][0] + 30
                        route[5] -= self.cuss[route[0][-1]][1][i][0]
                        route[0].append(i)
                        mi.remove(i)
                    if route[1][0] > 2 or route[1][1] > 12:  # 超过则减去
                        route[1][0] -= self.package[route[0][-1]][0]
                        route[1][1] -= self.package[route[0][-1]][1]
                        route[2] -= self.cuss[route[0][-1]][1][route[0][-2]][0]
                        route[3] -= (self.cuss[route[0][-1]][1][route[0][-2]][1]+30)
                        route[5] += self.cuss[route[0][-1]][1][route[0][-2]][0]
                        mi.append(route[0][-1])
                        route[0].pop()
                        break
                    if route[5]<0:
                        print('error')
                if route[5] < self.orig[route[0][-1]-1][2]:
                    route[2] += self.chardis[route[0][-1] - 1][1][0][2]
                    route[3] += self.chardis[route[0][-1] - 1][1][0][3] + 30
                    route[5] = 100000
                    route[0].append(self.chardis[route[0][-1] - 1][1][0][1])
                    route[6] += 1
                route[2] += self.orig[route[0][-1] - 1][2]
                route[3] += self.orig[route[0][-1] - 1][3]
                route[5] -= self.orig[route[0][-1] - 1][2]
                route[0].append(0)
                route[0].insert(0,0)
                solu.append(route)
                if route[5] < 0:
                    print('charge')
            for i in solu:
                re=[1, i[0], 8+i[4]//60 , i[4]%60, 8+i[3]//60, i[3]%60, i[2], i[2]*0.012, i[6]*50, i[8]*0.4, 200]
                re.append(re[7]+re[8]+re[9]+re[10])
                re.append(i[6])
                result.append(re)
        solution.append(solu)
        return result
    def larmain(self,group,s):
        gr=group.copy()
        solution = []
        result=[]
        if s == 1:
            size = 10000
        elif s== 2 :
            size = 18000
        elif s== 3 :
            size = 20000
        else:
            print('error')
        for x in gr:
            de = {}  # 时间物品信息
            so = []  # 时间排序
            for j in x:
                de[j] = [self.timewindows[j], self.package[j]]
                so.append([j, self.timewindows[j]])
            so.sort(key=lambda x: (x[1][0], x[1][1]))
            s = []  # 按照时间排序
            for l in so:
                s.append(l[0])
            solu = []
            while len(s) > 0:
                route = [[], [0, 0], 0, 0, 0, 120000, 0, 2, 0]  # 地点 路程 当前时间 开始时间  剩余里程 充电次数  车型 等待时间
                route[0].append(s[0])
                route[1][0] += self.package[s[0]][0]
                route[1][1] += self.package[s[0]][1]
                route[2] += self.orig[s[0] - 1][2]
                if self.timewindows[s[0]][0] > self.orig[s[0] - 1][3]:
                    route[3] = self.timewindows[s[0]][0] + 30
                    route[4] = self.timewindows[s[0]][0] - self.orig[s[0] - 1][3]
                else:
                    route[3] = self.orig[s[0] - 1][3] + 30
                    route[4] = 0
                route[5] -= self.orig[s[0] - 1][2]  # 第一个的路程时间等信息
                s.remove(s[0])  # 第一个添加完成

                while route[1][0] < 2.5 and route[1][1] < 16:
                    if route[5] < self.chardis[route[0][-1] - 1][1][0][2]:              #如果不够去最近的充电站
                        route[1][0] -= self.package[route[0][-1]][0]
                        route[1][1] -= self.package[route[0][-1]][1]
                        route[2] -= self.cuss[route[0][-1]][1][route[0][-2]][0]
                        route[3] -= (self.cuss[route[0][-1]][1][route[0][-2]][1] + 30)
                        route[5] += self.cuss[route[0][-1]][1][route[0][-2]][0]
                        s.append(route[0][-1])
                        route[0].pop()
                        route[2] += self.chardis[route[0][-1] - 1][1][0][2]
                        route[3] += self.chardis[route[0][-1] - 1][1][0][3] + 30
                        route[5] =120000
                        route[0].append(self.chardis[route[0][-1] - 1][1][0][1])
                        route[6] += 1
                    if route[5] < size:
                        route[2] += self.chardis[route[0][-1] - 1][1][0][2]
                        route[3] += self.chardis[route[0][-1] - 1][1][0][3] + 30
                        route[5] = 120000
                        route[0].append(self.chardis[route[0][-1] - 1][1][0][1])
                        route[6] += 1
                    pre = []  # 备选按照距离排序
                    if route[0][-1] <1001:
                        for m in self.dis[route[0][-1] - 1][1]:  # m=[[1,2,3,4],[start,end,dis,time]]
                            if m[1] in s:
                                pre.append(m)

                    if len(pre) > 0:  # 如果备选集非空
                        L = len(route[0])  # 当前路径
                        for n in pre:
                            if self.timewindows[n[1]][0] < route[3] + n[3] < self.timewindows[n[1]][1]:
                                route[1][0] += self.package[n[1]][0]
                                route[1][1] += self.package[n[1]][1]
                                route[2] += n[2]
                                route[3] += n[3] + 30
                                route[5] -= n[2]
                                route[0].append(n[1])
                                s.remove(n[1])
                                break
                            elif 0 < self.timewindows[n[1]][0] - route[3] - n[3] < 30:  # 需要等待30分钟内
                                route[1][0] += self.package[n[1]][0]
                                route[1][1] += self.package[n[1]][1]
                                if route[1][0] > 2.5 or route[1][1] > 16:  # 超过则减去
                                    route[1][0] -= self.package[n[1]][0]
                                    route[1][1] -= self.package[n[1]][1]
                                    break
                                route[8] += (self.timewindows[n[1]][0] - route[3] - n[3])
                                route[2] += n[2]
                                route[3] = self.timewindows[n[1]][0] + 30
                                route[5] -= n[2]
                                route[0].append(n[1])
                                s.remove(n[1])
                                break
                        if L == len(route[0]):  # 如果上述没有添加
                            for i in s:
                                if self.timewindows[i][0] < route[3] + self.cuss[route[0][-1]][1][i][1] < \
                                        self.timewindows[i][1]:
                                    route[1][0] += self.package[i][0]
                                    route[1][1] += self.package[i][1]
                                    route[2] += self.cuss[route[0][-1]][1][i][0]
                                    route[3] += self.cuss[route[0][-1]][1][i][1] + 30
                                    route[5] -= self.cuss[route[0][-1]][1][i][0]
                                    route[0].append(i)
                                    s.remove(i)
                                    break
                                elif 0 < self.timewindows[i][0] - route[3] - self.cuss[route[0][-1]][1][i][
                                    1] < 30:  # 需要等待
                                    route[1][0] += self.package[i][0]
                                    route[1][1] += self.package[i][1]
                                    if route[1][0] > 2.5 or route[1][1] > 16:  # 超过则减去
                                        route[1][0] -= self.package[i][0]
                                        route[1][1] -= self.package[i][1]
                                        break
                                    route[8] += (self.timewindows[i][0] - route[3] - self.cuss[route[0][-1]][1][i][1])
                                    route[2] += self.cuss[route[0][-1]][1][i][0]
                                    route[3] = self.timewindows[i][0] + 30
                                    route[5] -= self.cuss[route[0][-1]][1][i][0]
                                    route[0].append(i)
                                    s.remove(i)
                                    break
                        if L == len(route[0]):
                            break
                        if route[5] < 0:
                            print(route)
                    else:  # 否则就直接添加下一个合法的
                        PL = len(route[0])
                        for i in s:
                            if self.timewindows[i][0] < route[3] + self.cuss[route[0][-1]][1][i][1] < \
                                    self.timewindows[i][1]:
                                route[1][0] += self.package[i][0]
                                route[1][1] += self.package[i][1]
                                route[2] += self.cuss[route[0][-1]][1][i][0]
                                route[3] += self.cuss[route[0][-1]][1][i][1] + 30
                                route[5] -= self.cuss[route[0][-1]][1][i][0]
                                route[0].append(i)
                                s.remove(i)
                                break
                            elif 0 < self.timewindows[i][0] - route[3] - self.cuss[route[0][-1]][1][i][1] < 30:  # 需要等待
                                route[1][0] += self.package[i][0]
                                route[1][1] += self.package[i][1]
                                if route[1][0] > 2.5 or route[1][1] > 16:  # 超过则减去
                                    route[1][0] -= self.package[i][0]
                                    route[1][1] -= self.package[i][1]
                                    break
                                route[8] += (self.timewindows[i][0] - route[3] - self.cuss[route[0][-1]][1][i][1])
                                route[2] += self.cuss[route[0][-1]][1][i][0]
                                route[3] = self.timewindows[i][0] + 30
                                route[5] -= self.cuss[route[0][-1]][1][i][0]
                                route[0].append(i)
                                s.remove(i)
                                break
                        if PL == len(route[0]):
                            break
                    if route[1][0] > 2.5 or route[1][1] > 16:  # 超过则减去
                        route[1][0] -= self.package[route[0][-1]][0]
                        route[1][1] -= self.package[route[0][-1]][1]
                        route[2] -= self.cuss[route[0][-1]][1][route[0][-2]][0]
                        route[3] -= (self.cuss[route[0][-1]][1][route[0][-2]][1]+30)
                        route[5] += self.cuss[route[0][-1]][1][route[0][-2]][0]
                        s.append(route[0][-1])
                        route[0].pop()
                        break
                    if route[5] < 0:
                        route[1][0] -= self.package[route[0][-1]][0]
                        route[1][1] -= self.package[route[0][-1]][1]
                        route[2] -= self.cuss[route[0][-1]][1][route[0][-2]][0]
                        route[3] -= (self.cuss[route[0][-1]][1][route[0][-2]][1]+30)
                        route[5] += self.cuss[route[0][-1]][1][route[0][-2]][0]
                        s.append(route[0][-1])
                        route[0].pop()

                if route[5] < self.orig[route[0][-1]-1][2]:
                    route[2] += self.chardis[route[0][-1] - 1][1][0][2]
                    route[3] += self.chardis[route[0][-1] - 1][1][0][3] + 30
                    route[5] = 120000
                    route[0].append(self.chardis[route[0][-1] - 1][1][0][1])
                    route[6] += 1

                route[2] += self.orig[route[0][-1] - 1][2]
                route[3] += self.orig[route[0][-1] - 1][3]
                route[5] -= self.orig[route[0][-1] - 1][2]
                route[0].append(0)
                route[0].insert(0,0)

                solu.append(route)

                if route[5] < 0:
                    print(route)
                    print('charge1')
                    # print(route)
            # print(solu)
            solution.append(solu)
            mi = []  # 个别值
            am = 0
            solut = solu.copy()                #复制后再删除
            for n in solut:
                am += len(n[0])  # 每个长度
                if len(n[0]) < 5:
                    for m in n[0]:
                        if m != 0 and m< 1001:
                            mi.append(m)
                    solu.remove(n)
            full = []
            for i in mi:
                full.append([i, self.timewindows[i]])
            full.sort(key=lambda x: (x[1][0], x[1][1]))
            for i in range(len(full)):
                mi[i] = full[i][0]
            while len(mi) > 0:
                route = [[], [0, 0], 0, 0, 0, 120000, 0, 2, 0]  # 地点 路程 当前时间 开始时间  剩余里程 充电次数  车型 等待时间
                route[0].append(mi[0])
                route[1][0] += self.package[mi[0]][0]
                route[1][1] += self.package[mi[0]][1]
                route[2] += self.orig[mi[0] - 1][2]
                if self.timewindows[mi[0]][0] > self.orig[mi[0] - 1][3]:
                    route[3] = self.timewindows[mi[0]][0] + 30
                    route[4] = self.timewindows[mi[0]][0] - self.orig[mi[0] - 1][3]
                else:
                    route[3] = self.orig[mi[0] - 1][3] + 30
                    route[4] = 0
                route[5] -= self.orig[mi[0] - 1][2]  # 第一个的路程时间等信息
                mi.remove(mi[0])  # 第一个添加完成
                for i in mi:
                    if self.timewindows[i][0] < route[3] + self.cuss[route[0][-1]][1][i][1] < \
                            self.timewindows[i][1]:
                        route[1][0] += self.package[i][0]
                        route[1][1] += self.package[i][1]
                        if route[1][0] > 2.5 or route[1][1] > 16:  # 超过则减去
                            route[1][0] -= self.package[i][0]
                            route[1][1] -= self.package[i][1]
                            continue
                        route[2] += self.cuss[route[0][-1]][1][i][0]
                        route[3] += self.cuss[route[0][-1]][1][i][1] + 30
                        route[5] -= self.cuss[route[0][-1]][1][i][0]
                        route[0].append(i)
                        mi.remove(i)
                    elif self.timewindows[i][0] > route[3] + self.cuss[route[0][-1]][1][i][1]:  # 需要等待
                        route[1][0] += self.package[i][0]
                        route[1][1] += self.package[i][1]
                        if route[1][0] > 2.5 or route[1][1] > 16:  # 超过则减去
                            route[1][0] -= self.package[i][0]
                            route[1][1] -= self.package[i][1]
                            continue
                        route[8] += (self.timewindows[i][0] - route[3] - self.cuss[route[0][-1]][1][i][1])
                        route[2] += self.cuss[route[0][-1]][1][i][0]
                        route[3] = self.timewindows[i][0] + 30
                        route[5] -= self.cuss[route[0][-1]][1][i][0]
                        route[0].append(i)
                        mi.remove(i)
                    if route[1][0] > 2.5 or route[1][1] > 16:  # 超过则减去
                        route[1][0] -= self.package[route[0][-1]][0]
                        route[1][1] -= self.package[route[0][-1]][1]
                        route[2] -= self.cuss[route[0][-1]][1][route[0][-2]][0]
                        route[3] -= (self.cuss[route[0][-1]][1][route[0][-2]][1]+30)
                        route[5] += self.cuss[route[0][-1]][1][route[0][-2]][0]
                        mi.append(route[0][-1])
                        route[0].pop()
                        break
                    if route[5]<0:
                        print('error')
                if route[5] < self.orig[route[0][-1]-1][2]:
                    route[2] += self.chardis[route[0][-1] - 1][1][0][2]
                    route[3] += self.chardis[route[0][-1] - 1][1][0][3] + 30
                    route[5] = 120000
                    route[0].append(self.chardis[route[0][-1] - 1][1][0][1])
                    route[6] += 1
                route[2] += self.orig[route[0][-1] - 1][2]
                route[3] += self.orig[route[0][-1] - 1][3]
                route[5] -= self.orig[route[0][-1] - 1][2]
                route[0].append(0)
                route[0].insert(0,0)
                solu.append(route)
                if route[5] < 0:
                    print('charge')
            #print(solu)
            for i in solu:
                re=[2, i[0], 8+i[4]//60 , i[4]%60, 8+i[3]//60, i[3]%60, i[2], i[2]*0.014, i[6]*50, i[8]*0.4,300]
                re.append(re[7]+re[8]+re[9]+re[10])
                re.append(i[6])
                result.append(re)
        #print(result)
        solution.append(solu)
        return result
    def spe(self):
        f=[718 , 654, 790,354,230,154,923,66, 828,505, 795 ,745,618]
        so = []  # 时间排序
        for j in f:
            so.append([j, self.timewindows[j]])
        so.sort(key=lambda x: (x[1][0], x[1][1]))
        mi = []  # 按照时间排序
        for l in so:
            mi.append(l[0])
        solu=[]
        result=[]
        while len(mi) > 0:
            route = [[], [0, 0], 0, 0, 0, 120000, 0, 2, 0]  # 地点 路程 当前时间 开始时间  剩余里程 充电次数  车型 等待时间
            route[0].append(mi[0])
            route[1][0] += self.package[mi[0]][0]
            route[1][1] += self.package[mi[0]][1]
            route[2] += self.orig[mi[0] - 1][2]
            if self.timewindows[mi[0]][0] > self.orig[mi[0] - 1][3]:
                route[3] = self.timewindows[mi[0]][0] + 30
                route[4] = self.timewindows[mi[0]][0] - self.orig[mi[0] - 1][3]
            else:
                route[3] = self.orig[mi[0] - 1][3] + 30
                route[4] = 0
            route[5] -= self.orig[mi[0] - 1][2]  # 第一个的路程时间等信息
            mi.remove(mi[0])  # 第一个添加完成
            for i in mi:
                if self.timewindows[i][0] < route[3] + self.cuss[route[0][-1]][1][i][1] < \
                        self.timewindows[i][1]:
                    route[1][0] += self.package[i][0]
                    route[1][1] += self.package[i][1]
                    if route[1][0] > 2.5 or route[1][1] > 16:  # 超过则减去
                        route[1][0] -= self.package[i][0]
                        route[1][1] -= self.package[i][1]
                        continue
                    route[2] += self.cuss[route[0][-1]][1][i][0]
                    route[3] += self.cuss[route[0][-1]][1][i][1] + 30
                    route[5] -= self.cuss[route[0][-1]][1][i][0]
                    route[0].append(i)
                    mi.remove(i)
                elif self.timewindows[i][0] > route[3] + self.cuss[route[0][-1]][1][i][1]:  # 需要等待
                    route[1][0] += self.package[i][0]
                    route[1][1] += self.package[i][1]
                    if route[1][0] > 2.5 or route[1][1] > 16:  # 超过则减去
                        route[1][0] -= self.package[i][0]
                        route[1][1] -= self.package[i][1]
                        continue
                    route[8] += (self.timewindows[i][0] - route[3] - self.cuss[route[0][-1]][1][i][1])
                    route[2] += self.cuss[route[0][-1]][1][i][0]
                    route[3] = self.timewindows[i][0] + 30
                    route[5] -= self.cuss[route[0][-1]][1][i][0]
                    route[0].append(i)
                    mi.remove(i)
                if route[1][0] > 2.5 or route[1][1] > 16:  # 超过则减去
                    route[1][0] -= self.package[route[0][-1]][0]
                    route[1][1] -= self.package[route[0][-1]][1]
                    route[2] -= self.cuss[route[0][-1]][1][route[0][-2]][0]
                    route[3] -= (self.cuss[route[0][-1]][1][route[0][-2]][1]+30)
                    route[5] += self.cuss[route[0][-1]][1][route[0][-2]][0]
                    mi.append(route[0][-1])
                    route[0].pop()
                    break
                if route[5] < 0:
                    route[1][0] -= self.package[route[0][-1]][0]
                    route[1][1] -= self.package[route[0][-1]][1]
                    route[2] -= self.cuss[route[0][-1]][1][route[0][-2]][0]
                    route[3] -= (self.cuss[route[0][-1]][1][route[0][-2]][1] + 30)
                    route[5] += self.cuss[route[0][-1]][1][route[0][-2]][0]
                    mi.append(route[0][-1])
                    route[0].pop()
            if route[5] < self.orig[route[0][-1] - 1][2]:
                route[2] += self.chardis[route[0][-1] - 1][1][0][2]
                route[3] += self.chardis[route[0][-1] - 1][1][0][3] + 30
                route[5] = 120000
                route[0].append(self.chardis[route[0][-1] - 1][1][0][1])
                route[6] += 1
            route[2] += self.orig[route[0][-1] - 1][2]
            route[3] += self.orig[route[0][-1] - 1][3]
            route[5] -= self.orig[route[0][-1] - 1][2]
            route[0].append(0)
            route[0].insert(0, 0)
            if route[1][0] > 2.5 or route[1][1] > 16:
                print(route)
            solu.append(route)
            if route[5] < 0:
                print('charge')

        # print(solu)
        for i in solu:
            re = [2, i[0], 8 + i[4] // 60, i[4] % 60, 8 + i[3] // 60, i[3] % 60, i[2], i[2] * 0.014, i[6] * 50,
                  i[8] * 0.4, 300]
            re.append(re[7] + re[8] + re[9] + re[10])
            re.append(i[6])
            result.append(re)
        return result
    def check(self,g):
        for i in range(70):
            wei=[]
            vol=[]
            for j in g[i][1]:
                if j >0 and j< 1001:
                    wei.append(self.package[j][0])
                    vol.append(self.package[j][1])
            if sum(wei) >2 or sum(vol)>12:
                print('packerror')
            stt = (g[i][2] - 8) * 60 + g[i][3]  # 当前时间
            ent = (g[i][4] - 8) * 60 + g[i][5]  # 结束时间
            wat = 0  # 等待时间
            dis = 0  # 路程
            cha = 0  # 充电次数
            rem = 100000
            for j in range(len(g[i][1]) - 2):
                if g[i][1][j+1] < 1001:                    #下一个是顾客
                    if self.timewindows[g[i][1][j + 1]][0] <= stt + self.cuss[g[i][1][j]][1][g[i][1][j + 1]][1] <= \
                            self.timewindows[g[i][1][j + 1]][1]:                #不需要等待
                        stt += self.cuss[g[i][1][j]][1][g[i][1][j + 1]][1]+30
                        dis += self.cuss[g[i][1][j]][1][g[i][1][j + 1]][0]
                        rem -= self.cuss[g[i][1][j]][1][g[i][1][j + 1]][0]
                        if rem <0:
                            print(g[i])
                            print(rem)
                    elif self.timewindows[g[i][1][j + 1]][0] > stt + self.cuss[g[i][1][j]][1][g[i][1][j + 1]][1]:

                        wat += self.timewindows[g[i][1][j + 1]][0] - (stt + self.cuss[g[i][1][j]][1][g[i][1][j + 1]][1])
                        stt = self.timewindows[g[i][1][j + 1]][0] + 30
                        dis += self.cuss[g[i][1][j]][1][g[i][1][j + 1]][0]
                        rem -= self.cuss[g[i][1][j]][1][g[i][1][j + 1]][0]
                        if rem < 0:
                            print(g[i])
                            print(rem)
                    else:
                        print(g[i])
                        print(g[i][1][j + 1])
                        print('timewin')
                        print(self.timewindows[g[i][1][j + 1]])
                        print(stt)
                        print(self.cuss[g[i][1][j]][1][g[i][1][j + 1]])

                else: #是充电桩
                    stt += self.cuss[g[i][1][j]][1][g[i][1][j + 1]][1]+30
                    dis += self.cuss[g[i][1][j]][1][g[i][1][j + 1]][0]
                    rem =100000
                    cha += 1
            stt += self.cuss[g[i][1][-2]][1][0][1]
            dis += self.cuss[g[i][1][-2]][1][0][0]
            rem -= self.cuss[g[i][1][-2]][1][0][0]
            if rem < 0:             #需要充电
                print(g[i])
                print(rem)
                print('charge1')
            if stt!=ent:       #时间不对
                print(g[i])
                print(stt)
                print(ent)
                print('time')
            if wat*0.4 != g[i][9]:           #等待不对
                print(g[i])
                print('wait')
                print(wat)
            if cha!= g[i][12]:            #充电次数不对
                print(g[i])
                print(g[i][12])
                print(cha)
                print('charge')
            if dis!= g[i][6]:
                print(g[i])
                print(g[i][6])
                print(dis)
                print('distance')
        for i in range(71,len(g)):
            wei=[]
            vol=[]
            for j in g[i][1]:
                if j >0 and j< 1001:
                    wei.append(self.package[j][0])
                    vol.append(self.package[j][1])
            if sum(wei) >2.5 or sum(vol)>16:
                print('packerror')
                print(g[i])
            stt = (g[i][2] - 8) * 60 + g[i][3]  # 当前时间
            ent = (g[i][4] - 8) * 60 + g[i][5]  # 结束时间
            wat = 0  # 等待时间
            dis = 0  # 路程
            cha = 0  # 充电次数
            rem = 120000
            for j in range(len(g[i][1]) - 2):
                if g[i][1][j+1] < 1001:                    #下一个是顾客
                    if self.timewindows[g[i][1][j + 1]][0] <= stt + self.cuss[g[i][1][j]][1][g[i][1][j + 1]][1] <= \
                            self.timewindows[g[i][1][j + 1]][1]:                #不需要等待
                        stt += self.cuss[g[i][1][j]][1][g[i][1][j + 1]][1]+30
                        dis += self.cuss[g[i][1][j]][1][g[i][1][j + 1]][0]
                        rem -= self.cuss[g[i][1][j]][1][g[i][1][j + 1]][0]
                        if rem <0:
                            print(g[i])
                            print(rem)
                    elif self.timewindows[g[i][1][j + 1]][0] > stt + self.cuss[g[i][1][j]][1][g[i][1][j + 1]][1]:

                        wat += self.timewindows[g[i][1][j + 1]][0] - (stt + self.cuss[g[i][1][j]][1][g[i][1][j + 1]][1])
                        stt = self.timewindows[g[i][1][j + 1]][0] + 30
                        dis += self.cuss[g[i][1][j]][1][g[i][1][j + 1]][0]
                        rem -= self.cuss[g[i][1][j]][1][g[i][1][j + 1]][0]
                        if rem < 0:
                            print(g[i])
                            print(rem)
                    else:
                        print(g[i])
                        print(g[i][1][j + 1])
                        print('timewin')
                        print(self.timewindows[g[i][1][j + 1]])
                        print(stt)
                        print(self.cuss[g[i][1][j]][1][g[i][1][j + 1]])

                else: #是充电桩
                    stt += self.cuss[g[i][1][j]][1][g[i][1][j + 1]][1]+30
                    dis += self.cuss[g[i][1][j]][1][g[i][1][j + 1]][0]
                    rem = 120000
                    cha += 1
            stt += self.cuss[g[i][1][-2]][1][0][1]
            dis += self.cuss[g[i][1][-2]][1][0][0]
            rem -= self.cuss[g[i][1][-2]][1][0][0]
            if rem < 0:             #需要充电
                print(g[i])
                print(rem)
                print('charge1')
            if stt!=ent:       #时间不对
                print(g[i])
                print(stt)
                print(ent)
                print('time')
            if wat*0.4 != g[i][9]:           #等待不对
                print(g[i])
                print('wait')
                print(wat)
            if cha!= g[i][12]:            #充电次数不对
                print(g[i])
                print(g[i][12])
                print(cha)
                print('charge')
            if dis!= g[i][6]:
                print(g[i])
                print(g[i][6])
                print(dis)
                print('distance')
    def dischech(self,g):
        for i in g:
            if i[0] == 1:
                full = 100000
            elif i[0] == 2:
                full = 120000
            else:
                print('error')
            dis=0                    #距离
            rem=0                      #里程
            for j in range(len(i[1])-1):
                dis += self.cuss[i[1][j]][1][i[1][j+1]][0]           #行驶距离增加
                full -= self.cuss[i[1][j]][1][i[1][j+1]][0]            #里程减少
                if full <0:                        #当里程为负数
                    print('chargeerror')
                    print(i)
                if i[1][j+1] >1000:                #当下一个点是充电站
                    if i[0] == 1:
                        full = 100000
                    elif i[0] == 2:
                        full = 120000
                    else:
                        print('error')

            if dis!= i[6]:
                print(dis)
                print(i[6])
g=graph([116.571614,39.792844])
g.get_cusimf()       #初始化顾客信息
g.get_time()         #初始化时间窗
g.get_item()         #初始化物品信息
g.get_loc()          #初始化地理位置
g.readinput()        #初始化距离
g.get_splitt()
sp=g.groupO()
#0-935-300  85+12   11.13  11.13.30
g.smag()
g.largr()
si=g.spe()            #单独组合
n=g.niche()                #单独组合
ss=g.smmain()              #小车
s=g.larmain(g.las,1)              #大车小距离
m=g.larmain(g.lam,2)                   #大车中距离
l=g.larmain(g.lal,3)                   #大车大距离
result=sp+n+ss+s+m+l
le = 0
#for i in result:
  #  for j in i[1]:
  #      if i[1][-1] !=0:
   #         print(i)
   #     if j!=0 and j<1001:
   #         le+=1
   # if len(i[1])<4:
   #         print(i[1])
res = result.copy()
for i in res:
    if len(i[1])<4:
        result.remove(i)
result+=si
#print(result)
g.check(result)
g.dischech(result)
end = time.clock()
#print('Running time: %s Seconds'%(end-start))
zero=0
lis=[]
le=0
for i in result:
    for j in i[1]:
        if j==0:
            zero+=1
        if i[1][-1] !=0:
            print(i)
        if j!=0 and j<1001:
            lis.append(j)
            le+=1
#print(le)
#print(len(result))
#print(zero)
ls=list(range(1,1001))
lis.sort()
#print(lis)
for i in range(1000):           #查漏补缺
    lis[i] -= ls[i]
    if lis[i]!=0:
        print(i)
#print(le)
#file_write_obj = open("result.txt", 'w')
#for var in result:
  #  a=str(var)
 #   file_write_obj.writelines(a)
 #   file_write_obj.write('\n')
#file_write_obj.close()
#Running time: 4.458761879990252 Seconds

#268 744 827

#745
#828
