import math
import numpy as np
import time
import matplotlib.pyplot as plt
def timetrans(s):             #将时间化为分钟
    a=s.split(':')
    a[0]=int(a[0])*60+int(a[1])-8*60
    a.pop()
    return(a[0])
timetrans('13:00')
cus=[]
#with open('input_node.csv') as file:
#    count=len(file.readlines())
#    print(count)
for line in open('customers.txt').readlines():        #顾客信息
    line=line.strip('\n')
    a=line.split(',')
    a[0]=int(a[0])
    a[1]=float(a[2])
    a[2]=float(a[3])
    a[3] = float(a[4])
    a[4] = float(a[5])
    a[5] = timetrans(a[6])
    a[6] = timetrans(a[7])
    del a[7]
    cus.append(a)
#print(cus)
charger=[]

for line in open('charger.txt').readlines():     #充电桩信息
    line = line.strip('\n')
    a = line.split(',')
    a[0] = int(a[0])-1000
    a[1] = float(a[2])
    a[2] = float(a[3])
    del a[3], a[4], a[5], a[4], a[3]
    charger.append(a)

def get_cloc():
        a=cus
        b={}
        for i in range(len(a)):

            e0=(a[i][1]-116.571614)*111000
            f0=(a[i][2]-39.792844)*111000*math.cos(a[i][2]/180*math.pi)
            g0=[e0,f0]
            b[i+1]=g0
        customerloc=b
        return b
def get_ch():
        c=charger
        d={}
        for j in range(len(c)):
         #   print((c[j][1]-116.571614)*111000)
            e=(c[j][1]-116.571614)*111000
            f=(c[j][2]-39.792844)*111000*math.cos(c[j][2]/180*math.pi)
            g=[e,f]
            d[j+1]=g
        charger1=d
        #print(customerloc)
        return d
def get_item():
    a = cus
    b = {}
    for i in range(len(a)):
        c=a[i][3]

        d=a[i][4]
        b[i + 1] = [c,d]
    package = b
    print(package)
def get_time():
    a = cus
    b = {}
    for i in range(len(a)):
        c=a[i][5]
        d=a[i][6]
        b[i + 1] = [c,d]
    timewindows = b
    #print(timewindows)
    return timewindows

def get_graph():  # 展示顾客，充电站，配送点地理信息
    xi = []  # 客户x轴集合
    yi = []  # 客户y轴集合
    for i in range(len(get_cloc())):
        xi.append(get_cloc()[i + 1][0])
        yi.append(get_cloc()[i + 1][1])
    plt.scatter(xi, yi, color='r')

    xj = []  # 充电站x轴集合
    yj = []  # 充电站y轴集合
    for j in range(len(get_ch())):
        xj.append(get_ch()[j + 1][0])
        yj.append(get_ch()[j + 1][1])
    plt.scatter(xj, yj, color='b')
    plt.scatter(0, 0, c='y', s=60)
    plt.show()
#get_time()
def get_split():  #根据规定时间分类
    x=get_time()
    a=[]             #9-10       1
    b=[]             #9.5-10.5    1
    c=[]             #9-11      2
    d=[]             #9.5-11    1.5
    e=[]             #10-11     1
    f=[]             #9-12      3
    g=[]             #9.5-12    2.5
    h=[]             #10-12     2
    i=[]             #11-12     1
    j=[]             #11-13     2
    k=[]             #11.5-13   1.5
    l=[]             #11-13.5   2.5
    m=[]             #11.5-13.5  2
    n=[]             #13-14      1
    o=[]             #13.5-14    0.5
    p=[]             #13-14.5    1.5
    q=[]             #13.5-14.5   1
    r=[]             #13-15       2
    s=[]             #13.5-15     1.5
    t=[]             #13-15.5     2.5
    u=[]             #13.5-15.5    2
    for v in range(len(x)):
        if x[v+1][0]==60 and x[v+1][1]==120:
            a.append(v+1)
        elif x[v+1][0]==90 and x[v+1][1]==150:
            b.append(v+1)
        elif x[v+1][0]==60 and x[v+1][1]==180:
            c.append(v+1)
        elif x[v+1][0]==90 and x[v+1][1]==180:
            d.append(v+1)
        elif x[v+1][0]==120 and x[v+1][1]==180:
            e.append(v+1)
        elif x[v+1][0]==60 and x[v+1][1]==240:
            f.append(v+1)
        elif x[v+1][0]==90 and x[v+1][1]==240:
            g.append(v+1)
        elif x[v+1][0]==120 and x[v+1][1]==240:
            h.append(v+1)
        elif x[v+1][0]==180 and x[v+1][1]==240:
            i.append(v+1)
        elif x[v+1][0]==180 and x[v+1][1]==300:
            j.append(v+1)
        elif x[v+1][0]==210 and x[v+1][1]==300:
            k.append(v+1)
        elif x[v+1][0]==180 and x[v+1][1]==330:
            l.append(v+1)
        elif x[v+1][0]==210 and x[v+1][1]==330:
            m.append(v+1)
        elif x[v+1][0]==300 and x[v+1][1]==360:
            n.append(v+1)
        elif x[v+1][0]==330 and x[v+1][1]==360:
            o.append(v+1)
        elif x[v+1][0]==300 and x[v+1][1]==390:
            p.append(v+1)
        elif x[v+1][0]==330 and x[v+1][1]==390:
            q.append(v+1)
        elif x[v+1][0]==300 and x[v+1][1]==420:
            r.append(v+1)
        elif x[v+1][0]==330 and x[v+1][1]==420:
            s.append(v+1)
        elif x[v+1][0]==300 and x[v+1][1]==450:
            t.append(v+1)
        elif x[v+1][0]==330 and x[v+1][1]==450:
            u.append(v+1)
        else:
            raise ValueError

def readinput():
    dis=[]          #所有距离表
    for line in open('input_distance-time.txt').readlines():
        line = line.strip('\n')
        a = line.split(',')
        a[0] = int(a[1])
        a[1] = int(a[2])
        a[2] = int(a[3])
        a[3] = int(a[4])
        del a[4]
        dis.append(a)
    gro=[]             #客户点到各地距离
    char=[]
    start=[]  #原点距离
    for i in range(1100):
        start.append(dis[i])
    del dis[:1100]         #dis为客户
    for j in range(1000):
       gro.append([j+1,dis[j*1100:(j+1)*1100]])
    for i in range(len(gro)):
        char.append([i+1,gro[i][1][1000:]])
    for i in range(len(char)):
        char[i][1]=sorted(char[i][1],key=lambda x:x[2])
        del (char[i][1])[20:]
    print(gro[1][1][:1000])
    for i in range(len(gro)):
        del (gro[i][1])[0]
        del (gro[i][1])[999:]
        gro[i][1]=sorted(gro[i][1],key=lambda x:x[2])
        del (gro[i][1])[20:]
    print(gro)

readinput()

#

