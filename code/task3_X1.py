# -*- coding:utf-8 -*-
#对总体和不同专业不同性别数据进行分析
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import random
pd.set_option('display.max_columns', None) #完全显示

et = pd.read_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task1_X4.csv',encoding='gbk')
info = pd.read_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/project_data/data1.csv',encoding='gbk')
print('去除 AccessCardNo 列。')
et = et.drop('AccessCardNo',axis=1)#去除
print(et.head(3))
et_gb = et[['Money','CardNo','Dept','Day','Timeline']].groupby([et['Major'],et['Sex']])#以专业和性别进行分组
#########################################################################################################################################
#参与本月消费的人数：
people = et['CardNo'].value_counts().size
print('编号在册的18级学生总数为：',len(info))
print('参与本月消费的学生总数为：',people)
#计算人均刷卡频次
res = et.shape[0]/people
print('18级学生本月人均刷卡频次为：',round(res))
#计算人均消费金额
res = et['Money'].sum()/people
print('18级学生本月人均消费金额为：',round(res,2))


#对消费特征进行统计
#工作日与非工作日划分：
str = ['2019-04-05 0:00:00', '2019-04-06 0:00:00', '2019-04-07 0:00:00', '2019-04-13 0:00:00', '2019-04-14 0:00:00',
           '2019-04-20 0:00:00', '2019-04-21 0:00:00', '2019-04-27 0:00:00']
wd = []
for i in range(len(str)):
    wd.append(dt.datetime.strptime(str[i], '%Y-%m-%d %H:%M:%S'))

#此处用字典组建列表原件
#c_m 人均月度消费频次；
#m_m 均笔消费金额； wd_m 周末均笔消费金额；
#0:女；1：男
stats = {'name':[],'F_c_m':[],'M_c_m':[],'F_m_m':[],'M_m_m':[],'F_wd_m':[],'M_wd_m':[]}
num = 0 #用以标记（专业，性别）
for n,g in et_gb:
    # 将时间列数据转换
    g.loc[:,'Day'] = pd.to_datetime(g['Day'])
    g_wd = g[g['Day'].isin(wd)]
    #指标计算
    ppl = g['CardNo'].value_counts().size
    c_m = int(round(g['Money'].count() / ppl))
    m_m = round(g['Money'].sum()/ppl,2)
    wd_m = round(g_wd['Money'].mean(),2)
    if num%2==0:
        stats['name'].append(n[0])
        stats['F_c_m'].append(c_m)
        stats['F_m_m'].append(m_m)
        stats['F_wd_m'].append(wd_m)
    else:
        stats['M_c_m'].append(c_m)
        stats['M_m_m'].append(m_m)
        stats['M_wd_m'].append(wd_m)
    num +=1

#创建dataFrame
res = pd.DataFrame(stats)
print(res)
res.to_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task3_X1.csv',encoding='gbk',index=None)

#对分析结果做调查
print('不同专业女性月均笔消费极差：',res['F_m_m'].max()-res['F_m_m'].min())
print('不同专业男性月均笔消费极差：',res['M_m_m'].max()-res['M_m_m'].min())
print('不同专业女性月总刷卡极差：',res['F_c_m'].max()-res['F_c_m'].min())
print('不同专业男性月总刷卡极差：',res['M_c_m'].max()-res['M_c_m'].min())
print('不同专业女性周末均笔消费极差：',res['F_wd_m'].max()-res['F_wd_m'].min())
print('不同专业男性周末均笔消费极差：',res['M_wd_m'].max()-res['M_wd_m'].min())

#绘图
print('------------------------------------------以下会报错，但是不影响输出------------------------------------------------')
#不同专业不同性别人均消费柱状图：
def dif_sex_money_mean(res,num):
    plt.figure(figsize=(4,4))
    index = np.arange(0,0.4,0.2)
    f = list(res.columns).index('F_m_m')
    m = list(res.columns).index('M_m_m')
    n = list(res.columns).index('name')
    values = (float(res.iloc[num,f]),float(res.iloc[num,m]))
    width = 0.1
    str = res.iloc[num,n]
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码问题
    plt.bar(index,values,width)
    plt.title(str)
    plt.xlabel('Sex')
    plt.ylabel('人均消费/元')
    plt.xticks(index,('Female','Male'))
    for x,y in zip(index,values):
        plt.text(x,y+0.02,'%.2f' %y, ha='center',va='bottom')
    path = 'C:/Users/lenovo/Desktop/学生校园消费行为分析/pic/task3/人均消_'+str+'.png'
    plt.savefig(path)

#不同专业不同性别消费频次柱状图：
def dif_sex_consume_count(res,num):
    plt.figure(figsize=(4,4))
    index = np.arange(0,0.4,0.2)
    f = list(res.columns).index('F_c_m')
    m = list(res.columns).index('M_c_m')
    n = list(res.columns).index('name')
    values = (float(res.iloc[num,f]),float(res.iloc[num,m]))
    width = 0.1
    str = res.iloc[num,n]
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码问题
    plt.bar(index,values,width)
    plt.title(str)
    plt.xlabel('Sex')
    plt.ylabel('人均月总消费/次')
    plt.xticks(index,('Female','Male'))
    for x,y in zip(index,values):
        plt.text(x,y+0.02,'%.2f' %y, ha='center',va='bottom')
    path = 'C:/Users/lenovo/Desktop/学生校园消费行为分析/pic/task3/频次_'+str+'.png'
    plt.savefig(path)
#给所有专业绘制柱状图
for i in range(40):
    dif_sex_money_mean(res,i)

for i in range(40):
    dif_sex_consume_count(res,i)

#某专业专用
# num = random.randint(0,39)
# dif_sex_money_mean(res,num)
plt.show()