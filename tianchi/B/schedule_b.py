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
        self.used = DataFrame            #已经使用的机器资源情况
        self.avalable = []        #可用机器

    def read(self):
        inc = pd.read_csv('incompatible.csv', header=None)
        incom = {'app_1002': ['app_6659']}
        for i in range(1, len(inc[0])):
            if inc[0][i-1] != inc[0][i]:
                incom[inc[0][i]] = []
                incom[inc[0][i]].append(inc[1][i])
            else:
                incom[inc[0][i]].append(inc[1][i])
        self.icpb = Series(incom)       #不兼容的
        machine = pd.read_csv('scheduling_preliminary_b_machine_resources_20180726.csv', header=None,
                              names=['name', 'cpu', 'memo', 'disk', 'p', 'm', 'pm'])
        a = DataFrame(machine[['cpu', 'memo', 'disk', 'p', 'm', 'pm']],)
        a.index = list(machine['name'])
        self.machine = a                        #每个机器的信息，容量
        ap = pd.read_csv('belong.csv', header=None)
        app = {'app_1': ['inst_18457']}
        for i in range(1, len(ap[0])):
            if ap[1][i-1] != ap[1][i]:
                app[ap[1][i]] = []
                app[ap[1][i]].append(ap[0][i])
            else:
                app[ap[1][i]].append(ap[0][i])
        self.app = Series(app)                  #每个APP所有的实例
        inf = pd.read_csv('resource.csv', header=None)
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
        icpb = {'app_1222': ['app_1222'], 'app_8223': ['app_8223', 'app_7102'], 'app_3414': ['app_7102'],
                'app_4608': ['app_22', 'app_255', 'app_7102'], 'app_6683': ['app_1637'], 'app_7102': ['app_8223']}
        set = {}
        ind = 0
        while len(self.app['app_4608']) > 0:
            if len(self.app['app_8223']) > 0:
                set[self.avalable[ind]] = [['app_8223', self.app['app_8223'][-1]], ['app_4608', self.app['app_4608'][-1]]]
                self.app['app_4608'].pop()
                self.app['app_8223'].pop()
            else:
                set[self.avalable[ind]] = [['app_6683', self.app['app_6683'][-1]], ['app_4608', self.app['app_4608'][-1]]]
                self.app['app_4608'].pop()
                self.app['app_6683'].pop()
            ind += 1
        while len(self.app['app_7102']) > 0:
            set[self.avalable[ind]] = [['app_7102', self.app['app_7102'][-1]], ['app_6683', self.app['app_6683'][-1]]]
            self.app['app_7102'].pop()
            self.app['app_6683'].pop()
            ind += 1
        while len(self.app['app_80']) > 0:             #145个
            if len(self.app['app_3414']) > 0:
                set[self.avalable[ind]] = [['app_80', self.app['app_80'][-1]],
                                           ['app_3414', self.app['app_3414'][-1]]]
                self.app['app_80'].pop()
                self.app['app_3414'].pop()
            else:
                set[self.avalable[ind]] = [['app_80', self.app['app_80'][-1]],
                                           ['app_4210', self.app['app_4210'][-1]]]
                self.app['app_80'].pop()
                self.app['app_4210'].pop()
            ind += 1
        for i in set:
            cpu = np.zeros(98)
            memo = np.zeros(98)
            for j in set[i]:
                cpu += self.source['cpu'][j[0]]
                memo += self.source['memo'][j[0]]
            for k in range(98):
                if cpu[k] > 32:
                    print(set[i])
                    print(cpu)        #无问题
                if memo[k] > 64:
                    print('memoerror')
                    break
        del self.avalable[0:ind]             #更新可用machine
        for i in nichi_index:
            if len(self.app[i]) == 0:
                del self.app[i]
        diskf = {'app_30': ['inst_31938', 'inst_27198', 'inst_34986', 'inst_67759', ], 'app_3678': ['inst_39867', 'inst_11'],
                 'app_5003': ['inst_82625', 'inst_64831', 'inst_55879'], 'app_8862': ['inst_52338', 'inst_31042'],
                 'app_6065': ['inst_33147', 'inst_66730']}
        #硬盘1000以上且未部署
        set[self.avalable[-1]] = [['app_30', 'inst_31938']]
        set[self.avalable[-2]] = [['app_30', 'inst_27198']]
        set[self.avalable[-3]] = [['app_30', 'inst_34986']]
        set[self.avalable[-4]] = [['app_30', 'inst_67759']]
        set[self.avalable[-5]] = [['app_3678', 'inst_39867']]
        set[self.avalable[-6]] = [['app_3678', 'inst_11']]
        set[self.avalable[-7]] = [['app_5003', 'inst_82625']]
        set[self.avalable[-8]] = [['app_5003', 'inst_64831']]
        set[self.avalable[-9]] = [['app_5003', 'inst_55879']]
        set[self.avalable[-10]] = [['app_8862', 'inst_52338']]
        set[self.avalable[-11]] = [['app_8862', 'inst_31042']]
        set[self.avalable[-12]] = [['app_6065', 'inst_33147']]
        set[self.avalable[-13]] = [['app_6065', 'inst_66730']]
        seriset = Series(set)
        del self.avalable[-13:]
        del self.app['app_30']
        del self.app['app_3678']
        del self.app['app_5003']
        del self.app['app_8862']
        del self.app['app_6065']
        self.schedule = seriset

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
                print('sameerror')
            for j in self.schedule[i]:
                if j[0] in tabu:
                    print('tabuerror')
        lar = []
        smn = []
        hug = []
        for i in self.app.index:
            c = self.source['cpum'][i]
            m = self.source['memom'][i]
            d = self.source['disk'][i]
            if c >= 16:
                hug.append([i, c, m, d])   #71
            elif c >= 9:
                lar.append([i, c, m, d])
            elif c >= 0.4:
                smn.append([i, c, m, d])   #9257
            else: print('error')
        small = self.avalable[:2643]
        large = self.avalable[2643:]        #1755
        clarge = large.copy()
        largeset = {}
        num = 0
        for i in self.app.index:
            for j in self.app[i]:
                num += 1
        cou = 0
        lar = hug + lar
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
                while machine[0] < 45 and machine[1] < 250 and machine[2] < 2457:
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
                    if machine[0] > 45 or machine[1] > 250 or machine[2] > 2457:
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
        amend = []
        for i in largeset:
            cpu = np.zeros(98)
            memo = np.zeros(98)
            for j in largeset[i]:
                cpu += self.source['cpu'][j[0]]
                memo += self.source['memo'][j[0]]
            for k in range(98):
                if cpu[k] > 92:
                    amend.append(i)
                    raise KeyError
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
        dicl = 0
        for i in largeset:
            for j in largeset[i]:
                dicl += 1
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
                    if machine[0] > 18 or machine[1] > 60 or machine[2] > 1440:
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
        for i in smallest:
            cpu = np.zeros(98)
            memo = np.zeros(98)
            for j in smallest[i]:
                cpu += self.source['cpu'][j[0]]
                memo += self.source['memo'][j[0]]
            for k in range(98):
                if cpu[k] > 32:
                    amend.append(i)
                    break
                if memo[k] > 64:
                    print('memoerror')
                    break
        for i in amend:
            while True:
                coun = 0
                cpu = np.zeros(98)
                for j in smallest[i]:
                    cpu += self.source['cpu'][j[0]]
                for k in cpu:
                    if k > 32:
                        cpu -= self.source['cpu'][smallest[i][-1][0]]
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
        dics = 0
        for i in smallest:
            dics += len(smallest[i])
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
                    if disk < 2457 and flag:      #满足条件
                        self.app[i].pop()
                        break
                    else:
                        largeset[r].pop()
        for i in smallest:
            cpu = np.zeros(98)
            memo = np.zeros(98)
            disk = 0
            for j in smallest[i]:
                cpu += self.source['cpu'][j[0]]
                memo += self.source['memo'][j[0]]
                disk += self.source['disk'][j[0]]
            if disk > 1440:
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
            if disk > 2457:
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
        if lenth != 68224:
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
        result.to_csv('result_B')
S = schedule(1)
S.read()
#S.nichi()
#S.classify()
#S.genre()
