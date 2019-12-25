# -*- coding:utf-8 -*-
#查重及查缺失值处理及清楚非营业时间数据,并且将日期时间拆分为两列，并按时间排序。
#查重
#导入数据：
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None) #完全显示
#导入消费数据
info = pd.read_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/project_data/data2.csv',encoding='gbk',index_col=0)
print(info.columns)#查看列名
print(info.shape)
#18级学生信息表
info2 = pd.read_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/project_data/data1.csv',encoding='gbk',index_col=0)
print(info2.columns)#查看列名
print(info2.shape)

#对消费数据进行数据探索与预处理
print('去除 PeoNo 列。')
info = info.drop(['PeoNo'],axis=1) #去除

#数据探索-缺失值，重复值
info = info.drop_duplicates()
print(info.shape)#无重复值,根据计算已去除3个重复值
#针对同卡号消费次数去重
# #以下可查看重复的记录
# a = {k: tuple(d.index) for k, d in info.groupby(['CardNo','CardCount']) if len(d) > 1}
# print(a)
# for key in a.keys():
#     print(key)
#     for j in range(len(a[key])):
#         print(info.loc[info.index==a[key][j],:])
#经人工检查发现是同一个卡号有两张卡同时在消费。因此选择直接去重，只保留一个账户一段消费流水。
info = info.drop_duplicates(subset=['CardNo','CardCount'])
print(info.shape)#检查清理效果
print('去除 CardCount 列。')
info = info.drop(['CardCount'],axis=1) #去除

#查缺失值
print(info.isnull().sum())#查找缺失值
# 看看是哪些数据
print('------检查TermSerNo-------')
sample = info.dropna(subset=['TermSerNo'])#创建不含空值的列表以检测
print('TermSerNo 非空数据个数为：',len(sample))#查看有多少非空值
print(sample.describe())#查看数值统计描述
#抽样观察
for i in range(0,len(sample),round(len(sample)/20)):
    print(sample.iloc[i])
    sample['Date'] = pd.to_datetime(sample['Date'])
    time = dt.time(0,0,0)
for i in range(len(sample)):
    if sample.iloc[i]['Date'].time() != time:
        print(sample.iloc[i])
print('所有TermSerNo 值非空的样本交易时间都为00：00：00.')
# 通过抽样观察，此处标记的数据多为零点消费数据，暂时不处理；因此可直接将此列删去。
print('去除 TermSerNo 列。')
info = info.drop(['TermSerNo'],axis=1) #去除

print('------检查conOperNo-------')
sample = info.dropna(subset=['conOperNo'])#选取不含空值的样本以检测
print('conOperNo 非空数据个数为：',len(sample))#查看有多少非空值
for i in range(0,len(sample),round(len(sample)/20)):
    print(sample.iloc[i])#抽样观察
for i in range(len(sample)):
    if sample.iloc[i]['Type'] =='消费':
        print(sample.iloc[i])
print('所有conOperNo 值非空的样本交易类型都不为 消费 。')
#分析得出，这些都不是消费记录，可忽略，而该步骤将在后面进行数据类型选择时同时进行。
print('去除 conOperNo 列。')
new_info = info.drop('conOperNo',axis=1)#去除
print(new_info.isnull().sum())#检查是否仍含缺失值

#继续处理无用数列，只取消费数据
new_info = new_info[new_info['Type'].isin(['消费'])] #只含消费数据
print('处理后的数据为消费数据。')

print('去除 Surplus, FundMoney&Type 列。')
new_info = new_info.drop('FundMoney',axis=1)#去除
new_info = new_info.drop('Type',axis=1)#去除
new_info = new_info.drop('Surplus',axis=1)#去除
print(new_info.shape)

#导入日期和时间两列,按时间排序
print('开始导入日期和时间两列。')
new_info['Date'] = pd.to_datetime(new_info['Date'] )
day = new_info.Date.map(lambda x:x.strftime('%Y-%m-%d'))
day = day.to_frame()
day.columns = ['Day']

time = new_info.Date.map(lambda x:x.strftime('%H:%M:%S'))
time = time.to_frame()
time.columns = ['Time']

new_info = pd.concat([new_info,day],axis=1,join='inner')
new_info = pd.concat([new_info,time],axis=1,join='inner')
print(new_info.head(3))
#排序
print('按时间排序。开始时间为：',dt.datetime.now())
new_info.index = new_info['Date']
new_info = new_info.sort_index()
print('排序成功。')

print('去除 Date 列。')
new_info = new_info.drop('Date',axis=1)#去除

#对零点数据进行探索。因为零点数据比较特殊和 TermSerNo 值非空的样本交易时间有关。 当以下检查发现这些零点数据都为这些非空值，计划删去。
str = input('请按%Y-%m-%d %H:%M:%S 输入今日零点：')
time = dt.datetime.strptime(str,'%Y-%m-%d %H:%M:%S')
print(time)

new_info['Time'] = pd.to_datetime(new_info['Time'])
sample = new_info[new_info['Time'].isin([time])]
if len(sample)==7259:
    print('所有零点消费数据都为 TermSerNo 值非空的数据。计划删去零点数据。')
print(new_info.shape)
info = new_info[new_info['Time']>time]
print('成功删除零点消费数据。')
print(info.shape)

#假设营业时间为6:00-24:00, 因此计划将此之外的消费数据删去（但是会对24小时校医院消费数据造成影响--假设校医院24小时营业的情况下）
print('删除所有非营业时间的消费数据：')
str2 = input('请按%Y-%m-%d %H:%M:%S 输入今日六点：')
mor = dt.datetime.strptime(str2,'%Y-%m-%d %H:%M:%S')
info = new_info[new_info['Time']>=mor]
print(info.shape)

time = info.Time.map(lambda x:x.strftime('%H:%M:%S'))
time = time.to_frame()
time.columns = ['Time_1']
info = pd.concat([info,time],axis=1,join='inner')
info = info.drop('Time',axis=1)#去除
t = list(info.columns).index('Time_1')
info.rename(columns={ info.columns[t]: "Time"}, inplace=True)

#值异常
print('查看消费金额是否有异常值: ')
plt.boxplot(new_info['Money'])

plt.show()
# 虽然箱线图的区域远低于50，但是考虑到有单次高消费的情况及值在100以下仍旧有较高密度，因此将考察大于100的值。
print('\n','-------------------------检查大于100的记录：','\n')
M_sample = new_info[new_info['Money']>100]
#抽样观察
for i in range(0,len(M_sample),round(len(M_sample)/50)):
    print(M_sample.iloc[i])
#看上去没什么问题

#保存处理后的数据
info.to_csv('C:/Users/lenovo/Desktop/学生校园消费行为分析/result/task1_X1.csv',encoding='gbk',index=None)

