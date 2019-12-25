# -*- coding:utf-8 -*-
#对个人进行分类
#聚类的指标计算
import pandas as pd
import datetime as dt
pd.set_option('display.max_columns', None) #完全显示
#专注于个人数据
et = pd.read_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task1_X4.csv',encoding='gbk')
print('去除 AccessCardNo 列。')
et = et.drop('AccessCardNo',axis=1)#去除)
info = pd.read_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/project_data/data1.csv',encoding='gbk')
print('登记在册总人数有：',info.shape[0])
c_gb = et[['Money','CardNo','Dept','Day','Timeline']].groupby([et['CardNo']])#以卡号划分，因为每个人的卡号是独特的
#########################################################################################################################################
#计算消费次数，计算平均消费（全部与部分）
#工作日与非工作日划分：
str = ['2019-04-05 0:00:00', '2019-04-06 0:00:00', '2019-04-07 0:00:00', '2019-04-13 0:00:00', '2019-04-14 0:00:00',
           '2019-04-20 0:00:00', '2019-04-21 0:00:00', '2019-04-27 0:00:00']
wd = []
for i in range(len(str)):
    wd.append(dt.datetime.strptime(str[i], '%Y-%m-%d %H:%M:%S'))
stats = {'CardNo':[],'Count':[],'mean':[],'work_mean':[],'holiday_mean':[]}
for n,g in c_gb:
    g['Day'] = pd.to_datetime(g['Day'])
    g_h = g[g['Day'].isin(wd)]
    g_w = g[(True^g['Day'].isin(wd))]
    #指标计算
    count = g['Money'].count()
    mean = g['Money'].mean()
    mean = round(mean,2)
    if g_h.empty:
        h_m =0
    else:
        h_m = round(g_h['Money'].mean(),2)
    if g_w.empty:
        w_m =0
    else:
        w_m = round(g_w['Money'].mean(),2)

    stats['CardNo'].append(n)
    stats['Count'].append(count)
    stats['mean'].append(mean)
    stats['work_mean'].append(w_m)
    stats['holiday_mean'].append(h_m)

stats = pd.DataFrame(stats)
# print(stats)
stats.to_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task3_X2.csv',encoding='gbk',index=None)

