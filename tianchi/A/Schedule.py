import numpy as np
import pandas as pd
import random
from pandas import Series, DataFrame


class schedule(object):

    def __init__(self, data):
        self.data = data
        self.machine = DataFrame
        self.app = Series
        self.schedule = Series            #已经部署的实例
        self.icpb = Series
        self.single = Series
        self.twice = Series
        self.trip = Series
        self.qua = Series
        self.used = DataFrame            #已经使用的机器资源情况
        self.avalable = []        #可用机器

    def read(self):
        inc = pd.read_csv('incompatible.csv', header=None)
        incom = {'app_1008': ['app_4027']}
        for i in range(1, len(inc[0])):
            if inc[0][i-1] != inc[0][i]:
                incom[inc[0][i]] = []
                incom[inc[0][i]].append(inc[1][i])
            else:
                incom[inc[0][i]].append(inc[1][i])
        self.icpb = Series(incom)       #不兼容的
        machine = pd.read_csv('scheduling_preliminary_machine_resources_20180606.csv', header=None,
                              names=['name', 'cpu', 'memo', 'disk', 'p', 'm', 'pm'])
        a = DataFrame(machine[['cpu', 'memo', 'disk', 'p', 'm', 'pm']],)
        a.index = list(machine['name'])
        self.machine = a                        #每个机器的信息，容量
        ap = pd.read_csv('belong.csv', header=None)
        app = {'app_1': ['inst_95888']}
        for i in range(1, len(ap[0])):
            if ap[1][i-1] != ap[1][i]:
                app[ap[1][i]] = []
                app[ap[1][i]].append(ap[0][i])
            else:
                app[ap[1][i]].append(ap[0][i])
        self.app = Series(app)                  #每个APP所有的实例
        inf = pd.read_csv('resources.csv', header=None)
        ma = DataFrame(inf[[1, 2, 3, 4]])
        ma.index = list(inf[0])
        ma.columns = ['disk', 'p', 'm', 'pm']
        lis = []
        cpum = []
        with open('cpu.csv') as cpu:
            for line in cpu.readlines():
                line = line.strip('\n')
                a = line.split(',')
                row = []
                for i in a:
                    row.append(float(i))
                rowmean = np.mean(row)
                lis.append(row)
                cpum.append(rowmean)
        mem = []
        memom = []
        with open('memo.csv') as memo:
            for line in memo.readlines():
                line = line.strip('\n')
                b = line.split(',')
                row = []
                for i in b:
                    row.append(float(i))
                rowmean = np.mean(row)
                mem.append(row)
                memom.append(rowmean)
        ma['cpu'] = lis
        ma['memo'] = mem
        ma['cpum'] = cpum
        ma['memom'] = memom
        self.source = ma              #每个APP占有的资源
        self.avalable = list(self.machine.index)

    def nichi(self):   #优先处理22个PM类约束
        '''
        app_22  app_80  app_255  app_1222  app_1637
        app_3414  app_4210  app_4608
        app_6683  app_7102   app_8223
        these apps have P PM as 1
        '''
        nichi_index = ['app_22',  'app_255', 'app_1222', 'app_1637', 'app_3414', 'app_4210', 'app_4608',
                       'app_6683', 'app_7102', 'app_80', 'app_8223']
        icpb = {}
        for i in nichi_index:
            icpb[i] = []
            if i in self.icpb.index:
                for j in self.icpb[i]:
                    if j in nichi_index:
                        icpb[i].append(j)
        icpb = {'app_1222': ['app_1222'], 'app_8223': ['app_8223']}
        set0 = {}
        mac = 0
        #print(len(self.app['app_8223']))    #130
        #print(len(self.app['app_1637']))      #137
        #print(len(self.app['app_80']))        #145
        #print(len(self.app['app_4210']))      #98
        while len(self.app['app_8223']) > 0:
            machine = [['app_8223', self.app['app_8223'][-1]], ['app_1637', self.app['app_1637'][-1]],
                     ['app_80', self.app['app_80'][-1]] ]
            self.app['app_8223'].pop()
            self.app['app_1637'].pop()
            self.app['app_80'].pop()
            set0[self.avalable[mac]] = machine
            mac += 1
        if len(self.app['app_8223']) == 0:
            del self.app['app_8223']
        else: print('delerror')
        nichi_index = ['app_22', 'app_255', 'app_1222', 'app_1637', 'app_3414',  'app_4608',
                       'app_6683', 'app_7102', 'app_80', 'app_4210']
        while True:
            machine = []
            for i in range(6):
                machine.append([nichi_index[i], self.app[nichi_index[i]][-1]])
                self.app[nichi_index[i]].pop()
                if len(self.app[nichi_index[i]]) == 0:
                    del self.app[nichi_index[i]]
                    nichi_index[i] = nichi_index[-1]
                    nichi_index.pop()
                if len(nichi_index) == 5:
                    break
            set0[self.avalable[mac]] = machine
            mac += 1
            if len(nichi_index) == 5:
                break
        for i in set0:
            cpu = np.zeros(98)
            memo = np.zeros(98)
            disk = 0
            for j in set0[i]:
                cpu += self.source['cpu'][j[0]]
                memo += self.source['memo'][j[0]]
                disk += self.source['disk'][j[0]]
            if disk > 600:
                print('diskerror')
            for j in range(98):
                if cpu[j] > 32:
                    print('cpuerror')
                    print(set0[i])
                    break
                if memo[j] > 64:
                    print(set0[i])
                    print('memoerror')
                    break
        del self.avalable[:208]
        self.schedule = Series(set0)

    def classify(self):
        for i in self.schedule.index:
            tabu = []
            app = []
            for j in self.schedule[i]:
                app.append(j[0])
                if j[0] in self.icpb.index:
                    cop = self.icpb[j[0]].copy()
                    if j[0] in cop:
                        cop.remove(j[0])
                    tabu.extend(cop)
            if len(app) != len(set(app)):
                print(self.schedule[i])
                print('sameerror')
            for j in self.schedule[i]:
                if j[0] in tabu:
                    print(tabu)
                    print(j[0])
                    print('tabuerror')
                    break
        lar = []
        med = []
        dla = []
        smn = []
        for i in self.app.index:
            c = self.source['cpum'][i]
            m = self.source['memom'][i]
            d = self.source['disk'][i]
            if c >= 4:
                if d > 300:
                    lar.append([i, c, m, d])   #4
                else:
                    med.append([i, c, m, d])   #820
            elif c >= 0.4:
                if d > 300:
                    dla.append([i, c, m, d])    #31
                else:
                    smn.append([i, c, m, d])   #8477
            else: print('error')
        lar += dla + med
        lnum = 0
        for i in lar:
            lnum += len(self.app[i]) #3420
        small = self.avalable[:2792]
        large = self.avalable[2792:]        #1755
        clarge = large.copy()
        csmall = small.copy()
        largeset = {}
        num = 0
        for i in self.app.index:
            for j in self.app[i]:
                num += 1
        cou = 0
        larco = lar.copy()
        for i in larco:
            larin = self.app[i[0]].copy()
            for j in larin:
                machine = [0, 0, 0, []]
                tabu = []
                machine[3].append([i[0], j])  # 添加大的app逐个添加inst
                machine[0] = i[1]  # 添加cpu
                machine[1] = i[2]  # 添加memo
                machine[2] = i[3]  # disk
                counter = smn.copy()
                if i[0] in self.icpb.index:
                    tabu.extend(self.icpb[i[0]])  # 增加禁忌表
                while machine[0] < 50 and machine[1] < 280 and machine[2] < 1024:
                    if len(counter) == 0:
                        break
                    flag = False
                    con_flag = False
                    r = counter[random.randint(0, len(counter) - 1)]  # 随机选取一个app
                    tabnum = 0
                    if r[0] not in tabu:
                        if r[0] in self.icpb.index:
                            for l in machine[3]:
                                if l[0] in self.icpb[r[0]]:
                                    con_flag = True
                                    tabnum += 1
                        if con_flag:
                            if len(counter) < 100:
                                break
                            else:
                                if tabnum < len(counter):
                                    continue
                                elif tabnum == len(counter):
                                    break
                                else:
                                    print('counerror')
                    else:
                        le = 0
                        for l in counter:
                            if l[0] in tabu:
                                le += 1
                        if le == len(counter):  # 全在禁忌表中
                            break
                        else:
                            continue
                    if r[0] in self.icpb.index:
                        tabu.extend(self.icpb[r[0]])
                    machine[3].append([r[0], self.app[r[0]][-1]])  # 添加实例信息
                    machine[0] += r[1]  # cpu
                    machine[1] += r[2]  # 内存
                    machine[2] += r[3]  # 硬盘
                    self.app[r[0]].pop()
                    counter.remove(r)  # 以免重复
                    if machine[0] > 50 or machine[1] > 280 or machine[2] > 1024:
                        self.app[r[0]].append(machine[3][-1][1])
                        machine[3].pop()
                        machine[0] -= r[1]
                        machine[1] -= r[2]
                        machine[2] -= r[3]
                        flag = True
                    if len(self.app[r[0]]) == 0:
                        del self.app[r[0]]
                        smn.remove(r)
                    if flag:
                        break
                self.app[i[0]].remove(j)
                cou += 1
                largeset[large[-1]] = machine[3]
                large.pop()
                if len(large) == 0:
                    break
            if len(large) == 0:
                break
            lar.remove(i)
            if len(self.app[i[0]]) == 0:
                del self.app[i[0]]
        if len(smn) + len(lar) != len(self.app):
            print('lenerror')
        if len(largeset) != cou:
            print('error')
        larnum = 0
        for i in largeset:
            for j in largeset[i]:
                larnum += 1
        lefnum = 0
        for i in self.app:
            lefnum += len(i)
        if lefnum + larnum != num:
            print('larnumerror')
        if len(largeset) != cou:
            print('error')
        for i in largeset:
            cpu = np.zeros(98)
            memo = np.zeros(98)
            for j in largeset[i]:
                cpu += self.source['cpu'][j[0]]
                memo += self.source['memo'][j[0]]
            for k in range(98):
                if cpu[k] > 92:
                    print('cpuerror')
                if memo[k] > 288:
                    print('memoerror')
                    break
        for i in largeset:
            tabu = []
            app = []
            for j in largeset[i]:
                app.append(j[0])
                if j[0] in self.icpb.index:
                    cop = self.icpb[j[0]].copy()
                    if j[0] in cop:
                        cop.remove(j[0])
                    tabu.extend(cop)
            if len(app) != len(set(app)):
                print('sameerror')
            for j in largeset[i]:
                if j[0] in tabu:
                    print('tabuerror')
        smallest = {}
        nex = lar + smn
        for i in nex:
            if i[0] in self.app.index:
                coun = self.app[i[0]].copy()
            else:
                continue
            for j in coun:
                machine = [0, 0, 0, []]
                tabu = []
                machine[3].append([i[0], j])  # 添加app逐个添加inst
                machine[0] = i[1]  # 添加cpu
                machine[1] = i[2]  # 添加memo
                machine[2] = i[3]  # disk
                self.app[i[0]].remove(j)
                if i[0] in self.icpb.index:
                    tabu.extend(self.icpb[i[0]])
                for l in self.app.index:
                    if l == i[0]:
                        continue
                    con_flag = False
                    if l not in tabu:
                        if l in self.icpb.index:
                            for m in machine[3]:
                                if m[0] in self.icpb[l]:
                                    con_flag = True
                        if con_flag:
                            continue
                        if l in self.icpb.index:
                            tabu.extend(self.icpb[l])
                        machine[0] += np.mean(self.source['cpu'][l])
                        machine[1] += np.mean(self.source['memo'][l])
                        machine[2] += self.source['disk'][l]
                        machine[3].append([l, self.app[l][-1]])
                        self.app[l].pop()
                    else:
                        continue
                    if machine[0] > 20 or machine[1] > 60 or machine[2] > 600:
                        self.app[l].append(machine[3][-1][1])
                        machine[3].pop()
                        machine[0] -= np.mean(self.source['cpu'][l])
                        machine[1] -= np.mean(self.source['memo'][l])
                        machine[2] -= self.source['disk'][l]
                        break
                for k in self.app.index:
                    if len(self.app[k]) == 0:
                        del self.app[k]
                smallest[small[-1]] = machine[3]
                small.pop()
                if len(small) == 0:
                    break
            if len(small) == 0:
                break
        amend = []
        for i in smallest:
            cpu = np.zeros(98)
            memo = np.zeros(98)
            for j in smallest[i]:
                cpu += self.source['cpu'][j[0]]
                memo += self.source['memo'][j[0]]
            for k in range(98):
                if cpu[k] > 32:
                    print('smcpuerror')
                    break
                if memo[k] > 64:
                    amend.append(i)
                    break
        for i in amend:
            while True:
                coun = 0
                memo = np.zeros(98)
                for j in smallest[i]:
                    memo += self.source['memo'][j[0]]
                for k in memo:
                    if k > 64:
                        memo -= self.source['memo'][smallest[i][-1][0]]
                        if smallest[i][-1][0] in self.app.index:
                            self.app[smallest[i][-1][0]].append(smallest[i][-1][1])
                        else:
                            self.app[smallest[i][-1][0]] = [smallest[i][-1][1]]
                        smallest[i].pop()
                        break
                    else:
                        coun += 1
                if coun == 98:
                    break
        lanum = 0
        for i in self.app:
            lanum += len(i)
        for i in self.app.index:
            while len(self.app[i]) > 0:
                num = 0
                while True:
                    r = clarge[num]
                    num += 1
                    tabu = []
                    con_flag = False
                    for j in largeset[r]:
                        if i == j[0]:
                            con_flag = True
                        if j[0] in self.icpb.index:
                            tabu.extend(self.icpb[j[0]])
                    if i in self.icpb.index:
                        for l in largeset[r]:
                            if l[0] in self.icpb[i]:
                                con_flag = True
                    if con_flag:
                        continue
                    if i not in tabu:
                        largeset[r].append([i, self.app[i][-1]])
                    else:
                        continue
                    cpu = np.zeros(98)
                    memo = np.zeros(98)
                    disk = 0
                    for m in largeset[r]:
                        cpu += self.source['cpu'][m[0]]
                        memo += self.source['memo'][m[0]]
                        disk += self.source['disk'][m[0]]
                    flag = True
                    for k in range(98):
                        if cpu[k] > 92 or memo[k] > 288:
                            flag = False
                    if disk < 1024 and flag:      #满足条件
                        self.app[i].pop()
                        break
                    else:
                        largeset[r].pop()
                    if num == len(clarge):
                        break
                if num == len(clarge):
                    break
        for i in self.app.index:
            while len(self.app[i]) > 0:
                num = 0
                while True:
                    r = csmall[num]
                    num += 1
                    tabu = []
                    con_flag = False
                    for j in smallest[r]:
                        if i == j[0]:
                            con_flag = True
                        if j[0] in self.icpb.index:
                            tabu.extend(self.icpb[j[0]])
                    if i in self.icpb.index:
                        for l in smallest[r]:
                            if l[0] in self.icpb[i]:
                                con_flag = True
                    if con_flag:
                        continue
                    if i not in tabu:
                        smallest[r].append([i, self.app[i][-1]])
                    else:
                        continue
                    cpu = np.zeros(98)
                    memo = np.zeros(98)
                    disk = 0
                    for m in smallest[r]:
                        cpu += self.source['cpu'][m[0]]
                        memo += self.source['memo'][m[0]]
                        disk += self.source['disk'][m[0]]
                    flag = True
                    for k in range(98):
                        if cpu[k] > 32 or memo[k] > 64:
                            flag = False
                    if disk < 600 and flag:      #满足条件
                        self.app[i].pop()
                        break
                    else:
                        smallest[r].pop()
                    if num == len(csmall):
                        break
                if num == len(csmall):
                    break
        for i in smallest:
            cpu = np.zeros(98)
            memo = np.zeros(98)
            disk = 0
            for j in smallest[i]:
                cpu += self.source['cpu'][j[0]]
                memo += self.source['memo'][j[0]]
                disk += self.source['disk'][j[0]]
            if disk > 600:
                print('diskerror')
            for j in range(98):
                if cpu[j] > 32:
                    print('cpuerror')
                    break
                if memo[j] > 64:
                    print('memoerror')
                    break
        for i in largeset:
            cpu = np.zeros(98)
            memo = np.zeros(98)
            disk = 0
            for j in largeset[i]:
                cpu += self.source['cpu'][j[0]]
                memo += self.source['memo'][j[0]]
                disk += self.source['disk'][j[0]]
            if disk > 1024:
                print('diskerror')
            for j in range(98):
                if cpu[j] > 92:
                    print('cpuerror')
                    break
                if memo[j] > 288:
                    print('memoerror')
                    break
        largeset.update(smallest)
        result = Series(largeset)
        for i in largeset:
            tabu = []
            app = []
            for j in largeset[i]:
                app.append(j[0])
                if j[0] in self.icpb.index:
                    cop = self.icpb[j[0]].copy()
                    if j[0] in cop:
                        cop.remove(j[0])
                    tabu.extend(cop)
            if len(app) != len(set(app)):
                print('sameerror')
            for j in largeset[i]:
                if j[0] in tabu:
                    print('tabuerror')
        self.schedule = self.schedule.append(result)
        lenth = 0
        for i in self.schedule:
            lenth += len(i)
        if lenth != 68219:
            print('lenerror')

    def genre(self):
        inst = []
        mach = []
        app = []
        if len(self.schedule.index) != len(set(self.schedule.index)) != 6000:
            print('machineerror')
        for i in self.schedule.index:
            for j in self.schedule[i]:
                inst.append(j[1])
                app.append(j[0])
                mach.append(i)
        if len(inst) != len(set(inst)):
            print('lentherror')
        result = DataFrame()
        result['inst'] = inst
        result['app'] = app
        result['machine'] = mach
        result.to_csv('result_A')

    def check(self):
        schedule = pd.read_csv('result_A.csv')
        print(self.schedule)

S = schedule(1)
S.read()
#S.nichi()
#S.classify()
#S.genre()
S.check()
