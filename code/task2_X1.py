# -*- coding:utf-8 -*-
#画饼图，找峰值（峰值图分两种画法）

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import datetime as dt
pd.set_option('display.max_columns', None) #完全显示

#导入食堂消费数据
cons = pd.read_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task1_X3.csv',encoding='gbk')

#时间节点
print('现在时间为：',dt.datetime.now())
str0 = input('请按%Y-%m-%d %H:%M:%S 输入今日十一点：')
str1 = input('请按%Y-%m-%d %H:%M:%S 输入今日十四点：')
str2 = input('请按%Y-%m-%d %H:%M:%S 输入今日十七点：')
str3 = input('请按%Y-%m-%d %H:%M:%S 输入今日二十点：')
noon = dt.datetime.strptime(str0,'%Y-%m-%d %H:%M:%S')
tea = dt.datetime.strptime(str1,'%Y-%m-%d %H:%M:%S')
eve = dt.datetime.strptime(str2,'%Y-%m-%d %H:%M:%S')
xia = dt.datetime.strptime(str3,'%Y-%m-%d %H:%M:%S')

#将时间列数据转换
cons['Timeline'] =pd.to_datetime(cons['Timeline'])
#按时间分组：早、中、晚
print('开始分组。',dt.datetime.now())
m = cons[(cons['Timeline']<noon)]
n = cons[(cons['Timeline']<tea)&(cons['Timeline']>=noon)]
e = cons[(cons['Timeline']<xia)&(cons['Timeline']>=eve)]
print('分组完成。',dt.datetime.now())
print('检查分组结果：')
print(m.head(3))
print(n.head(3))
print(e.head(3))
#画饼
#先计算总和
#再用总和来画饼
def bingtu(data):
    string = input('请输入该表格名称：')
    num = len(data) #查看就餐总人次
    str2 = '         ——4月就餐总人次为：'+str(num)
    value = data['Dept'].value_counts()
    print(value)#看看怎么解决标签的问题
    can = list(value.index)  # 餐厅，做标签
    matplotlib.rcParams['font.sans-serif']=['SimHei'] #解决中文乱码问题
    length = [i/20 for i in range(value.size)]
    if (value[-1]/num)<0.001 :
        length[-1] += 0.3
    plt.pie(value,autopct='%.2f %%',explode=length,labels=can,labeldistance=1.1)
    plt.title(string+'\n'+str2)
    path = 'C:/Users/lenovo/Desktop/学生校园消费行为分析/pic/'+string+'.png'
    plt.savefig(path)
    plt.show()

print('将绘制早餐各食堂就餐人次占比图')
bingtu(m)
print('将绘制午餐各食堂就餐人次占比图')
bingtu(n)
print('将绘制晚餐各食堂就餐人次占比图')
bingtu(e)

#工作日与非工作日就餐曲线
#变换时间序列
time = cons.Timeline.map(lambda x:x.strftime('%H:%M:%S'))
time = time.to_frame()
time.columns = ['Time_1']
cons = pd.concat([cons,time],axis=1,join='inner')
cons = cons.drop('Timeline',axis=1)#去除
t = list(cons.columns).index('Time_1')
cons.rename(columns={ cons.columns[t]: "Timeline"}, inplace=True)
print('检查时间序列变换与否：')
print(cons.head(3))
#第一步，将数据集分成工作日与非工作日
cons['Day'] =pd.to_datetime(cons['Day'])
d = list(cons.columns).index('Day')  # 查看'Day'所在的列
str = ['2019-04-05 0:00:00','2019-04-06 0:00:00','2019-04-07 0:00:00','2019-04-13 0:00:00','2019-04-14 0:00:00','2019-04-20 0:00:00','2019-04-21 0:00:00','2019-04-27 0:00:00']
wk = []
for i in range(len(str)):
    wk.append(dt.datetime.strptime(str[i], '%Y-%m-%d %H:%M:%S'))
week = cons[(True^cons['Day'].isin(wk))]#取相反就是了
holiday = cons[cons['Day'].isin(wk)]
print('检查分组情况：')
print('WEEK:')
print(week.head(5))
print('HOLIDAY:')
print(holiday.head(5))

print('绘制工作日与非工作日就餐曲线图：')
title = input('请输入该图片名称：')
day = len(holiday['Day'].value_counts().index) #用来统计该数据集含有多少天，以作日均
res = holiday['Timeline'].value_counts()
res = res.sort_index()
time = res.index
value = res.values/day

day2 = len(week['Day'].value_counts().index) #用来统计该数据集含有多少天，以作日均
res2 = week['Timeline'].value_counts()
res2 = res2.sort_index()
time2 = res2.index
value2 = res2.values/day2

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码问题
fig = plt.figure(figsize=(10,6))
plt.plot(time2,value2,color='deepskyblue',marker='P',markersize=4,label='weekday')
plt.plot(time,value,color='orange',marker='D',markersize=4,label='holiday')
plt.legend()
plt.title(title)
plt.xlabel('时间')
plt.ylabel('日均累计就餐人数')
fig.autofmt_xdate(rotation=45)
path = 'C:/Users/lenovo/Desktop/学生校园消费行为分析/pic/工作日和非工作日就餐曲线图.png'
plt.savefig(path)
plt.show()

'''#单个图
def fengzhi(h):
    d = list(h.columns).index('Day')#查看'Day'所在的列
    day = len(h['Day'].value_counts().index) #用来统计该数据集含有多少天，以作日均
    res = h['Timeline'].value_counts()
    res = res.sort_index()
    time = res.index #时间段，做x轴
    value = res.values/day #日均值，做y轴
    if day>1:
        y_name = '日均累计就餐人数'
        title = input('请输入该图片名称：')
        path = 'C:/Users/lenovo/Desktop/学生校园消费行为分析/pic/' + title + '.png'
    else:
        y_name = '累计就餐人数'
        title = str(h.iloc[0, d]) + ' 就餐曲线图'
        path = 'C:/Users/lenovo/Desktop/学生校园消费行为分析/pic/' + str(h.iloc[0, d]) + '.png'

    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码问题
    fig = plt.figure(figsize=(10,6))
    plt.plot(time,value,marker='o')
    plt.title(title)
    plt.xlabel('时间')
    plt.ylabel(y_name)
    fig.autofmt_xdate(rotation=45)
    plt.savefig(path)
    plt.show()

#按工作日与非工作日输出就餐曲线图
print('现在绘制的数据集为：假期数据集')
fengzhi(holiday)
print('现在绘制的数据集为：工作日数据集')
fengzhi(week)
'''


