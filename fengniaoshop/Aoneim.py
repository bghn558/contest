import pandas as pd
import datetime
import numpy as py
import sys

year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day
hour = datetime.datetime.now().hour
selectstore = {'北京':['北京仓','上海仓','宅急送-广州仓'],'黑龙江省':['北京仓','上海仓','宅急送-广州仓'],
               '吉林省':['北京仓','上海仓','宅急送-广州仓'],'辽宁省':['北京仓','上海仓','宅急送-广州仓'],
               '内蒙古自治区':['北京仓','上海仓','宅急送-广州仓'],'宁夏回族自治区':['北京仓','上海仓','宅急送-广州仓'],
               '甘肃省':['北京仓','上海仓','宅急送-广州仓'],'山西省':['北京仓','上海仓','宅急送-广州仓'],
               '河北省':['北京仓','上海仓','宅急送-广州仓'],'天津':['北京仓','上海仓','宅急送-广州仓'],
               '山东省': ['北京仓','上海仓','宅急送-广州仓'],'广东省': ['宅急送-广州仓','上海仓','北京仓'],
               '湖南省': ['宅急送-广州仓','上海仓','北京仓'],'贵州省': ['宅急送-广州仓','上海仓','北京仓'],
               '广西壮族自治区': ['宅急送-广州仓','上海仓','北京仓'],'云南省': ['宅急送-广州仓','上海仓','北京仓'],
               '江西省': ['宅急送-广州仓','上海仓','北京仓'],'福建省': ['宅急送-广州仓','上海仓','北京仓'],
               '海南省': ['宅急送-广州仓','上海仓','北京仓'],'上海': ['上海仓','北京仓','宅急送-广州仓'],
               '江苏省': ['上海仓','北京仓','宅急送-广州仓'],'浙江省': ['上海仓','北京仓','宅急送-广州仓'],
               '安徽省':['上海仓','北京仓','宅急送-广州仓'],'河南省':['上海仓','北京仓','宅急送-广州仓'],
               '湖北省':['上海仓','北京仓','宅急送-广州仓'],'四川省':['上海仓','北京仓','宅急送-广州仓'],
               '陕西省':['上海仓','北京仓','宅急送-广州仓'],'青海省':['上海仓','宅急送-广州仓','北京仓'],
               '新疆维吾尔族自治区':['上海仓','宅急送-广州仓','北京仓'],'重庆':['上海仓','北京仓','宅急送-广州仓']}

#stock = pd.read_csv('stock214.csv', encoding="gb2312",converters={'物料编码': str})
stock = pd.read_csv('stock4118.csv', encoding="utf_8_sig",converters={'物料编码': str})


def check(code,store,num):
    #print(code,store,num)
    #print(stock['物料编码'])
    index = stock[(stock['物料编码']==code)&(stock['仓库']==store)].index.tolist()
    #print(index)
    #print(index[0])
    inventory = stock['库存数量'][index[0]]
    if  inventory < num: # orinventory < 10 :
        return False
    else:
        inventory -= num
        stock['库存数量'][index] = inventory
        return True


orders = pd.read_excel('412.xls',encoding='utf-8',converters={'收货人电话': str})

location = orders['收货地址'].str.split(n=2, expand=True)
location.columns = ['省', '市', '地址']

Aone = pd.DataFrame(columns=['单据类型', '领用仓库', '运费', '客户名称', '来源单据','扣款ID号','联系人','联系方式'
                             ,'省','市','详细地址','说明（头上）','物料编码','物料名称','数量','备注（行上）','领用公司'])
orders['商家编码'] = orders['商家编码'].map(str.strip)
Aone.loc[0] = ['销售类领用申请单-蜂鸟商城',None,None,None,None,None,None,None,
             None,None,None,None,None,None,None,None,'拉扎斯网络科技（上海）有限公司']

for i in orders.index:
    counter = 0
    warehouse = None
    name = None
    for m in selectstore[location['省'][i]]:
        if check(orders['商家编码'][i],m,orders['数量'][i]):
            warehouse = m
            index = stock[(stock['物料编码'] == orders['商家编码'][i]) & (stock['仓库'] == m)].index.tolist()
            name = stock['物料名称'][index[0]]
            break
        counter += 1
    if warehouse == None:
        print('out of stock')
        print(orders.loc[i])
        raise ValueError
    if len(location['省'][i]) < 3:
        location['省'][i] += '市'
    Aone.loc[i+1] = ['销售类领用申请单-蜂鸟商城',warehouse,None,orders['收货人'][i],None,None,orders['收货人'][i],orders['收货人电话'][i],
                   location['省'][i],location['市'][i],orders['收货地址'][i],None,orders['商家编码'][i],
                   name,orders['数量'][i],None,'拉扎斯网络科技（上海）有限公司']


Aone.to_excel(str(year)+str(month)+str(day)+str(hour)+'.xls', index=0, encoding='utf_8_sig')
stock.to_csv('stock'+str(month)+str(day)+str(hour)+'.csv', index=0, encoding='utf_8_sig')
